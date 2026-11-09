"""PAM: a line-for-line Python port of the lab's TestMapping_PAMfunc.m.

Reference: Lu, Ichien & Holyoak (2022), Probabilistic analogical mapping with
semantic relation networks, Psychological Review. The MATLAB original
("PAM public", Analysis/PAM public/TestMapping_PAMfunc.m) is the reference
implementation; `validate.py` checks this port against it.

Algorithm (version 3 of the original: graduated assignment + bistochastic normalization):

1. Compatibility W[i, j, i', j'] = 1 + cosine(attr1[i, j], attr2[i', j']) for every pair of
   attributes of the same length (node attributes sit on the diagonal i = j, edge
   attributes off it; nodes and edges are told apart only by their lengths), times
   edge presence.
2. Bistochastic normalization (Cour et al., 2006): W reshaped to (n1^2 x n2^2) and
   normalized by rows, then columns, 100 times. Node rows and columns are then
   multiplied by `objweight` (so node compatibilities scale with objweight^2), and
   edge rows and columns by their edge weights (1 by default).
3. Graduated assignment: from M = 1, 500 iterations of
   Q = sum_jj' W[i, j, i', j'] M[j, j'] + sum_ii' W[i, j, i', j'] M[i, i'],
   M = exp(beta * Q), normalize columns then rows, beta += 0.1 (from 1).
4. Analogy score: sum of W[i, j, i', j'] M[j, j'] M[i, i'] over entries with M > 1e-5.

Rows of M are graph 1 (the source), columns graph 2 (the target).
"""
from __future__ import annotations

import numpy as np


def compatibility(attr1: list[list[np.ndarray]], attr2: list[list[np.ndarray]],
                  edge1: np.ndarray, edge2: np.ndarray) -> np.ndarray:
    n1, n2 = len(attr1), len(attr2)
    W = np.zeros((n1, n1, n2, n2))
    for i in range(n1):
        for j in range(n1):
            a = np.asarray(attr1[i][j], float)
            for ip in range(n2):
                for jp in range(n2):
                    b = np.asarray(attr2[ip][jp], float)
                    if a.shape != b.shape:
                        continue
                    cos = float(a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
                    W[i, j, ip, jp] = (2.0 - (1.0 - cos)) * (edge1[i, j] > 0) * (edge2[ip, jp] > 0)
    return W


def bistochastic(W: np.ndarray, edge1: np.ndarray, edge2: np.ndarray, objweight: float,
                 iterations: int = 100) -> np.ndarray:
    n1, n2 = W.shape[0], W.shape[2]
    S = W.reshape(n1 * n1, n2 * n2).copy()       # row m = i*n1 + j, column n = i'*n2 + j'
    node_rows = np.array([i * n1 + i for i in range(n1)])
    node_cols = np.array([i * n2 + i for i in range(n2)])
    rw = np.where(edge1.reshape(-1) > 1, edge1.reshape(-1), 1.0)
    cw = np.where(edge2.reshape(-1) > 1, edge2.reshape(-1), 1.0)
    for _ in range(iterations):
        rs = S.sum(1, keepdims=True)
        S = np.divide(S, rs, out=np.zeros_like(S), where=rs != 0)
        cs = S.sum(0, keepdims=True)
        S = np.divide(S, cs, out=np.zeros_like(S), where=cs != 0)
    rw[node_rows], cw[node_cols] = objweight, objweight
    S = S * rw[:, None] * cw[None, :]
    return S.reshape(n1, n1, n2, n2)


def pam(attr1, attr2, edge1=None, edge2=None, objweight: float = 1.0, iterations: int = 500,
        beta_init: float = 1.0, beta_step: float = 0.1):
    """Probabilistic mapping matrix M (n1 x n2) and analogy scores, as in TestMapping_PAMfunc."""
    n1, n2 = len(attr1), len(attr2)
    edge1 = np.ones((n1, n1)) if edge1 is None else np.asarray(edge1, float)
    edge2 = np.ones((n2, n2)) if edge2 is None else np.asarray(edge2, float)
    W = bistochastic(compatibility(attr1, attr2, edge1, edge2), edge1, edge2, objweight)
    M = np.ones((n1, n2))
    beta = beta_init
    with np.errstate(over="ignore", invalid="ignore"):
        for _ in range(iterations):
            Q = np.einsum("ijab,jb->ia", W, M) + np.einsum("ijab,ia->jb", W, M)
            M = np.exp(beta * Q)
            M = M / M.sum(0, keepdims=True)
            M = M / M.sum(1, keepdims=True)
            beta += beta_step
    Mr = M * (M > 1e-5)
    sim = np.einsum("ijab,jb,ia->ijab", W, Mr, Mr)
    node = np.array([sim[i, i, a, a] for i in range(n1) for a in range(n2)])
    score = float(sim.sum())
    return M, {"score": score, "node_part": float(node.sum()), "relation_part": score - float(node.sum())}


def attributes(nodes: list[np.ndarray], edges: dict[tuple[int, int], np.ndarray]) -> list[list[np.ndarray]]:
    """Node vectors on the diagonal, edge vectors off it: the A{i,j} cell array of the original."""
    n = len(nodes)
    return [[nodes[i] if i == j else edges[(i, j)] for j in range(n)] for i in range(n)]
