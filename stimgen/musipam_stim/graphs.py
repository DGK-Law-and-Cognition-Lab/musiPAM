"""Symbolic motif graphs: nodes = motifs, edges = computed relation vectors.

Two node codes are provided because the design separates them:

* ``rel``  key- and tempo-relative structure: pitch contour (time-normalized),
           scale-free rhythm, key-relative pitch-class profile.
* ``abs``  literal surface: a blurred piano roll on a fixed pitch/time grid
           plus an absolute pitch-class profile.

Edges are relation vectors for every ordered motif pair (i -> j), computed
from the score in the spirit of visiPAM's computed spatial relations. They
are a first symbolic implementation; a learned relation model (a "music
BART") is a later upgrade, not a prerequisite.
"""
from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter

from .theory import KeyInfo, tension
from .themes import Segment, Stim

N_CONTOUR = 16
N_RHYTHM = 48
PR_LO, PR_HI = 36, 96
PR_RES = 0.25
PR_MAX_QL = 16.0

RELATION_NAMES = [
    "d_position", "is_next", "is_prev", "d_mean_pitch", "d_first_step", "d_last_step",
    "contour_same", "contour_retro", "log2_dur_ratio", "rhythm_same", "rhythm_retro",
    "restatement", "tension_end_i", "tension_start_j", "d_tension", "junction",
]


