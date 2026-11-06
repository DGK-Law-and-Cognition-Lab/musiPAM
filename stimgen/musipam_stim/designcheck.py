"""Design check: does each transformation dissociate node vs. edge similarity?

This is NOT PAM. It is an exact brute-force graph matcher (4 motifs -> 24
permutations) with the same two ingredients PAM trades off:

    S(pi; w) = (1 - w) * mean_i  sim(node_i, node'_pi(i))
             +      w  * mean_ij sim(rel_ij, rel'_pi(i)pi(j))

w = 0 is object-only matching; w = 1 is relation-only matching. A stimulus
"works" for its grid cell if the mapping changes with w the way the cell
predicts. The real model (Lu, Ichien & Holyoak's PAM) should replace this
proxy once the lab code is wired in.
"""
from __future__ import annotations

import itertools

import numpy as np

from .graphs import _cos, node_vector

W_LEVELS = [0.0, 0.25, 0.5, 0.75, 1.0]


def relation_norm(graphs) -> tuple[np.ndarray, np.ndarray]:
    """Per-dimension mean/sd of relation vectors over a stimulus corpus.

    Standardizing matters: raw relation vectors are dominated by positional
    dimensions that are identical for any two 4-motif passages, which makes a
    designed analog (T1~T3) no more relationally similar than a different
    skeleton (T1~T2). After standardization they separate (see report).
    """
    R = np.array([e["r"] for g in graphs for e in g["edges"]], float)
    mu, sd = R.mean(0), R.std(0)
    sd[sd == 0] = 1.0
    return mu, sd


def _mats(gA, gB, code, norm=None):
    N = np.array([[_cos(node_vector(a, code), node_vector(b, code)) for b in gB["nodes"]] for a in gA["nodes"]])
    tf = (lambda r: (np.asarray(r) - norm[0]) / norm[1]) if norm is not None else np.asarray
    rA = {(e["i"], e["j"]): tf(e["r"]) for e in gA["edges"]}
    rB = {(e["i"], e["j"]): tf(e["r"]) for e in gB["edges"]}
    n = len(gA["nodes"])
    E = {}
    for (i, j), ra in rA.items():
        for (k, l), rb in rB.items():
            E[(i, j, k, l)] = _cos(ra, rb)
    return N, E, n


def _scores(perm, N, E, n):
    node = float(np.mean([N[i, perm[i]] for i in range(n)]))
    edge = float(np.mean([E[(i, j, perm[i], perm[j])] for i in range(n) for j in range(n) if i != j]))
    return node, edge


def match(gA, gB, code: str, norm=None) -> dict:
    """Best permutation at each w, plus node/edge scores of every permutation."""
    N, E, n = _mats(gA, gB, code, norm)
    perms = list(itertools.permutations(range(n)))
    sc = {p: _scores(p, N, E, n) for p in perms}
    best = {w: max(perms, key=lambda p: (1 - w) * sc[p][0] + w * sc[p][1]) for w in W_LEVELS}
    return {"best": best, "scores": sc, "node_sim": N}


def truth_by_source(gA, gB) -> tuple:
    """Theme -> variation correspondence by motif identity (source index)."""
    return tuple(next(k for k, b in enumerate(gB["nodes"]) if b["src"] == a["src"]) for a in gA["nodes"])


def content_class(label: str) -> str:
    """Identical-content motifs (T2's a1/a2) share a class."""
    return "a" if label in ("a1", "a2") else label


def evaluate(gA, gB, truth: tuple, code: str, norm=None) -> dict:
    m = match(gA, gB, code, norm)
    la = [n["label"] for n in gA["nodes"]]
    lb = [n["label"] for n in gB["nodes"]]
    rows = {}
    for w, p in m["best"].items():
        exact = tuple(p) == truth
        by_class = all(content_class(la[i]) == content_class(lb[p[i]]) for i in range(len(p))) \
            if truth_is_identity_class(gA, gB, truth) else exact
        rows[w] = {"perm": p, "exact": exact, "class_ok": by_class,
                   "a_maps_to": lb[p[0]], "node": m["scores"][p][0], "edge": m["scores"][p][1]}
    t_node, t_edge = m["scores"][truth]
    return {"rows": rows, "truth": truth, "truth_node": t_node, "truth_edge": t_edge,
            "labels_A": la, "labels_B": lb}


def truth_is_identity_class(gA, gB, truth) -> bool:
    return all(content_class(gA["nodes"][i]["label"]) == content_class(gB["nodes"][truth[i]]["label"])
               for i in range(len(truth)))
