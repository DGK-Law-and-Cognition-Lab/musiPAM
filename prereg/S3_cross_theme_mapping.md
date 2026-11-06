# Study 3 — Cross-theme analogical mapping (preregistration draft)

*Draft 0.1, 2026-11-06. Fields follow the OSF Preregistration template. Shared methods: [README](README.md).*

## 1. Study information

**Title.** musiPAM Study 3: Mapping one piece of music onto a different piece by relational role.

**Authors.** David G. Kamper, Hongjing Lu, Keith J. Holyoak (UCLA). *DECISION: author list.*

**Description.** Two different themes can share a relational skeleton (for example, both are sentences) while sharing no motifs. In half of the analog pairs, the target theme contains a **look-alike**: a motif with the shape of a source motif but a different role. This is the classic cross-mapping design (Gentner & Toupin, 1986; Markman & Gentner, 1993; Richland, Morrison & Holyoak, 2006). Listeners mark which part of the target corresponds to a probed part of the source.

**Hypotheses.**

- **H1 (relational mapping).** On clean analog pairs, the role-matched segment is chosen above chance (25%).
- **H2 (object competition).** On cross-mapped analog pairs where the probe has a look-alike:
  - (a) the role match is chosen less often than on clean analog pairs; and
  - (b) the look-alike is chosen above chance (25%).
- **H3 (expertise).** On cross-mapped trials, musicians choose the role match more often than non-musicians.
- **H4 (PAM).** Relation-weighted PAM predicts choices better than object-only PAM, and the fitted w is higher for musicians.

**Precondition.** Study 1b's H3 manipulation check must show that each look-alike pair is perceived as more similar than its role-matched pair. Cross-mappings that fail it are redesigned and re-tested before this study runs.

## 2. Design plan

**Study type.** Experiment: mixed design, with group between subjects and pair type within.

**Blinding.** Participants are not told that themes share structures.

**Study design.**

- **Items.**
  - 24 analog pairs: same skeleton, from 4 skeletons × the 6 pairs of 4 realizations. Of these, 8 are cross-mapped and 16 are clean.
  - 24 different-skeleton control pairs, sampled from the 96 available and balanced across skeleton combinations.
- **Direction.** Each pair is presented in both directions across participants, and cross-mappings are look-alike in both directions.
- **Probes.**
  - On cross-mapped trials, the probe is the motif that has a look-alike.
  - On clean analog and control trials, the probe position is counterbalanced.
- **Per participant.** About 48 trials (24 analog, of which 8 are cross-mapped, plus 24 control), 4 catch trials (the source and target are the same theme), and 2 practice trials.
- **Trial.** The interface is identical to Study 2's, except that the second passage is a different theme.

**Randomization.** Lists rotate within each group. Trial order is randomized, and no theme appears on consecutive trials.

## 3. Sampling plan

**Existing data.** Registration prior to the creation of data.

**Data collection.** As in Study 2, with the same group definitions. Participants of Studies 1–2 are not eligible.

**Sample size.** Provisional: 64 per group. *DECISION: replaced by the simulation result.*

**Rationale.** H3 is sample-limiting: 80% power for d = 0.5 on the participant-level rate of role choices on cross-mapped trials. The final N comes from simulation.

**Stopping rule.** Stop at the target N per group.

## 4. Variables

**Manipulated variables.** Pair type (clean analog, cross-mapped analog, control), skeleton and probe position (within subjects); group (between).

**Measured variables.** The chosen segment, the response time, replays, and Gold-MSI Musical Training.

**Indices.**

- **Role choice:** the segment with the probe's relational role.
- **Look-alike choice:** on cross-mapped trials, the segment with the probe's shape.
- **Other choice.**
- **Model predictions,** fixed before data collection with a hash in `predictions/S3_trial_model_probs.csv`: the PAM choice probabilities at w ∈ {0, 0.1, …, 1} for every trial, under each node code.

## 5. Analysis plan

**Statistical models.**

- **H1.** Clean analog trials: `role_choice ~ 1 + (1 | participant) + (1 | pair)` with offset logit(0.25). H1 is supported if the intercept is greater than 0.
- **H2a.** Analog trials: `role_choice ~ cross_mapped + (1 + cross_mapped | participant) + (1 | pair)`. H2a is supported if β_cross_mapped < 0.
- **H2b.** Cross-mapped trials: `lookalike_choice ~ 1 + (1 | participant) + (1 | pair)` with offset logit(0.25). H2b is supported if the intercept is greater than 0.
- **H3.** Cross-mapped trials: `role_choice ~ group + (1 | participant) + (1 + group | pair)`. H3 is supported if musicians score higher.
- **H4.** As in Study 2: maximum-likelihood or hierarchical PAM fits per group, w = 0 against free w by likelihood ratio and cross-validation, and the group difference in w.

**Inference.** α = .05, two-sided; Holm correction across H1, H2a, H2b, H3 and H4.

**Data exclusion.** The common exclusions apply, plus catch-trial accuracy below 75%.

**Missing data.** As in Study 2.

**Exploratory analyses.**

- Whether any consistent mapping appears on control pairs, such as position-based mapping.
- Skeleton-specific effects.
- Direction asymmetries.
- Gold-MSI as a continuous predictor.
- Comparison of node codes.