def _unit(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def _cos(a, b) -> float:
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(a @ b / (na * nb)) if na > 0 and nb > 0 else 0.0


def _events(seg: Segment):
    t, out = 0.0, []
    for n in seg.notes:
        out.append((t, n.dur, n.p.midi, n.p.diatonicNoteNum))
        t += n.dur
    return out


def _sampled_pitch(ev, n=N_CONTOUR) -> np.ndarray:
    T = sum(d for _, d, _, _ in ev)
    vals = []
    for t in (np.arange(n) + 0.5) / n * T:
        vals.append(next(m for o, d, m, _ in ev if o - 1e-9 <= t < o + d - 1e-9))
    return np.array(vals, float)


def _onset_curve(xs, n=N_RHYTHM, sigma=1.0) -> np.ndarray:
    idx = np.arange(n)
    v = np.zeros(n)
    for x in xs:
        v += np.exp(-0.5 * ((idx - x * n) / sigma) ** 2)
    return v


def _piano_roll(ev) -> np.ndarray:
    rows, cols = PR_HI - PR_LO + 1, int(PR_MAX_QL / PR_RES)
    g = np.zeros((rows, cols))
    for o, d, m, _ in ev:
        r = min(max(m, PR_LO), PR_HI) - PR_LO
        g[r, int(round(o / PR_RES)):min(cols, int(round((o + d) / PR_RES)))] = 1.0
    return gaussian_filter(g, sigma=(1.0, 1.0)).ravel()


def node_features(s: Stim) -> list[dict]:
    ki = KeyInfo(s.k)
    nodes, t0 = [], 0.0
    for pos, seg in enumerate(s.segments):
        ev = _events(seg)
        T = seg.dur
        w = np.array([d for _, d, _, _ in ev])
        midi = np.array([m for _, _, m, _ in ev], float)
        sp = _sampled_pitch(ev)
        rel_chroma = np.zeros(12)
        abs_chroma = np.zeros(12)
        for (_, d, m, _) in ev:
            rel_chroma[(m - ki.tonic_pc) % 12] += d
            abs_chroma[m % 12] += d
        figs, spans, acc = [], [], 0.0
        for ch in seg.chords:
            figs.append(ch.fig)
            spans.append(ch.dur)
        tens = [tension(f) for f in figs]
        contour = (sp - sp.mean()) / 12.0
        rhythm = _onset_curve([o / T for o, _, _, _ in ev])
        retro_rhythm = _onset_curve([(T - o - d) / T for o, d, _, _ in ev])
        nodes.append({
            "pos": pos, "label": seg.label, "src": seg.src,
            "onset_ql": t0, "dur_ql": T, "n_notes": len(ev),
            "mean_midi": float((midi * w).sum() / w.sum()),
            "first_midi": int(midi[0]), "last_midi": int(midi[-1]),
            "first_step": int(ev[0][3] - ki.tonic_dnn4), "last_step": int(ev[-1][3] - ki.tonic_dnn4),
            "contour16": contour.round(5).tolist(),
            "rhythm48": rhythm.round(5).tolist(),
            "retro_rhythm48": retro_rhythm.round(5).tolist(),
            "rel_chroma12": (rel_chroma / rel_chroma.sum()).round(5).tolist(),
            "abs_chroma12": (abs_chroma / abs_chroma.sum()).round(5).tolist(),
            "harmony": figs,
            "tension_start": tens[0], "tension_end": tens[-1],
            "tension_mean": float(np.dot(tens, spans) / sum(spans)),
            "_piano_roll": _piano_roll(ev),
        })
        t0 += T
    return nodes


def node_vector(n: dict, code: str) -> np.ndarray:
    if code == "rel":
        blocks = [n["contour16"], n["rhythm48"], n["rel_chroma12"]]
    elif code == "abs":
        blocks = [n["_piano_roll"], n["abs_chroma12"]]
    elif code == "mert":  # learned audio embedding, attached by embed.py (already unit-normalized)
        return np.asarray(n["_mert"], float)
    else:
        raise ValueError(code)
    return np.concatenate([_unit(np.asarray(b, float)) for b in blocks]) / np.sqrt(len(blocks))


def relation_vector(ni: dict, nj: dict) -> np.ndarray:
    ci, cj = np.asarray(ni["contour16"]), np.asarray(nj["contour16"])
    return np.array([
        (nj["pos"] - ni["pos"]) / 3.0,
        float(nj["pos"] == ni["pos"] + 1),
        float(nj["pos"] == ni["pos"] - 1),
        (nj["mean_midi"] - ni["mean_midi"]) / 12.0,
        (nj["first_step"] - ni["first_step"]) / 7.0,
        (nj["last_step"] - ni["last_step"]) / 7.0,
        _cos(ci, cj),
        _cos(ci, cj[::-1]),
        float(np.log2(nj["dur_ql"] / ni["dur_ql"])),
        _cos(ni["rhythm48"], nj["rhythm48"]),
        _cos(ni["rhythm48"], nj["retro_rhythm48"]),
        _cos(node_vector(ni, "rel"), node_vector(nj, "rel")),
        ni["tension_end"],
        nj["tension_start"],
        nj["tension_mean"] - ni["tension_mean"],
        (nj["first_midi"] - ni["last_midi"]) / 12.0,
    ])


def stim_graph(s: Stim) -> dict:
    nodes = node_features(s)
    edges = []
    for i, ni in enumerate(nodes):
        for j, nj in enumerate(nodes):
            if i != j:
                edges.append({"i": i, "j": j, "r": relation_vector(ni, nj).round(5).tolist()})
    return {"nodes": nodes, "edges": edges}


def graph_json(s: Stim, g: dict) -> dict:
    """JSON-safe export (drops the piano-roll arrays, which are recomputable)."""
    return {
        "stim_id": s.stim_id, "theme": s.theme_id, "condition": s.condition,
        "key": f"{s.k.tonic.name} {s.k.mode}", "meter": s.meter, "bpm": s.bpm,
        "node_codes": {"rel": "contour16 + rhythm48 + rel_chroma12 (unit-normalized blocks)",
                       "abs": "blurred piano roll (MIDI 36-96 x 0.25ql, 16ql) + abs_chroma12"},
        "relation_names": RELATION_NAMES,
        "nodes": [{k: v for k, v in n.items() if not k.startswith("_")} for n in g["nodes"]],
        "edges": g["edges"],
    }
