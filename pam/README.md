# PAM on the musiPAM stimuli

The lab's Probabilistic Analogical Mapping model (Lu, Ichien & Holyoak, 2022), applied to the 176 musiPAM stimulus graphs. It replaces the brute-force design check in `stimgen`, which is essentially the "exhaustive search" baseline the PAM paper compared against.

- `pam.py`: a line-for-line Python port of `TestMapping_PAMfunc.m` from the lab's "PAM public" code (`Analysis/PAM public/` in the musiPAM folder): graduated assignment with bistochastic normalization.
- `validate.py` with `pam_reference.m`: runs the same problems through the port and through the unchanged MATLAB original. Result on 408 runs: largest difference in any mapping probability 2 × 10⁻¹⁶, largest relative difference in the analogy score 9 × 10⁻¹⁶, and identical hard mappings in every run.
- `problems.py`: the stimulus graphs, with motif nodes coded three ways (key-relative, absolute, MERT) and relation edges four ways (computed raw, computed standardized, learned music BART, learned to the 5th power).
- `run_pam.py`: the full sweep → [`reports/pam_check.md`](reports/pam_check.md).

## Run it

```bash
~/.venvs/musipam/bin/python run_pam.py
```

```bash
~/.venvs/musipam/bin/python validate.py
```

`validate.py` needs MATLAB with the Statistics and Machine Learning Toolbox (for `pdist`), and the lab's code folder (`MUSIPAM_PAM_DIR`, default `../../Analysis/PAM public`). The learned edges need the trained relation model (`../relations/`), and the MERT nodes need `stimgen/embed.py` to have been run.

## What α means here

α is PAM's node weight (`objweight` in the code): α = 0 maps by relations only, and larger α gives motif similarity more weight. The code applies it to both rows and columns of the normalized compatibility matrix, so node compatibilities scale with α². The paper used α = 0.1 for word triplets, 1 for texts, and 2 vs 1 for younger vs older children. For musiPAM's graphs, α above about 5 overflows the exponential in the assignment step (in the original too), so the sweep stops at α = 4.

## Results (2026-11-09, after the T6 and T12 revisions)

The MERT rows were recomputed on the Muse Sounds audio the same day; none of the figures below changed.

| Motifs | Relations | Cross-mappings: role match by relations alone | ... and look-alike once motifs weigh more | Same-skeleton pairs mapped by role (α = 0) |
|---|---|---|---|---|
| key-relative | computed, standardized | 8/8 | 8/8 | 21/24 |
| key-relative | learned (music BART) | 8/8 | 7/8 | 24/24 |
| MERT | computed, standardized | 8/8 | 2/8 | 21/24 |

- With relations alone, PAM maps the probe to its role match in all eight cross-mappings.
- As α rises, every pair switches to the look-alike, each at its own α (key-relative motifs, computed relations): 0.5 for T9 → T10; 1 for T2 → T4, T5 → T6 and T7 → T8; 2 for T1 → T3, T11 → T12 and T15 → T16; 4 for T13 → T14. A listener group's α is therefore estimable from where its choices switch.
- T5 → T6 and T11 → T12 used to stay on the role match at every α. Their role matches were nearly as similar to the probe as the look-alikes (0.67 and 0.73 against 0.76 and 0.82), and PAM's normalization discounts a motif that resembles every candidate. After the 2026-11-09 revisions (0.16 and 0.19) both switch. The lesson for design: under PAM, a look-alike has to stand out clearly, not just rank first.
- With the learned relations, PAM maps all 24 same-skeleton pairs by role.
- MERT motif codes rarely pull toward the look-alikes, consistent with MERT's look-alike ranks.

## Sharing

`pam.py` is derived from the lab's PAM code and is published here with the authors' permission (confirmed by D. Kamper, 2026-11-09). Cite Lu, Ichien & Holyoak (2022) when using it.
