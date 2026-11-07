"""Step 4: the learned relations in the musiPAM design check.

    ~/.venvs/musipam/bin/python apply_musipam.py

The relation model never saw a musiPAM motif. This step computes its relation
vector for every directed pair of motifs in each of the 176 stimuli and reruns
stimgen's design check with those edges in place of the computed ones.
Variants compared:

    computed            the 16 hand-built relation features (the current design)
    learned             the learned relation profile (26 relations)
    learned + order     the learned profile plus the 3 positional features (first, next, previous)
    raw differences     motif-code differences (B - A), the untrained baseline

Writes reports/musipam_learned_edges.md (+ .json) and reports/musipam_edge_profiles.csv,
the learned relation vector of every edge (to be frozen before a study is registered).
"""
from __future__ import annotations

import copy
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from musipam_rel.paths import MODELS, REPORTS, STIMGEN, STIMULI  # noqa: E402

sys.path.insert(0, str(STIMGEN))
from musipam_stim import designcheck as dc  # noqa: E402
from musipam_stim.themes import CROSS_MAPPINGS, THEMES, analog_pairs  # noqa: E402
from musipam_stim.transforms import TRANSFORMS  # noqa: E402

from musipam_rel.bart import RelationModel, auc  # noqa: E402
from musipam_rel.features import codes, pair_code  # noqa: E402
from musipam_rel.motif import musipam_motifs  # noqa: E402

W = dc.W_LEVELS
LOOK = {("T2", "T4"): [0, 2], ("T7", "T8"): [1, 3], ("T15", "T16"): [0, 1, 2]}
# designed relations inside each skeleton: (from, to) motif positions, and the relation a musician would name
DESIGNED = {
    "sentence": [((0, 1), "a → a′", "seq_up_1")],
    "period": [((0, 2), "a₁ → a₂", "repeat"), ((1, 3), "b → c", "consequent")],
    "rounded": [((0, 3), "a → a′", "consequent")],
    "chain": [((0, 1), "a → a′", "seq_down_1"), ((1, 2), "a′ → a″", "seq_down_1"), ((0, 2), "a → a″", "seq_down_2")],
}


