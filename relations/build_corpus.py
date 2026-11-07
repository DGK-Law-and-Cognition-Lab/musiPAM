"""Step 1: cut the folk-tune collections bundled with music21 into two-bar motifs.

    ~/.venvs/musipam/bin/python build_corpus.py          # all four collections, ~5 minutes

Writes motifs.jsonl, one motif per line, to the data folder (~/musipam-data/relations,
or $MUSIPAM_REL_DATA). The tunes come from the music21 corpus and are not
redistributed, so the data folder stays outside Google Drive and git.

A tune is used only if it is a single melody line with one key and one meter.
A two-bar window becomes a motif if it starts with a note on the downbeat,
has 4-16 notes, spans at most an octave and a half, and is diatonic. In minor,
raised 6th and 7th degrees are also allowed.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from music21 import converter, corpus, key, meter, note, stream  # noqa: E402

from musipam_rel.motif import EPS, SCALES, Motif, alteration, height  # noqa: E402
from musipam_rel.paths import DATA  # noqa: E402

COLLECTIONS = {"essen": "essenFolksong", "oneills": "oneills1850", "aird": "airdsAirs", "ryan": "ryansMammoth"}


def tunes(path: str):
    s = converter.parse(path)
    yield from (s.scores if isinstance(s, stream.Opus) else [s])


def tune_motifs(sc: stream.Score, src: str) -> list[Motif]:
    if len(sc.parts) > 1:
        return []
    part = sc.parts[0] if len(sc.parts) else sc
    keys = list(part.recurse().getElementsByClass(key.Key))
    if not keys:
        sigs = list(part.recurse().getElementsByClass(key.KeySignature))
        if not sigs:
            return []
        keys = [sigs[0].asKey("major")]
    if len({str(k) for k in keys}) > 1:
        return []
    k = keys[0]
    tss = list(part.recurse().getElementsByClass(meter.TimeSignature))
    if not tss or len({t.ratioString for t in tss}) > 1 or k.mode not in SCALES:
        return []
    ts, mode = tss[0], k.mode
    bar = float(ts.barDuration.quarterLength)
    t_step, t_pc = k.tonic.step, k.tonic.pitchClass

    # notes with absolute offsets; tied notes merged
    events: list[list] = []  # [onset, dur, height, pc]
    for el in part.flatten().notesAndRests:
        if isinstance(el, note.Rest):
            continue
        if not isinstance(el, note.Note):
            return []  # a chord: not a single melody line
        if el.quarterLength <= 0:
            continue  # grace note
        on, d = float(el.offset), float(el.quarterLength)
        if el.tie is not None and el.tie.type in ("stop", "continue") and events \
                and events[-1][3] == el.pitch.pitchClass and abs(events[-1][0] + events[-1][1] - on) < EPS:
            events[-1][1] += d
            continue
        x = height(el.pitch.step, el.pitch.octave, t_step)
        events.append([on, d, x, el.pitch.pitchClass])

    measures = list(part.getElementsByClass(stream.Measure))
    full = [m for m in measures if abs(float(m.duration.quarterLength) - bar) < EPS]
    out, i = [], 0
    while i + 1 < len(full):
        m1, m2 = full[i], full[i + 1]
        start = float(m1.offset)
        if abs(float(m2.offset) - (start + bar)) > EPS:
            i += 1
            continue
        end = start + 2 * bar
        win = [e for e in events if start - EPS <= e[0] < end - EPS]
        i += 2
        if not win or abs(win[0][0] - start) > EPS or not 4 <= len(win) <= 16:
            continue
        h = [e[2] for e in win]
        alt = [alteration(e[2], e[3], t_pc, mode) for e in win]
        ok_alt = all(a == 0 or (mode == "minor" and a == 1 and x % 7 in (5, 6)) for x, a in zip(h, alt))
        if not ok_alt or max(h) - min(h) > 10:
            continue
        on = [e[0] - start for e in win]
        dur = [min(e[1], end - e[0]) for e in win]
        out.append(Motif(h, alt, on, dur, 2 * bar, bar, ts.ratioString, mode,
                         src=f"{src}/{int(m1.number) if m1.number is not None else i}"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DATA / "motifs.jsonl"))
    ap.add_argument("--max-files", type=int, default=0, help="per collection, for a quick test")
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    n_tunes, n_motifs, t0 = {}, {}, time.time()
    with out.open("w") as f:
        for name, folder in COLLECTIONS.items():
            paths = sorted(str(p) for p in corpus.getCorePaths() if f"/{folder}/" in str(p))
            if args.max_files:
                paths = paths[:args.max_files]
            for path in paths:
                stem = Path(path).stem
                try:
                    scores = list(tunes(path))
                except Exception as e:  # a few corpus files don't parse; skip them
                    print(f"  skip {name}/{stem}: {type(e).__name__}", flush=True)
                    continue
                for ti, sc in enumerate(scores):
                    n_tunes[name] = n_tunes.get(name, 0) + 1
                    try:
                        ms = tune_motifs(sc, f"{name}/{stem}/{ti}")
                    except Exception:
                        continue
                    for m in ms:
                        f.write(json.dumps(m.to_json()) + "\n")
                    n_motifs[name] = n_motifs.get(name, 0) + len(ms)
            print(f"{name}: {n_tunes.get(name, 0)} tunes -> {n_motifs.get(name, 0)} motifs ({time.time() - t0:.0f} s)",
                  flush=True)
    print(f"{sum(n_motifs.values())} motifs -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
