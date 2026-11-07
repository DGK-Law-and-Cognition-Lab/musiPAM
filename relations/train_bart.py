"""Step 3 (Track A): fit the BART-style relation model on the symbolic motif code, and test it.

    ~/.venvs/musipam/bin/python train_bart.py

Writes the model to the data folder (models/bart_symbolic.npz) and the results
to reports/track_a_symbolic.md and .json. The tests:

1. Relation recognition on new tunes (test_in) and on a new collection (test_out).
2. Four-term analogies: given A -> B, pick which of four C -> D pairs is related the
   same way. Compared with two untrained baselines: raw differences between motif
   codes (B - A, the symbolic counterpart of MERT difference vectors) and the raw pair code.
3. Leak check: a model that sees only A, the base motif, should be close to chance.
   It can beat chance a little only because some relations can't be applied to some motifs.
4. Natural relations: pairs found in real tunes, not made by the generator.
5. Compositions: two relations applied in sequence, never seen in training. Are both
   components among the model's top choices?
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from musipam_rel.bart import RelationModel, analogy_accuracy, auc, cosine_rows  # noqa: E402
from musipam_rel.features import DIM, codes, pair_code  # noqa: E402
from musipam_rel.motif import Motif  # noqa: E402
from musipam_rel.paths import DATA, MODELS, REPORTS  # noqa: E402
from musipam_rel.relations import INDEX, NAMES, RELATIONS  # noqa: E402

FAMILY = {n: f for n, f, _ in RELATIONS}


def load(path: Path):
    rows = [json.loads(line) for line in open(path)]
    A = codes([Motif.from_json(r["A"]) for r in rows])
    B = codes([Motif.from_json(r["B"]) for r in rows])
    return rows, A, B


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--l2", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    t0 = time.time()

    rows, A, B = load(DATA / "pairs_train.jsonl")
    y = np.array([INDEX[r["label"]] for r in rows])
    X = pair_code(A, B)
    print(f"train: {len(y)} pairs, {X.shape[1]} features ({DIM} per motif)", flush=True)
    model = RelationModel(NAMES, l2=args.l2).fit(X, y)
    print(f"  fitted in {time.time() - t0:.0f} s: {model.fit_info}", flush=True)
    MODELS.mkdir(parents=True, exist_ok=True)
    model.save(MODELS / "bart_symbolic.npz")
    a_only = RelationModel(NAMES, l2=args.l2).fit(A, y)          # leak check
    d_mu, d_sd = (B - A).mean(0), (B - A).std(0) + 1e-6           # baseline: standardized raw differences
    p_mu, p_sd = X.mean(0), X.std(0) + 1e-6                        # baseline: standardized raw pair code

    out = {"train": {"pairs": int(len(y)), "fit": model.fit_info, "l2": args.l2}}
    for split in ("test_in", "test_out"):
        rows, A, B = load(DATA / f"pairs_{split}.jsonl")
        y = np.array([INDEX[r["label"]] for r in rows])
        base = np.array([r["base"] for r in rows])
        X = pair_code(A, B)
        R = model.profile(X)
        pred = R.argmax(1)
        res = {"pairs": int(len(y)), "accuracy": float((pred == y).mean()),
               "top3": float(np.mean([y[i] in np.argsort(-R[i])[:3] for i in range(len(y))])),
               "a_only_accuracy": float((a_only.profile(A).argmax(1) == y).mean()),
               "chance": 1 / len(NAMES)}
        res["per_relation"] = {
            n: {"n": int((y == k).sum()), "recall": float((pred[y == k] == k).mean()) if (y == k).any() else None,
                "auc": auc(R[:, k], y == k)} for k, n in enumerate(NAMES)}
        conf = {}
        for k, j in zip(y, pred):
            if k != j:
                conf[(NAMES[k], NAMES[j])] = conf.get((NAMES[k], NAMES[j]), 0) + 1
        res["top_confusions"] = [[a, b, c] for (a, b), c in sorted(conf.items(), key=lambda kv: -kv[1])[:8]]
        res["analogy"] = {
            "learned_profiles": analogy_accuracy(R, y, base, rng),
            "raw_differences": analogy_accuracy((B - A - d_mu) / d_sd, y, base, rng),
            "raw_pair_code": analogy_accuracy((X - p_mu) / p_sd, y, base, rng),
            "chance": 0.25}

        nat_rows, nA, nB = load(DATA / f"natural_{split}.jsonl")
        if nat_rows:
            ny = np.array([INDEX[r["label"]] for r in nat_rows])
            nR = model.profile(pair_code(nA, nB))
            npred = nR.argmax(1)
            res["natural"] = {"pairs": int(len(ny)), "accuracy": float((npred == ny).mean()),
                              "per_relation": {NAMES[k]: {"n": int((ny == k).sum()),
                                                          "recall": float((npred[ny == k] == k).mean())}
                                               for k in sorted(set(ny.tolist()))}}
        comp_rows, cA, cB = load(DATA / f"compositions_{split}.jsonl")
        if comp_rows:
            cR = model.profile(pair_code(cA, cB))
            comp = {}
            for r, prof in zip(comp_rows, cR):
                ks = [INDEX[c] for c in r["components"]]
                order = list(np.argsort(-prof))
                c = comp.setdefault(r["label"], {"n": 0, "both_in_top2": 0, "both_in_top3": 0, "one_in_top1": 0})
                c["n"] += 1
                c["both_in_top2"] += int(all(k in order[:2] for k in ks))
                c["both_in_top3"] += int(all(k in order[:3] for k in ks))
                c["one_in_top1"] += int(order[0] in ks)
            res["compositions"] = {k: {m: (v[m] / v["n"] if m != "n" else v["n"]) for m in v} for k, v in comp.items()}
        out[split] = res
        print(f"{split}: accuracy {res['accuracy']:.1%} (chance {res['chance']:.1%}, A only {res['a_only_accuracy']:.1%}); "
              f"analogies {res['analogy']['learned_profiles']:.1%} vs raw differences {res['analogy']['raw_differences']:.1%}",
              flush=True)

    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "track_a_symbolic.json").write_text(json.dumps(out, indent=1))
    _report(out, REPORTS / "track_a_symbolic.md")
    print(f"done in {time.time() - t0:.0f} s -> {REPORTS / 'track_a_symbolic.md'}")
    return 0


def _report(out: dict, path: Path) -> None:
    ti, to = out["test_in"], out["test_out"]
    pct = lambda x: "–" if x is None or x != x else f"{x:.0%}"  # noqa: E731
    L = ["# Track A: BART-style relation model on the symbolic motif code", "",
         "One regularized logistic classifier per relation on the pair code [a, b, b − a, |b − a|, a·b] of a "
         "generic symbolic motif code; a pair's relation vector is its profile of probabilities over the "
         f"{len(NAMES)} relations. Trained on {out['train']['pairs']:,} generated pairs from Essen tunes "
         "(see `build_pairs.py`).", "",
         "| Test | New tunes, same collection (Essen) | New collection (Irish and Scottish) |", "|---|---|---|",
         f"| Relation recognized (top choice) | {pct(ti['accuracy'])} | {pct(to['accuracy'])} |",
         f"| Correct relation among top 3 | {pct(ti['top3'])} | {pct(to['top3'])} |",
         f"| Leak check: model that sees only A | {pct(ti['a_only_accuracy'])} | {pct(to['a_only_accuracy'])} |",
         f"| Chance | {pct(ti['chance'])} | {pct(to['chance'])} |",
         f"| Four-term analogies, learned relation vectors | {pct(ti['analogy']['learned_profiles'])} | {pct(to['analogy']['learned_profiles'])} |",
         f"| Four-term analogies, raw motif-code differences (B − A) | {pct(ti['analogy']['raw_differences'])} | {pct(to['analogy']['raw_differences'])} |",
         f"| Four-term analogies, raw pair code | {pct(ti['analogy']['raw_pair_code'])} | {pct(to['analogy']['raw_pair_code'])} |",
         "| Four-term analogies, chance | 25% | 25% |"]
    for split, name in (("test_in", "new tunes"), ("test_out", "new collection")):
        nat = out[split].get("natural")
        if nat:
            L.append(f"| Natural relations found in real tunes ({name}): {nat['pairs']} pairs | "
                     + (f"{pct(nat['accuracy'])} | |" if split == "test_in" else f"| {pct(nat['accuracy'])} |"))
    L += ["", "## Per relation (recall of the top choice, and AUC of the relation's own probability)", "",
          "| Relation | Family | New tunes: recall | AUC | New collection: recall | AUC |", "|---|---|---|---|---|---|"]
    for n in NAMES:
        a, b = ti["per_relation"][n], to["per_relation"][n]
        L.append(f"| {n} | {FAMILY[n]} | {pct(a['recall'])} | {a['auc']:.2f} | {pct(b['recall'])} | {b['auc']:.2f} |")
    for split, name in (("test_in", "New tunes"), ("test_out", "New collection")):
        L += ["", f"## {name}: most frequent confusions (true → chosen, count)", ""]
        L += [f"- {a} → {b}: {c}" for a, b, c in out[split]["top_confusions"]]
        nat = out[split].get("natural")
        if nat:
            L += ["", f"**Natural relations ({name.lower()}):** " + "; ".join(
                f"{k} {pct(v['recall'])} (n = {v['n']})" for k, v in nat["per_relation"].items())]
        comp = out[split].get("compositions")
        if comp:
            L += ["", f"**Compositions ({name.lower()}, never seen in training):** " + "; ".join(
                f"{k}: both parts in top 2 {pct(v['both_in_top2'])}, in top 3 {pct(v['both_in_top3'])} (n = {v['n']})"
                for k, v in comp.items())]
    path.write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
