"""Check the Python port of PAM against the lab's MATLAB original on musiPAM problems.

    ~/.venvs/musipam/bin/python validate.py

Needs MATLAB (with the Statistics and Machine Learning Toolbox, for pdist) and the
lab's "PAM public" folder (set MUSIPAM_PAM_DIR, default: Analysis/PAM public in the
musiPAM folder). Runs the same problems through both and reports the largest
differences in the mapping matrix and the analogy score.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from scipy.io import loadmat, savemat

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pam import attributes, pam  # noqa: E402
from problems import edges, nodes, problem_sets  # noqa: E402

PAM_DIR = Path(os.environ.get("MUSIPAM_PAM_DIR", HERE.parents[1] / "Analysis" / "PAM public"))
MATLAB = os.environ.get("MATLAB", "/Applications/MATLAB_R2024b.app/bin/matlab")
WEIGHTS = [0.0, 0.5, 1.0, 2.0]


def main() -> int:
    sets = problem_sets()
    probs = sets["cross"] + sets["variation"][::8] + sets["pairs"][::12]
    worst = []
    for node_code, edge_code in (("rel", "computed_std"), ("rel", "learned_p5"), ("abs", "computed")):
        N1, N2, E1, E2, w, py_M, py_S = [], [], [], [], [], [], []
        for p in probs:
            na, nb = nodes(p["A"], node_code), nodes(p["B"], node_code)
            ea, eb = edges(p["A"], edge_code), edges(p["B"], edge_code)
            n = len(na)
            for ow in WEIGHTS:
                N1.append(np.stack(na)); N2.append(np.stack(nb))
                E1.append(np.stack([[ea.get((i, j), np.zeros_like(ea[(0, 1)])) for j in range(n)] for i in range(n)]))
                E2.append(np.stack([[eb.get((i, j), np.zeros_like(eb[(0, 1)])) for j in range(n)] for i in range(n)]))
                w.append(ow)
                M, s = pam(attributes(na, ea), attributes(nb, eb), objweight=ow)
                py_M.append(M); py_S.append(s["score"])
        with tempfile.TemporaryDirectory() as td:
            fin, fout = Path(td) / "in.mat", Path(td) / "out.mat"
            savemat(fin, {"N1": np.array(N1), "N2": np.array(N2), "E1": np.array(E1), "E2": np.array(E2),
                          "w": np.array(w, float)[:, None]})
            cmd = f"pam_reference('{fin}', '{fout}', '{PAM_DIR}')"
            subprocess.run([MATLAB, "-batch", f"addpath('{HERE}'); {cmd}"], check=True, capture_output=True)
            ref = loadmat(fout)
        dM = np.nanmax(np.abs(np.array(py_M) - ref["Ms"]))
        dS = np.nanmax(np.abs(np.array(py_S) - ref["As"][:, 0]) / np.maximum(1e-12, np.abs(ref["As"][:, 0])))
        same_map = np.mean([np.array_equal(a.argmax(1), b.argmax(1)) for a, b in zip(py_M, ref["Ms"])])
        print(f"{node_code} nodes, {edge_code} edges: {len(w)} runs; max |M - M_matlab| = {dM:.2e}; "
              f"max relative score difference = {dS:.2e}; same hard mapping in {same_map:.0%}")
        worst.append(dM)
    return 0 if max(worst) < 1e-6 else 1


if __name__ == "__main__":
    raise SystemExit(main())
