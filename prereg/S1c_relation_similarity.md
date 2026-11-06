# Study 1c — Relation similarity (preregistration draft)

*Draft 0.1, 2026-11-06. Fields follow the OSF Preregistration template. Shared methods: [README](README.md).*

## 1. Study information

**Title.** musiPAM Study 1c: Do listeners perceive the change between two motifs as an abstract relation?

**Authors.** David G. Kamper, Hongjing Lu, Keith J. Holyoak (UCLA). *DECISION: author list.*

**Description.** PAM maps by matching relations, which for words are represented by BART relation vectors (Lu, Wu & Holyoak, 2019). Before relations can be used to model musical mapping, listeners must be shown to perceive musical relations abstractly: the change from one motif to another must be recognizable as the same kind of change when it is applied to a different motif. This is the musical counterpart of Ichien, Lu & Holyoak (2022), who predicted human similarity among semantic relations from relation vectors.

**Hypotheses.**

- **H1.** Two motif pairs related by the same transformation are rated more similar than two pairs related by different transformations, with the base motifs always different between the two pairs.
- **H2.** Ratings increase with the similarity of the two pairs' standardized relation vectors, over and above the similarity of the motifs involved.

**Research question RQ1.** Do MERT difference vectors (A2 − A1) predict ratings as well as the computed symbolic relation vectors?

## 2. Design plan

**Study type.** Experiment; within-subjects with counterbalanced lists.

**Blinding.** Participants are not told which transformations exist.

**Study design.**

- **Relation types.** Ten: identity, a step higher, a step lower, inversion, retrograde, augmentation, ornamentation, mode change, fragmentation (the motif's head repeated in rising sequence), and contrast (an unrelated motif).
- **Instances.** Each relation is applied to 16 base motifs, the opening motif of each theme, giving 160 instance pairs (A1 → A2).
- **Trials.** Two instances with different base motifs. They are either same-relation (20 per participant, 2 per relation type) or different-relation (44 per participant, spread over all 45 type pairs across lists). *DECISION: counts.*
- **Trial.** A1, A2, a 1.5 s pause, then B1, B2, followed by "How similar is the change from the first motif to the second, to the change from the third motif to the fourth?" (1–7).
- **Training.** Two worked practice trials with feedback-free examples, drawn from motifs not in the set.
- **Catch trials.** Four trials where both pairs are the same instance (expected rating ≥ 6).

**Randomization.** Lists are balanced so that every relation-type pair appears equally often across participants. Trial order is randomized.

## 3. Sampling plan

**Existing data.** Registration prior to the creation of data.

**Data collection.** UCLA SONA undergraduates.

**Sample size.** Provisional N = 60. *DECISION: replaced by the simulation result.*

**Rationale.** Simulation of the H1 contrast and the H2 coefficient at 90% power, using pilot variance.

**Stopping rule.** Stop at the target N per list.

## 4. Variables

**Manipulated variables.** Same versus different relation; relation types; base motifs.

**Measured variables.** Rating (1–7); Gold-MSI Musical Training.

**Indices,** computed before data collection and saved with a hash in `predictions/S1c_trial_predictors.csv`. For each trial:

- **Rsim**: the cosine of the two instances' standardized symbolic relation vectors;
- **Nsim**: the mean key-relative similarity of A1 with B1 and A2 with B2;
- **Rsim_mert**: the cosine of the MERT difference vectors.

## 5. Analysis plan

**Statistical models.** All are cumulative-link mixed models.

- **H1.** `rating ~ same_relation + (1 + same_relation | participant) + (1 | relation_type_pair) + (1 | base_motif_pair)`. H1 is supported if β > 0.
- **H2.** `rating ~ Rsim + Nsim + (1 + Rsim | participant) + (1 | relation_type_pair)`. H2 is supported if β_Rsim > 0.
- **RQ1.** Replace Rsim with Rsim_mert; compare by ΔAIC and cross-validated log-likelihood.

**Inference.** α = .05, two-sided; Holm correction across H1 and H2.

**Data exclusion.** The common exclusions apply, plus a mean catch-trial rating below 5.0.

**Missing data.** Trials with playback failures are dropped.

**Exploratory analyses.**

- The relational similarity space by MDS: are pitch-direction relations (inversion, step) separated from temporal relations (retrograde, augmentation)?
- Musical-training moderation.
- Asymmetries between relation types.
