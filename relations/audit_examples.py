"""Audit the example pairs in examples/: does each MusicXML file show its relation, and does the model know it?

    ~/.venvs/musipam/bin/python audit_examples.py

For each example, the notes are read back from the MusicXML file, not from the code that wrote
it, and checked against the relation's definition by rules written independently of
musipam_rel/relations.py (the same notes, rhythm, register and spelling a musician would check).
Then the trained relation model scores the pair. Writes examples/AUDIT.md and examples/audit.json.

The audit cannot judge how natural a B sounds; that still needs a listener.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
from music21 import converter  # noqa: E402

from examples import TONIC  # noqa: E402
from musipam_rel.bart import RelationModel  # noqa: E402
from musipam_rel.features import codes, pair_code  # noqa: E402
from musipam_rel.motif import LETTERS, SCALES, Motif  # noqa: E402
from musipam_rel.paths import DATA, EXAMPLES, MODELS  # noqa: E402
from musipam_rel.relations import NAMES, RELATIONS  # noqa: E402

CLARINET = (50, 94)  # the stimuli's melody range (MIDI), stimgen/musipam_stim/validate.py


def read(path: Path, A: Motif):
    """(A, B) note lists from an example file: (letter height, MIDI, onset, duration) in quarter notes."""
    part = converter.parse(str(path)).parts[0].stripTies()
    tonic = TONIC[A.mode]
    t0 = 7 * 4 + LETTERS.index(tonic)
    b_start = A.span + A.bar
    a, b = [], []
    for n in part.flatten().notes:
        p, on = n.pitch, Fraction(n.offset).limit_denominator(48)
        row = (7 * p.octave + LETTERS.index(p.step) - t0, p.midi, float(on), float(n.quarterLength))
        (a if on < A.span else b).append(row if on < A.span else (row[0], row[1], float(on - Fraction(b_start).limit_denominator(48)), row[3]))
    return a, b


def letters(x):
    return [r[0] for r in x]


def midis(x):
    return [r[1] for r in x]


def rhythm(x):
    return [(round(r[2], 4), round(r[3], 4)) for r in x]


def steps(x):
    return [q - p for p, q in zip(letters(x), letters(x)[1:])]


def off_key(x, mode):
    """Notes outside the key's scale, as (letter height, semitones off)."""
    sc = SCALES[mode]
    out = []
    for L, m, _, _ in x:
        tonic_midi = 60 + {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[TONIC[mode]]
        alt = (m - tonic_midi) - (12 * (L // 7) + sc[L % 7])
        if alt:
            out.append((L, alt))
    return out


def minor_alterations_ok(x, mode):
    """In minor, the only alterations allowed are a raised 7th (and 6th) on the way up (melodic minor)."""
    if mode not in ("minor", "aeolian"):
        return not off_key(x, mode)
    return all(L % 7 in (5, 6) and alt == 1 for L, alt in off_key(x, mode))


def bar_split(x, bar):
    return [r for r in x if r[2] < bar - 1e-6], [r for r in x if r[2] >= bar - 1e-6]


def check(name: str, a, b, A: Motif) -> tuple[bool, str]:
    """Rule check of B against A for one relation. Returns (ok, what was checked)."""
    mode, bar = A.mode, A.bar
    same_r = rhythm(a) == rhythm(b)
    if name == "repeat":
        return midis(b) == midis(a) and same_r, "same pitches and rhythm"
    if name in ("octave_up", "octave_down"):
        k = 12 if name == "octave_up" else -12
        return [m + k for m in midis(a)] == midis(b) and same_r, f"every note {k:+d} semitones, same rhythm"
    if name.startswith("seq_"):
        k = int(name[-1]) * (1 if "_up_" in name else -1)
        ok = [L + k for L in letters(a)] == letters(b) and same_r and minor_alterations_ok(b, mode)
        return ok, f"every note {k:+d} scale steps, same rhythm, still in the key"
    if name in ("real_up", "real_down"):
        d = {m2 - m1 for m1, m2 in zip(midis(a), midis(b))}
        n = d.pop() if len(d) == 1 else None
        ok = n is not None and 1 <= abs(n) <= 5 and (n > 0) == (name == "real_up") and same_r and bool(off_key(b, mode))
        return ok, f"every note {n:+d} semitones, same rhythm, leaves the key" if n is not None else "not one interval"
    if name == "inversion":
        ok = letters(b)[0] == letters(a)[0] and [2 * letters(a)[0] - L for L in letters(a)] == letters(b) and same_r
        return ok, "intervals mirrored about the first note (in scale steps), same rhythm"
    if name == "retrograde":
        span = A.span
        rev_r = [(round(span - (o + d), 4), round(d, 4)) for _, _, o, d in a[::-1]]
        return letters(b) == letters(a)[::-1] and rhythm(b) == rev_r, "notes and rhythm backwards"
    if name == "retro_inversion":
        span = A.span
        inv = [2 * letters(a)[0] - L for L in letters(a)]
        rev_r = [(round(span - (o + d), 4), round(d, 4)) for _, _, o, d in a[::-1]]
        return letters(b) == inv[::-1] and rhythm(b) == rev_r, "mirrored, then backwards"
    if name in ("augmentation", "diminution"):
        f = 2.0 if name == "augmentation" else 0.5
        ok = midis(b) == midis(a) and rhythm(b) == [(round(o * f, 4), round(d * f, 4)) for _, _, o, d in a]
        return ok, f"same pitches, every onset and duration x{f:g}"
    if name == "rhythm_new":
        ok = midis(b) == midis(a) and not same_r and abs(sum(r[3] for r in b) - sum(r[3] for r in a)) < 1e-6
        return ok, "same pitches, a different rhythm of the same length"
    if name == "pitch_new":
        return same_r and letters(b)[0] == letters(a)[0] and steps(b) != steps(a), "same rhythm and first note, new pitches"
    if name == "mode_change":
        diffs = [(L % 7, m2 - m1) for (L, m1, _, _), m2 in zip(a, midis(b)) if m2 != m1]
        ok = letters(b) == letters(a) and same_r and diffs and all(dg in (2, 5, 6) and abs(s) == 1 for dg, s in diffs)
        return ok, "same letters and rhythm; only 3rds, 6ths and 7ths altered by a semitone"
    if name in ("ornament", "reduction"):
        full, plain = (b, a) if name == "ornament" else (a, b)
        at = {round(o, 4): (L, m) for L, m, o, _ in full}
        kept = all(at.get(round(o, 4)) == (L, m) for L, m, o, _ in plain)
        plain_on = {round(o, 4) for _, _, o, _ in plain}
        extra_ok, k = True, 0
        for i, (L, m, o, d) in enumerate(full):
            if round(o, 4) in plain_on:
                continue
            k += 1
            prev, nxt = full[i - 1][0], (full[i + 1][0] if i + 1 < len(full) else None)
            passing = nxt is not None and abs(nxt - prev) == 2 and L == (prev + nxt) // 2
            neighbor = abs(L - prev) == 1 and nxt == prev                      # x, x±1, (x)
            returning = i >= 2 and L == full[i - 2][0] and abs(prev - L) == 1  # (x, x±1,) x
            extra_ok &= passing or neighbor or returning
        return kept and k > 0 and extra_ok, (f"A's notes kept at their onsets; {k} added notes, each a passing tone "
                                              "or part of a neighbor-note figure")
    if name == "fragment":
        a1, _ = bar_split(a, bar)
        b1, b2 = bar_split(b, bar)
        s = {L2 - L1 for (L1, *_), (L2, *_) in zip(a1, b2)}
        ok = (letters(b1) == letters(a1) and rhythm(b1) == rhythm(a1) and len(s) == 1 and abs(next(iter(s))) == 1
              and [(round(o - bar, 4), d) for o, d in rhythm(b2)] == rhythm(a1))
        return ok, "bar 1 of A, then bar 1 again a scale step higher or lower"
    if name in ("opening_kept", "consequent", "ending_kept"):
        a1, a2 = bar_split(a, bar)
        b1, b2 = bar_split(b, bar)
        if name == "ending_kept":
            return (letters(b2) == letters(a2) and rhythm(b2) == rhythm(a2) and letters(b1) != letters(a1),
                    "A's second bar kept, a new first bar")
        tonic_end = letters(b)[-1] % 7 == 0
        ok = letters(b1) == letters(a1) and rhythm(b1) == rhythm(a1) and letters(b2) != letters(a2)
        if name == "opening_kept":
            return ok and not tonic_end, "A's first bar kept, a new second bar that does not end on the tonic"
        return ok and tonic_end and letters(a)[-1] % 7 != 0, "A ends away from the tonic; B keeps bar 1 and ends on it"
    if name == "unrelated":
        return steps(b) != steps(a) and not same_r, "different intervals and rhythm"
    raise KeyError(name)


def spell(x, mode):
    names = []
    for L, m, _, _ in x:
        letter = LETTERS[(LETTERS.index(TONIC[mode]) + L) % 7]
        names.append(letter)
    return names


def main() -> int:
    rows = [json.loads(line) for line in open(DATA / "pairs_test_in.jsonl")]
    by_base = defaultdict(dict)
    for r in rows:
        by_base[r["base"]].setdefault(r["label"], r)
    best = max(by_base, key=lambda b: (len(by_base[b]), -b))
    first = {}
    for r in rows:
        first.setdefault(r["label"], r)
    model = RelationModel.load(MODELS / "bart_symbolic.npz")

    lines = ["# Audit of the relation examples", "",
             "Each example file (A, a bar's rest, then B) was read back from its MusicXML and checked against the "
             "relation's definition with rules written independently of the code that made it "
             "(`audit_examples.py`). Then the trained model (`bart_symbolic.npz`) scored the pair. "
             "*p* is the model's probability for the relation the file illustrates; *rank* is that relation's place "
             "among all 26.", "",
             "| File | Relation | Definition check | B's range | Accidentals in B | Model's top relation (p) | p, rank of this relation |",
             "|---|---|---|---|---|---|---|"]
    fails, misses, records = [], [], []
    for k, (name, family, desc) in enumerate(RELATIONS, 1):
        r = by_base[best].get(name) or first.get(name)
        fn = f"{k:02d}_{name}.musicxml"
        A, B = Motif.from_json(r["A"]), Motif.from_json(r["B"])
        a, b = read(EXAMPLES / fn, A)
        ok, what = check(name, a, b, A)
        lo, hi = min(midis(b)), max(midis(b))
        acc = off_key(b, A.mode)
        acc_txt = "none" if not acc else ", ".join(f"{'#' if s > 0 else 'b'}{(L % 7) + 1}" for L, s in acc)
        prof = model.profile(pair_code(codes([A]), codes([B])))[0]
        order = np.argsort(-prof)
        rank = int(np.where(order == NAMES.index(name))[0][0]) + 1
        top = NAMES[order[0]]
        rng_txt = f"{lo}-{hi}" + ("" if CLARINET[0] <= lo and hi <= CLARINET[1] else " (outside the stimuli's range)")
        lines.append(f"| `{fn}` | {name} | {'pass' if ok else '**FAIL**'}: {what} | {rng_txt} | {acc_txt} | "
                     f"{top} ({prof[order[0]]:.2f}) | {prof[NAMES.index(name)]:.2f}, {rank} |")
        records.append({"file": fn, "relation": name, "family": family, "description": desc, "ok": bool(ok),
                        "check": what, "b_range": [int(lo), int(hi)], "accidentals": acc_txt, "model_top": top,
                        "model_top_p": round(float(prof[order[0]]), 3), "p": round(float(prof[NAMES.index(name)]), 3),
                        "rank": rank, "mode": A.mode, "meter": A.meter, "a_span": A.span, "bar": A.bar,
                        "b_span": B.span, "src_a": A.src})
        if not ok:
            fails.append(name)
        if rank != 1:
            misses.append((name, top, rank))
        print(f"{fn:28s} {'ok  ' if ok else 'FAIL'} model top {top} ({prof[order[0]]:.2f}), {name} rank {rank}  "
              f"[{A.mode}, {A.meter}, src {A.src}]")
    lines += ["", f"**{len(RELATIONS) - len(fails)}/{len(RELATIONS)} examples pass their definition check; "
                  f"the model ranks the illustrated relation first for {len(RELATIONS) - len(misses)}/{len(RELATIONS)}.**", ""]
    if misses:
        lines += ["Where the model's first choice differs:", ""]
        lines += [f"- `{n}`: the model prefers `{t}` (this relation ranks {k})." for n, t, k in misses]
        lines.append("")
    lines += ["Accidentals are scale degrees altered against the key (#7 = raised 7th). B's range is in MIDI note "
              "numbers; the stimuli's melodies stay within 50-94."]
    (EXAMPLES / "AUDIT.md").write_text("\n".join(lines) + "\n")
    (EXAMPLES / "audit.json").write_text(json.dumps(records, indent=1) + "\n")
    print(f"{len(fails)} definition failures; model misses: {misses}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
