"""Track A: a BART-style relation model.

As in BART (Lu, Chen & Holyoak, 2012; Lu, Wu & Holyoak, 2019), every relation
gets its own regularized logistic classifier on the pair's features, and a
pair is represented by its profile of probabilities over all learned
relations. Two relation instances are compared by comparing their profiles.

The K classifiers are independent (one-vs-rest, sigmoid outputs, not a
softmax), so a pair can instantiate two relations at once. They are fitted
jointly with L-BFGS, which is identical to fitting them one at a time.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, log_expit
from scipy.stats import rankdata


class RelationModel:
    def __init__(self, names: list[str], l2: float = 1.0):
        self.names, self.l2 = list(names), l2
        self.mu = self.sd = self.W = self.b = None

    # ------------------------------------------------------------------
    def fit(self, X: np.ndarray, y: np.ndarray, maxiter: int = 1000) -> "RelationModel":
        K, n = len(self.names), len(X)
        self.mu, self.sd = X.mean(0), X.std(0)
        self.sd[self.sd < 1e-8] = 1.0
        Z = ((X - self.mu) / self.sd).astype(np.float32)
        Y = np.zeros((n, K), np.float32)
        Y[np.arange(n), y] = 1.0
        d = Z.shape[1]

        def loss_grad(theta):
            W = theta[:d * K].reshape(d, K).astype(np.float32)
            b = theta[d * K:].astype(np.float32)
            S = Z @ W + b
            loss = -(Y * log_expit(S) + (1 - Y) * log_expit(-S)).sum() / n + 0.5 * self.l2 * float((W * W).sum()) / n
            G = (expit(S) - Y) / n
            gW = Z.T @ G + self.l2 * W / n
            return float(loss), np.concatenate([gW.ravel(), G.sum(0)]).astype(np.float64)

        res = minimize(loss_grad, np.zeros(d * K + K), jac=True, method="L-BFGS-B",
                       options={"maxiter": maxiter})
        self.W = res.x[:d * K].reshape(d, K).astype(np.float32)
        self.b = res.x[d * K:].astype(np.float32)
        self.fit_info = {"iterations": int(res.nit), "loss": float(res.fun), "converged": bool(res.success)}
        return self

    def profile(self, X: np.ndarray) -> np.ndarray:
        """Probability that each pair instantiates each learned relation (n x K)."""
        return expit(((X - self.mu) / self.sd).astype(np.float32) @ self.W + self.b)

    # ------------------------------------------------------------------
    def save(self, path) -> None:
        np.savez_compressed(path, names=np.array(self.names), l2=self.l2, mu=self.mu, sd=self.sd, W=self.W, b=self.b)

    @staticmethod
    def load(path) -> "RelationModel":
        z = np.load(path, allow_pickle=False)
        m = RelationModel([str(x) for x in z["names"]], float(z["l2"]))
        m.mu, m.sd, m.W, m.b = z["mu"], z["sd"], z["W"], z["b"]
        return m


# ----------------------------------------------------------------------
# evaluation helpers
# ----------------------------------------------------------------------
def auc(scores: np.ndarray, positive: np.ndarray) -> float:
    """Area under the ROC curve (rank-based; ties count half)."""
    n_pos, n_neg = int(positive.sum()), int((~positive).sum())
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    ranks = rankdata(scores)
    return float((ranks[positive].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def cosine_rows(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    a = A / np.maximum(np.linalg.norm(A, axis=-1, keepdims=True), 1e-9)
    b = B / np.maximum(np.linalg.norm(B, axis=-1, keepdims=True), 1e-9)
    return (a * b).sum(-1)


def analogy_accuracy(R: np.ndarray, y: np.ndarray, base: np.ndarray, rng: np.random.Generator,
                     n_items: int = 4000, n_foils: int = 3) -> float:
    """Four-term analogy test. For a pair A->B, the answer is another pair with the same
    relation (from a different base motif); the foils are pairs with other relations.
    The model chooses the candidate whose relation vector is most similar."""
    by_rel = {k: np.flatnonzero(y == k) for k in np.unique(y)}
    items = rng.choice(len(y), size=min(n_items, len(y)), replace=False)
    correct = tested = 0
    for i in items:
        same = by_rel[y[i]][base[by_rel[y[i]]] != base[i]]
        others = np.flatnonzero((y != y[i]) & (base != base[i]))
        if len(same) == 0 or len(others) < n_foils:
            continue
        cands = np.concatenate([[rng.choice(same)], rng.choice(others, n_foils, replace=False)])
        sims = cosine_rows(R[i][None, :], R[cands])
        correct += int(np.argmax(sims) == 0)
        tested += 1
    return correct / max(tested, 1)