def main() -> int:
    model = RelationModel.load(MODELS / "bart_symbolic.npz")
    names = model.names
    rows = list(csv.DictReader(open(STIMULI / "manifest.csv")))
    motifs = musipam_motifs(STIMULI)
    base = {(r["theme"], r["condition"]): json.loads((STIMULI / r["graph"]).read_text()) for r in rows}

    variants = {"computed": base}
    learned, ordered, raw = {}, {}, {}
    profiles_out = []
    for r in rows:
        key, sid = (r["theme"], r["condition"]), r["stim_id"]
        g = base[key]
        x = codes(motifs[sid])
        for v in (learned, ordered, raw):
            v[key] = copy.deepcopy(g)
        for e_l, e_o, e_r in zip(learned[key]["edges"], ordered[key]["edges"], raw[key]["edges"]):
            i, j = e_l["i"], e_l["j"]
            prof = model.profile(pair_code(x[i][None, :], x[j][None, :]))[0]
            e_l["r"] = prof.tolist()
            e_o["r"] = prof.tolist() + list(e_o["r"][:3])
            e_r["r"] = (x[j] - x[i]).tolist()
            profiles_out.append([sid, i, j, g["nodes"][i]["label"], g["nodes"][j]["label"]] + [round(float(p), 4) for p in prof])
    variants.update({"learned": learned, "learned + order": ordered, "raw differences": raw})

    results = {v: evaluate(G) for v, G in variants.items()}
    designed = designed_edges(learned, names)
    REPORTS.mkdir(parents=True, exist_ok=True)
    with open(REPORTS / "musipam_edge_profiles.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["stim_id", "from_pos", "to_pos", "from_motif", "to_motif"] + names)
        w.writerows(profiles_out)
    (REPORTS / "musipam_learned_edges.json").write_text(json.dumps({"variants": results, "designed": designed}, indent=1))
    _report(results, designed, REPORTS / "musipam_learned_edges.md")
    for v, res in results.items():
        print(f"{v:16s} cross-mappings {res['cross_working']}/8 | analogs vs controls AUC {res['relsim']['auc']:.0%}, "
              f"role best {res['relsim']['role_best']}/24")
    return 0


def evaluate(G: dict) -> dict:
    norm = dc.relation_norm(G.values())
    ident = {t: G[(t, "identity")] for t in THEMES}
    cross, working = {}, 0
    for src, si, dst, di in CROSS_MAPPINGS:
        r = dc.evaluate(ident[src], ident[dst], (0, 1, 2, 3), "rel", norm)
        land = [r["rows"][w]["perm"][si] for w in W]
        ok = [bool(r["rows"][w]["class_ok"]) for w in W]
        look = LOOK.get((src, dst), [di])
        works = land[0] in look and any(ok)
        working += works
        cross[f"{src}>{dst}"] = {"lands": [r["labels_B"][k] for k in land], "ok": ok, "works": works,
                                 "role_from": next((w for w, o in zip(W, ok) if o), None)}
    analogs, tids, rel = set(analog_pairs()), list(THEMES), []
    for i, a in enumerate(tids):
        for b in tids[i + 1:]:
            m = dc.match(ident[a], ident[b], "rel", norm)
            best = max(m["scores"], key=lambda p: m["scores"][p][1])
            rel.append(((a, b) in analogs, m["scores"][(0, 1, 2, 3)][1], best == (0, 1, 2, 3)))
    s = np.array([x[1] for x in rel])
    is_an = np.array([x[0] for x in rel])
    theme = {}
    for cond in TRANSFORMS:
        if cond in ("identity", "timbre", "tempo"):
            continue
        n_rel = n_any = 0
        for t in THEMES:
            gB = G[(t, cond)]
            r = dc.evaluate(ident[t], gB, dc.truth_by_source(ident[t], gB), "rel", norm)
            n_rel += bool(r["rows"][1.0]["class_ok"])
            n_any += any(r["rows"][w]["class_ok"] for w in W)
        theme[cond] = {"relations_only": n_rel, "any_weight": n_any}
    return {"cross": cross, "cross_working": int(working),
            "relsim": {"auc": auc(s, is_an), "analog_mean": float(s[is_an].mean()), "control_mean": float(s[~is_an].mean()),
                       "role_best": int(sum(x[2] for x in rel if x[0]))},
            "theme": theme}


def designed_edges(G: dict, names: list[str]) -> list[dict]:
    out = []
    for t, th in THEMES.items():
        g = G[(t, "identity")]
        edges = {(e["i"], e["j"]): np.asarray(e["r"]) for e in g["edges"]}
        for (i, j), label, expected in DESIGNED[th.skeleton]:
            prof = edges[(i, j)]
            order = np.argsort(-prof)
            out.append({"theme": t, "skeleton": th.skeleton, "edge": label, "expected": expected,
                        "top": names[order[0]], "p_top": float(prof[order[0]]), "second": names[order[1]],
                        "p_expected": float(prof[names.index(expected)]),
                        "rank_expected": int(list(order).index(names.index(expected)) + 1)})
    return out


def _report(results: dict, designed: list[dict], path: Path) -> None:
    pct = lambda x: f"{x:.0%}"  # noqa: E731
    wl = lambda w: "–" if w is None else f"{w:g}"  # noqa: E731
    L = ["# Learned relations in the musiPAM design check", "",
         "The relation model was trained only on generated pairs of folk-tune motifs (`train_bart.py`); it never "
         "saw a musiPAM motif. Here its relation vectors replace the hand-built edges of the 176 stimuli, and "
         "stimgen's design check is rerun (motif nodes stay on the key-relative code).", "",
         "## Does the model name the designed relations?", "",
         "For each theme, the relations its skeleton was built on, and what the model calls them.", "",
         "| Theme | Skeleton | Edge | Built as | Model's top relation (p) | Rank of the built relation |",
         "|---|---|---|---|---|---|"]
    for d in designed:
        L.append(f"| {d['theme']} | {d['skeleton']} | {d['edge']} | {d['expected']} | {d['top']} ({d['p_top']:.2f}) | "
                 f"{d['rank_expected']} |")
    n_top = sum(d["rank_expected"] == 1 for d in designed)
    L += ["", f"The built relation is the model's top choice for {n_top} of {len(designed)} designed edges.", "",
          "## The design check with each kind of edge", "",
          "| Edges | Cross-mappings that work | Role mapping wins from w = | Analogs vs controls (AUC) | "
          "Analog pairs aligned by role |", "|---|---|---|---|---|"]
    for v, res in results.items():
        froms = ", ".join(f"{k.replace('>', '→')} {wl(c['role_from'])}" for k, c in res["cross"].items())
        L.append(f"| {v} | {res['cross_working']}/8 | {froms} | {pct(res['relsim']['auc'])} | "
                 f"{res['relsim']['role_best']}/24 |")
    L += ["", "## Theme → variation: themes (of 16) whose mapping relations alone recover", "",
          "| Condition | " + " | ".join(results) + " |", "|---|" + "---|" * len(results)]
    for cond in next(iter(results.values()))["theme"]:
        L.append(f"| {cond} | " + " | ".join(str(res["theme"][cond]["relations_only"]) for res in results.values()) + " |")
    L += ["", "Motif-only matching (w = 0) is the same in every row, since only the edges change."]
    path.write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
