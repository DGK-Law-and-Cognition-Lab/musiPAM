"""Step 2: generate labeled motif pairs from the corpus motifs.

    ~/.venvs/musipam/bin/python build_pairs.py

Splits are by tune, so no tune contributes to two splits:

    train      80% of the Essen tunes
    test_in    the other 20% of the Essen tunes (new tunes, same collection)
    test_out   the Irish and Scottish collections: O'Neill, Aird, Ryan (a new collection)

Each base motif gets one pair per applicable relation. Relations that borrow
material (a new rhythm, a new ending, an unrelated motif) take it from another
tune in the same split. If two relations turn the same A into the same B, both
pairs are dropped as ambiguous. The 704 motifs of the musiPAM stimuli, and any
corpus motif with the same steps and rhythm as one of them, never enter.

The test splits also get:

    compositions  two relations applied in sequence, never seen in training
    natural       pairs of two-bar windows from the same tune that stand in an exact
                  relation (repeat, sequence, octave, kept opening or ending,
                  consequent), found by searching real tunes rather than made by the generator
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import zlib
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from musipam_rel.motif import EPS, Motif, musipam_motifs  # noqa: E402
from musipam_rel.paths import DATA, STIMULI  # noqa: E402
from musipam_rel.relations import (COMPOSITIONS, NAMES, bars, canonical_minor, compose,  # noqa: E402
                                   donor_pool, make, take)


def split_of(m: Motif) -> str:
    coll = m.src.split("/", 1)[0]
    if coll != "essen":
        return "test_out"
    return "train" if zlib.crc32(m.tune().encode()) % 100 < 80 else "test_in"


def natural_relation(A: Motif, B: Motif) -> str | None:
    """The relation between two windows of one tune, if it is one the inventory names exactly."""
    A, B = canonical_minor(A), canonical_minor(B)
    if abs(A.bar - B.bar) > EPS or abs(A.span - B.span) > EPS:
        return None
    rnd = lambda xs: [round(x, 4) for x in xs]  # noqa: E731
    if A.n == B.n and rnd(A.on) == rnd(B.on) and rnd(A.dur) == rnd(B.dur):
        if A.signature() == B.signature():
            return "repeat"
        dh = {b - a for a, b in zip(A.h, B.h)}
        if len(dh) == 1:
            k = dh.pop()
            if abs(k) == 7:
                return "octave_up" if k > 0 else "octave_down"
            if 1 <= abs(k) <= 3:
                return f"seq_{'up' if k > 0 else 'down'}_{abs(k)}"
    ba, bb = bars(A), bars(B)
    if ba and bb:
        A1, B1, A2, B2 = take(A, ba[0]), take(B, bb[0]), take(A, ba[1]), take(B, bb[1])
        A1, B1, A2, B2 = ([v[0], rnd(v[1]), rnd(v[2])] for v in (A1, B1, A2, B2))
        if A1 == B1 and A2 != B2:
            if A.h[-1] % 7 != 0 and B.h[-1] % 7 == 0:
                return "consequent"
            if B.h[-1] % 7 != 0:
                return "opening_kept"
        if A2 == B2 and A1 != B1:
            return "ending_kept"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--motifs", default=str(DATA / "motifs.jsonl"))
    ap.add_argument("--n-train", type=int, default=4000, help="base motifs in train")
    ap.add_argument("--n-test", type=int, default=1000, help="base motifs in each test split")
    ap.add_argument("--n-compositions", type=int, default=300, help="base motifs per test split")
    ap.add_argument("--seed", type=int, default=2026)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    motifs = [Motif.from_json(json.loads(line)) for line in open(args.motifs)]
    held_out = {m.shape() for ms in musipam_motifs(STIMULI).values() for m in ms}
    kept = [m for m in motifs if m.shape() not in held_out]
    print(f"{len(motifs)} corpus motifs; {len(motifs) - len(kept)} share steps and rhythm with a musiPAM motif "
          f"and are excluded")

    by_split: dict[str, list[Motif]] = defaultdict(list)
    for m in kept:
        by_split[split_of(m)].append(m)
    n_base = {"train": args.n_train, "test_in": args.n_test, "test_out": args.n_test}
    DATA.mkdir(parents=True, exist_ok=True)
    summary = {}
    for split, ms in by_split.items():
        pool = donor_pool(ms)
        bases = ms[:]
        rng.shuffle(bases)
        bases = bases[:n_base[split]]
        counts, dropped = Counter(), 0
        with open(DATA / f"pairs_{split}.jsonl", "w") as f:
            for bi, A in enumerate(bases):
                outs = {name: r for name in NAMES if (r := make(name, A, rng, pool)) is not None}
                sigs = Counter(r[1].signature() for name, r in outs.items() if name != "reduction")
                for name, (a, b, params) in outs.items():
                    if name != "reduction" and sigs[b.signature()] > 1:
                        dropped += 1
                        continue
                    counts[name] += 1
                    f.write(json.dumps({"split": split, "base": bi, "label": name, "params": params,
                                        "A": a.to_json(), "B": b.to_json()}) + "\n")
        summary[split] = {"bases": len(bases), "pairs": sum(counts.values()), "ambiguous_dropped": dropped,
                          "per_relation": dict(counts)}
        print(f"{split}: {len(bases)} base motifs -> {sum(counts.values())} pairs ({dropped} ambiguous dropped)")

        if split == "train":
            continue
        with open(DATA / f"compositions_{split}.jsonl", "w") as f:
            nc = 0
            for bi, A in enumerate(bases[:args.n_compositions]):
                for names in COMPOSITIONS:
                    r = compose(names, A, rng, pool)
                    if r is not None:
                        f.write(json.dumps({"split": split, "base": bi, "label": "+".join(names),
                                            "components": list(names), "A": r[0].to_json(), "B": r[1].to_json()}) + "\n")
                        nc += 1
        tunes: dict[str, list[Motif]] = defaultdict(list)
        for m in ms:
            tunes[m.tune()].append(m)
        nat = Counter()
        with open(DATA / f"natural_{split}.jsonl", "w") as f:
            for tune, ws in tunes.items():
                ws.sort(key=lambda m: int(m.src.rsplit("/", 1)[1]))
                for i in range(len(ws)):
                    for j in range(i + 1, len(ws)):
                        lab = natural_relation(ws[i], ws[j])
                        if lab is None or nat[lab] >= 400:
                            continue
                        nat[lab] += 1
                        f.write(json.dumps({"split": split, "base": -1, "label": lab, "tune": tune,
                                            "A": canonical_minor(ws[i]).to_json(),
                                            "B": canonical_minor(ws[j]).to_json()}) + "\n")
        summary[split]["compositions"] = nc
        summary[split]["natural"] = dict(nat)
        print(f"  {nc} composition pairs; natural pairs: {dict(nat)}")
    (DATA / "pairs_summary.json").write_text(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
