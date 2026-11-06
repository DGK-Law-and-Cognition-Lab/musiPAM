"""Learned motif embeddings (MERT) for every stimulus, and the design check
rerun with learned representations.

    ~/.venvs/musipam/bin/python -I embed.py

Needs the model extras (requirements-models.txt). Writes
stimuli/embeddings/mert_v1_95m.npz (+ .json metadata) and
stimuli/reports/design_check_mert.md.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import csv
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from musipam_stim import designcheck as dc  # noqa: E402
from musipam_stim import embeddings as E  # noqa: E402
from musipam_stim.themes import THEMES  # noqa: E402
from musipam_stim.transforms import CELL, TRANSFORMS  # noqa: E402

STIM = ROOT.parent / "stimuli"


def main() -> int:
    rows = list(csv.DictReader(open(STIM / "manifest.csv")))
    model, proc = E.load_mert()
    emb, graphs = {}, {}
    for r in rows:
        g = json.loads((STIM / r["graph"]).read_text())
        bpm = float(r["bpm"])
        x = E.load_mono_24k(STIM / r["wav"])
        layers = [E.embed_clip(model, proc, E.slice_motif(x, n["onset_ql"] * 60 / bpm + 0.1, n["dur_ql"] * 60 / bpm))
                  for n in g["nodes"]]
        emb[r["stim_id"]] = np.stack(layers)  # [motifs, layers, dim]
        for n, lay in zip(g["nodes"], layers):
            n["_mert"] = E.node_code(lay)
        graphs[(r["theme"], r["condition"])] = g
        print(f"  embedded {r['stim_id']}", flush=True)

    out = STIM / "embeddings"
    out.mkdir(exist_ok=True)
    npz = out / "mert_v1_95m.npz"
    np.savez_compressed(npz, **emb)
    shape = next(iter(emb.values())).shape
    (out / "mert_v1_95m.json").write_text(json.dumps({
        "model": E.MERT_MODEL, "revision": E.MERT_REVISION, "sample_rate": E.MERT_SR,
        "array": "per stimulus: [motif, layer, dim] time-pooled hidden states", "shape": list(shape),
        "slicing": "each motif cut from the stimulus WAV at its onset (manifest timing, incl. 0.1 s lead-in), "
                   f"{E.FADE_S * 1000:.0f} ms fades, embedded without context",
        "confirmatory_node_code": "mean over all layers, unit-normalized (embeddings.node_code)",
        "device": "cpu", "npz_sha256": hashlib.sha256(npz.read_bytes()).hexdigest(),
    }, indent=1))

    # learned relations: difference vectors between motif embeddings
    diff = {}
    for key, g in graphs.items():
        d = json.loads(json.dumps({k: v for k, v in g.items() if k != "nodes"}))
        d["nodes"] = g["nodes"]
        d["edges"] = [{"i": e["i"], "j": e["j"],
                       "r": (np.asarray(g["nodes"][e["j"]]["_mert"]) - np.asarray(g["nodes"][e["i"]]["_mert"])).tolist()}
                      for e in g["edges"]]
        diff[key] = d
    _report(graphs, diff, STIM / "reports" / "design_check_mert.md")
    print(f"{len(emb)} stimuli embedded -> {npz.name}")
    return 0


def _report(graphs, diff, path: Path) -> None:
    W = dc.W_LEVELS
    hdr = "| condition | grid cell | " + " | ".join(f"w={w:g}" for w in W) + " |"
    sep = "|---|---|" + "---|" * len(W)
    variants = (("MERT motifs + computed relations", graphs, dc.relation_norm(graphs.values())),
                ("MERT motifs + MERT difference-vector relations (fully learned)", diff, dc.relation_norm(diff.values())))
    L = ["# Design check with learned representations (MERT-v1-95M)", "",
         "Same exact matcher as design_check.md (a proxy, not PAM), with motif nodes coded by MERT embeddings "
         "of the audio participants hear. Unlike the symbolic codes, MERT also sees timbre and tempo, so those "
         "conditions are included. ✓ = the theme's motifs map onto their own transformed selves "
         "(identical a1/a2 count as one class); the label is where the theme's first motif landed.", ""]
    for title, G, norm in variants:
        L += [f"## {title}", ""]
        for tid in THEMES:
            base = G[(tid, "identity")]
            L += [f"**{tid}**", "", hdr, sep]
            for cond in TRANSFORMS:
                if cond == "identity":
                    continue
                gB = G[(tid, cond)]
                r = dc.evaluate(base, gB, dc.truth_by_source(base, gB), "mert", norm)
                L.append(f"| {cond} | {CELL[cond]} | " + " | ".join(
                    ("✓ " if r["rows"][w]["class_ok"] else "✗ ") + r["rows"][w]["a_maps_to"] for w in W) + " |")
            L.append("")
        L += ["**Cross-theme analogs** (label = where the cross-mapped source motif landed)", "", hdr.replace("condition", "pair"), sep]
        for src, dst, probe in (("T1", "T3", 0), ("T2", "T4", 1)):
            r = dc.evaluate(G[(src, "identity")], G[(dst, "identity")], (0, 1, 2, 3), "mert", norm)
            lb = r["labels_B"]
            L.append(f"| {src} → {dst} | {r['labels_A'][probe]} → ? | " + " | ".join(
                ("✓ " if r["rows"][w]["class_ok"] else "✗ ") + lb[r["rows"][w]["perm"][probe]] for w in W) + " |")
        L += ["", "**Relational similarity between themes** (role alignment / best of 24)", "",
              "| pair | kind | role | best | best is role |", "|---|---|---|---|---|"]
        tids = list(THEMES)
        for i, a in enumerate(tids):
            for b in tids[i + 1:]:
                m = dc.match(G[(a, "identity")], G[(b, "identity")], "mert", norm)
                bp = max(m["scores"], key=lambda p: m["scores"][p][1])
                kind = "**analog**" if (a, b) in {("T1", "T3"), ("T2", "T4")} else "different skeleton"
                L.append(f"| {a} → {b} | {kind} | {m['scores'][(0, 1, 2, 3)][1]:.2f} | {m['scores'][bp][1]:.2f} | "
                         f"{'yes' if bp == (0, 1, 2, 3) else 'no'} |")
        L.append("")
    path.write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
