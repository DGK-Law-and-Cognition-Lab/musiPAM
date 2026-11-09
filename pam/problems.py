"""musiPAM mapping problems for PAM: the stimulus graphs, coded several ways.

Node codes (motif attributes):
    rel    key-relative contour, rhythm and pitch-class profile (stimgen's symbolic code)
    abs    blurred piano roll plus absolute pitch classes
    mert   MERT-v1-95M audio embedding (layer mean, unit length), if stimgen/embed.py has been run

Edge codes (relation attributes):
    computed      stimgen's 16 hand-built relation features, raw
    computed_std  the same, standardized per dimension over all 176 stimuli
    learned       the music-BART relation profile (26 relations) plus the 3 positional features
    learned_p5    the same with the profile raised to the 5th power, as PAM does with BART vectors

Problems:
    cross      the 8 designed cross-mappings (theme -> its analog)
    variation  each theme -> each of its 8 symbolic variations (transpose ... retrograde)
    pairs      all 120 pairs of themes, for analog-versus-control analogy scores
"""
from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

import numpy as np

V2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(V2 / "stimgen"))
sys.path.insert(0, str(V2 / "relations"))
sys.dont_write_bytecode = True

from musipam_stim import designcheck as dc  # noqa: E402
from musipam_stim.graphs import node_vector, stim_graph  # noqa: E402
from musipam_stim.themes import CROSS_MAPPINGS, THEMES, analog_pairs, theme_stim  # noqa: E402
from musipam_stim.transforms import TRANSFORMS  # noqa: E402

VARIATIONS = ["transpose", "mode", "ornament", "augment", "reorder", "motif_retro", "invert", "retrograde"]
LOOK = {("T2", "T4"): [0, 2], ("T7", "T8"): [1, 3], ("T15", "T16"): [0, 1, 2]}


@lru_cache(maxsize=1)
def graphs() -> dict:
    """In-memory graphs of all 176 stimuli, keyed (theme, condition)."""
    out = {}
    for tid in THEMES:
        ident = theme_stim(tid)
        for cond, fn in TRANSFORMS.items():
            out[(tid, cond)] = stim_graph(fn(ident))
    return out


@lru_cache(maxsize=1)
def _mert() -> dict:
    path = V2 / "stimuli" / "embeddings" / "mert_v1_95m.npz"
    if not path.exists():
        return {}
    z = np.load(path)
    out = {}
    for sid in z.files:
        v = z[sid].mean(1)  # [motif, layer, dim] -> [motif, dim]
        out[sid] = v / np.linalg.norm(v, axis=1, keepdims=True)
    return out


@lru_cache(maxsize=1)
def _learned() -> dict:
    """Music-BART relation profile for every directed motif pair of every stimulus, keyed (theme, condition)."""
    from musipam_rel.bart import RelationModel
    from musipam_rel.features import codes, pair_code
    from musipam_rel.motif import musipam_motifs
    from musipam_rel.paths import MODELS, STIMULI
    model = RelationModel.load(MODELS / "bart_symbolic.npz")
    mots = musipam_motifs(STIMULI)
    out = {}
    for (tid, cond), g in graphs().items():
        ms = mots[f"{tid}_{cond}"]
        labels = [m.src.split(":")[1] for m in ms]
        assert labels == [n["label"] for n in g["nodes"]], (tid, cond, labels)
        x = codes(ms)
        n = len(ms)
        out[(tid, cond)] = {(i, j): model.profile(pair_code(x[i][None], x[j][None]))[0]
                            for i in range(n) for j in range(n) if i != j}
    return out


@lru_cache(maxsize=1)
def _edge_norm():
    R = np.array([np.asarray(e["r"], float) for g in graphs().values() for e in g["edges"]])
    sd = R.std(0)
    sd[sd == 0] = 1.0
    return R.mean(0), sd


def nodes(key, code: str) -> list[np.ndarray]:
    g = graphs()[key]
    if code == "mert":
        return list(_mert()[f"{key[0]}_{key[1]}"])
    return [node_vector(n, code) for n in g["nodes"]]


def edges(key, code: str) -> dict:
    g = graphs()[key]
    comp = {(e["i"], e["j"]): np.asarray(e["r"], float) for e in g["edges"]}
    if code == "computed":
        return comp
    if code == "computed_std":
        mu, sd = _edge_norm()
        return {k: (v - mu) / sd for k, v in comp.items()}
    prof = _learned()[key]
    power = 5 if code == "learned_p5" else 1
    return {k: np.concatenate([prof[k] ** power, comp[k][:3]]) for k in comp}


def labels(key) -> list[str]:
    return [n["label"] for n in graphs()[key]["nodes"]]


def problem_sets() -> dict:
    cross = [{"name": f"{s}>{d}", "A": (s, "identity"), "B": (d, "identity"), "probe": si, "look": LOOK.get((s, d), [di]),
              "role": si} for s, si, d, di in CROSS_MAPPINGS]
    variation = []
    for tid in THEMES:
        base = graphs()[(tid, "identity")]
        for cond in VARIATIONS:
            gB = graphs()[(tid, cond)]
            variation.append({"name": f"{tid}>{cond}", "A": (tid, "identity"), "B": (tid, cond), "cond": cond,
                              "truth": dc.truth_by_source(base, gB)})
    analogs = set(analog_pairs())
    tids = list(THEMES)
    pairs = [{"name": f"{a}~{b}", "A": (a, "identity"), "B": (b, "identity"), "analog": (a, b) in analogs}
             for i, a in enumerate(tids) for b in tids[i + 1:]]
    return {"cross": cross, "variation": variation, "pairs": pairs}


def class_ok(prob: dict, perm: list[int]) -> bool:
    """Every source motif maps to its own transformed self (identical a1/a2 count as one class)."""
    la, lb = labels(prob["A"]), labels(prob["B"])
    return all(dc.content_class(lb[perm[i]]) == dc.content_class(lb[prob["truth"][i]]) for i in range(len(la)))
