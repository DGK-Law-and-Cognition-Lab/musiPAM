"""Run PAM (Lu, Ichien & Holyoak, 2022) on the musiPAM stimuli.

    ~/.venvs/musipam/bin/python run_pam.py

Uses the Python port in pam.py, which validate.py checks against the lab's MATLAB
original. For each combination of node code and edge code, and for a range of node
weights (PAM's objweight, alpha in the paper: 0 = relations only; larger = more weight
on motif similarity), it maps:

    cross      the 8 designed cross-mappings: where does the probe go?
    variation  each theme onto its 8 symbolic variations: are the motifs mapped onto their own transformed selves?
    pairs      all 120 theme pairs: does PAM's analogy score separate same-skeleton analogs from controls?

Writes reports/pam_check.md and .json.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pam import attributes, pam  # noqa: E402
from problems import VARIATIONS, class_ok, edges, labels, nodes, problem_sets  # noqa: E402

WEIGHTS = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0]
COMBOS = [("rel", "computed"), ("rel", "computed_std"), ("rel", "learned"), ("rel", "learned_p5"),
          ("abs", "computed_std"), ("mert", "computed_std"), ("mert", "learned_p5")]
NAMES = {"rel": "key-relative motifs", "abs": "absolute-pitch motifs", "mert": "MERT motifs",
         "computed": "computed relations (raw)", "computed_std": "computed relations (standardized)",
         "learned": "learned relations", "learned_p5": "learned relations, 5th power"}


def auc(pos, neg) -> float:
    pos, neg = np.asarray(pos), np.asarray(neg)
    return float(((pos[:, None] > neg[None, :]).sum() + 0.5 * (pos[:, None] == neg[None, :]).sum()) / (len(pos) * len(neg)))


def run_combo(sets, node_code, edge_code) -> dict:
    cache = {}

    def attr(key):
        if key not in cache:
            cache[key] = attributes(nodes(key, node_code), edges(key, edge_code))
        return cache[key]

    res = {"cross": {}, "variation": {}, "pairs": {}}
    for p in sets["cross"]:
        lb = labels(p["B"])
        rows = []
        for ow in WEIGHTS:
            M, _ = pam(attr(p["A"]), attr(p["B"]), objweight=ow)
            k = int(M[p["probe"]].argmax())
            rows.append({"w": ow, "lands": lb[k], "p": round(float(M[p["probe"], k]), 3),
                         "kind": "role" if k == p["role"] else "look-alike" if k in p["look"] else "other"})
        res["cross"][p["name"]] = rows
    for p in sets["variation"]:
        res["variation"][p["name"]] = [class_ok(p, list(pam(attr(p["A"]), attr(p["B"]), objweight=ow)[0].argmax(1)))
                                       for ow in WEIGHTS]
    for ow in WEIGHTS:
        an, ct, role = [], [], 0
        for p in sets["pairs"]:
            M, s = pam(attr(p["A"]), attr(p["B"]), objweight=ow)
            (an if p["analog"] else ct).append(s["score"])
            role += p["analog"] and list(M.argmax(1)) == list(range(M.shape[0]))
        res["pairs"][str(ow)] = {"auc": auc(an, ct), "role_aligned": int(role), "n_analog": len(an)}
    return res


def summarize(res) -> dict:
    cross = res["cross"]
    works = {k: (rows[0]["kind"] == "role", any(r["kind"] == "look-alike" for r in rows)) for k, rows in cross.items()}
    var = {c: [sum(v[i] for k, v in res["variation"].items() if k.endswith(">" + c)) for i in range(len(WEIGHTS))]
           for c in VARIATIONS}
    return {"cross_role_at_0": sum(a for a, _ in works.values()),
            "cross_full": sum(a and b for a, b in works.values()),
            "variation": var}


def main() -> int:
    t0 = time.time()
    sets = problem_sets()
    out = {}
    for node_code, edge_code in COMBOS:
        if node_code == "mert" and not nodes(("T1", "identity"), "mert"):
            continue
        key = f"{node_code}+{edge_code}"
        out[key] = run_combo(sets, node_code, edge_code)
        out[key]["summary"] = summarize(out[key])
        s, pr = out[key]["summary"], out[key]["pairs"]
        print(f"{key:22s} cross: role with relations only {s['cross_role_at_0']}/8, full crossover {s['cross_full']}/8 | "
              f"pairs AUC at w=1: {pr['1.0']['auc']:.0%} ({time.time() - t0:.0f} s)", flush=True)
    (HERE / "reports").mkdir(exist_ok=True)
    (HERE / "reports" / "pam_check.json").write_text(json.dumps({"weights": WEIGHTS, "results": out}, indent=1))
    _report(out, HERE / "reports" / "pam_check.md")
    return 0


def _report(out: dict, path: Path) -> None:
    wl = " | ".join(f"α = {w:g}" for w in WEIGHTS)
    L = ["# PAM on the musiPAM stimuli", "",
         "PAM is the lab's model (Lu, Ichien & Holyoak, 2022), run through a Python port of `TestMapping_PAMfunc.m` "
         "that matches the MATLAB original to machine precision (`validate.py`). α is PAM's node weight "
         "(`objweight`): α = 0 maps by relations only; larger α gives motif similarity more weight. "
         "The paper used α = 0.1 for word triplets, 1 for texts, and 2 vs 1 for younger vs older children.", "",
         "## Summary", "",
         "| Node code | Edge code | Cross-mappings: role match with relations only | Cross-mappings: look-alike at higher α too | "
         "Analogs vs controls (AUC of the analogy score, α = 0 / 1 / 4) | Analogs mapped by role (α = 0 / 1 / 4) |",
         "|---|---|---|---|---|---|"]
    for key, res in out.items():
        n, e = key.split("+")
        s, pr = res["summary"], res["pairs"]
        L.append(f"| {NAMES[n]} | {NAMES[e]} | {s['cross_role_at_0']}/8 | {s['cross_full']}/8 | "
                 f"{pr['0.0']['auc']:.0%} / {pr['1.0']['auc']:.0%} / {pr['4.0']['auc']:.0%} | "
                 f"{pr['0.0']['role_aligned']} / {pr['1.0']['role_aligned']} / {pr['4.0']['role_aligned']} of 24 |")
    for key, res in out.items():
        n, e = key.split("+")
        L += ["", f"## {NAMES[n]}, {NAMES[e]}", "", "**Cross-mappings: where the probe lands** "
              "(role = the motif in the probe's role; look-alike = the designed copy of its shape)", "",
              f"| Pair | {wl} |", "|---|" + "---|" * len(WEIGHTS)]
        for name, rows in res["cross"].items():
            L.append(f"| {name.replace('>', ' → ')} | " + " | ".join(
                f"{r['lands'].replace(chr(39) * 2, '″').replace(chr(39), '′')} ({r['kind']})" for r in rows) + " |")
        L += ["", "**Theme → variation: themes (of 16) mapped correctly**", "",
              f"| Condition | {wl} |", "|---|" + "---|" * len(WEIGHTS)]
        for c, counts in res["summary"]["variation"].items():
            L.append(f"| {c} | " + " | ".join(str(x) for x in counts) + " |")
    path.write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
