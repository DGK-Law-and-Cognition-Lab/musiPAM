# Study 1a — Perceived derivation (preregistration draft)

*Draft 0.1, 2026-11-06. Fields follow the OSF Preregistration template. Shared methods: [README](README.md).*

## 1. Study information

**Title.** musiPAM Study 1a: Which transformations preserve a musical theme's identity, and do relations between motifs predict it?

**Authors.** David G. Kamper, Hongjing Lu, Keith J. Holyoak (UCLA). *DECISION: author list.*

**Description.** Analogical mapping models such as PAM (Lu, Ichien & Holyoak, 2022) represent an analog as a graph. The nodes are its parts, here two-bar motifs; the edges are the relations between parts. This study asks how strongly listeners hear a variation as "a version of" its theme across ten transformations, each chosen for what it does to that graph:

| Transformation | What it changes |
|---|---|
| timbre, tempo | surface only |
| tritone transposition | absolute pitch only |
| mode change, ornamentation | motif content |
| motif-2 augmentation | duration relations |
| motif reordering, motif-order retrograde | temporal relations only |
| inversion, note-level retrograde | motifs and relations together |

It also tests whether ratings are better predicted by motif similarity plus relation similarity, computed before data collection from the stimulus graphs, than by motif similarity alone.

**Hypotheses.** All are directional.

- **H1 (surface invariance).** Timbre and tempo variations are rated higher than the mean of the eight structural transformations.
- **H2 (relative pitch coding).** Tritone transposition is rated higher than mode change, and higher than ornamentation.
- **H3 (relations carry identity).** The transformations that keep derivational relations (transposition, mode change, ornamentation, augmentation, reordering, motif-order retrograde) are rated higher than those that change motifs and relations together (inversion, retrograde).
- **H4 (graph similarity).** In item-level models, adding relation similarity R to motif similarity N improves fit, and R's coefficient is positive.
- **H5 (pitch code).** Motif similarity computed with the key-relative code predicts ratings better than with the absolute code.

**Research question RQ1 (no directional prediction).** How does the learned MERT motif code compare with the symbolic codes in predicting the ratings?

## 2. Design plan

**Study type.** Experiment; within-subjects with counterbalanced lists.

**Blinding.** Participants are not told the transformation of any trial, or that the study concerns relations.

**Study design.**

- **Factors.** Condition (10 transformations) × theme (16 themes, from 4 skeletons × 4 realizations).
- **Lists.** Five lists, built by a cyclic Latin design. Each list contains every theme in exactly two conditions, and every theme × condition cell appears in exactly one list.
- **Per participant.** 32 test trials, 4 identity catch trials (the variation is the theme itself, in four different themes), and 2 practice trials using a practice theme from outside the set.
- **Trial.** The theme plays (about 15–20 s), then 1.0 s of silence, then the variation. Afterwards the participant answers "How much does this sound like a version of the theme?" (1 = not at all, 7 = completely). Responses are enabled only after the variation ends, and there is no replay. *DECISION: allow one replay or not.*

**Randomization.**

- List assignment rotates across participants in order of arrival.
- Trial order is randomized per participant, with the constraint that the same theme never appears on consecutive trials.
- Catch trials are placed at random positions within each quarter of the session.

## 3. Sampling plan

**Existing data.** Registration prior to the creation of data.

**Data collection.** UCLA SONA undergraduates for course credit. Participants must report normal hearing and use headphones.

**Sample size.** Provisional N = 100 included participants (20 per list). *DECISION: replaced by the simulation result.*

**Sample size rationale.** N will be set by simulating the H4 model comparison and the H1–H3 contrasts (`simr`) with variance components from Study 0 and the pilot. The target is 90% power for each confirmatory test at α = .05 after Holm correction. The provisional N gives 20 ratings per theme × condition cell.

**Stopping rule.** Stop when every list has its target number of included participants.

## 4. Variables

**Manipulated variables.** Condition (10 levels) and theme (16 levels), both within subjects.

**Measured variables.** Rating (1–7) on each trial; the Gold-MSI Musical Training subscale; years of formal training.

**Indices,** fixed before data collection. For each theme → variation item, under the ground-truth motif correspondence (known by construction):

- **N_rel**: the mean cosine similarity between corresponding motifs, key-relative code.
- **N_abs**: the same, with the absolute code.
- **N_mert**: the same, with the MERT code.
- **R**: the mean similarity of corresponding relation vectors, standardized over the stimulus corpus.

These come from the `stimgen` generator at the registered commit and are saved in `predictions/S1a_item_predictors.csv`, whose SHA-256 hash goes in this registration.

## 5. Analysis plan

**Statistical models.** All are cumulative-link mixed models (`ordinal::clmm`) of the rating.

- **H1–H3.** `rating ~ condition + (1 + condition | participant) + (1 + condition | theme)`, simplified for convergence by the common rule. Planned contrasts are computed with `emmeans` on the latent scale:
  - H1: the mean of {timbre, tempo} against the mean of the 8 structural conditions;
  - H2: transposition against mode, and transposition against ornament (2 tests);
  - H3: the mean of {transpose, mode, ornament, augment, reorder, motif_retro} against the mean of {invert, retrograde}.
- **H4.** `M0: rating ~ N_rel + (1 + N_rel | participant) + (1 | theme)` against `M1: M0 + R`. Test by likelihood ratio; H4 is supported if the LRT is significant and β_R > 0.
- **H5.** Two non-nested models, one using N_rel and one using N_abs, each with the same random structure as M0. H5 is supported if ΔAIC ≥ 4 favors N_rel; if neither model leads by that margin, H5 is inconclusive.
- **RQ1.** The same comparison including an N_mert model, reported descriptively, with ΔAIC and 10-fold cross-validated log-likelihood by participant.

**Transformations.** All predictors are z-scored across items before modeling.

**Inference criteria.** α = .05, two-sided. Holm correction across the six confirmatory tests: H1, H2 (×2), H3, H4 and H5.

**Data exclusion.** The common exclusions apply (README), plus a participant whose mean rating on identity catch trials is below 5.0. *DECISION: threshold.*

**Missing data.** Trials with audio playback failures are dropped; there is no imputation.

**Exploratory analyses** (labeled as exploratory in any report):

- moderation by Gold-MSI Musical Training;
- condition × skeleton interactions;
- the relation weight that best fits ratings, from a grid over w;
- MERT layer-wise codes;
- item-level outliers.

## 6. Other

All stimuli, item predictors and analysis code are public: GitHub DGK-Law-and-Cognition-Lab/musiPAM, archived on Zenodo (*DOI at registration*).
