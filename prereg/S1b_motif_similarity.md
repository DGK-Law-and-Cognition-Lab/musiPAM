# Study 1b — Motif similarity (preregistration draft)

*Draft 0.1, 2026-11-06. Fields follow the OSF Preregistration template. Shared methods: [README](README.md).*

## 1. Study information

**Title.** musiPAM Study 1b: Which representation of a musical motif matches perceived motif similarity?

**Authors.** David G. Kamper, Hongjing Lu, Keith J. Holyoak (UCLA). *DECISION: author list.*

**Description.** PAM's mapping depends on its node representation. For words that is Word2Vec; here it is a code for two-bar musical motifs. This study tests three candidate codes against perceived similarity between pairs of motifs:

- **key-relative:** time-normalized contour, scale-free rhythm, and a key-relative pitch-class profile;
- **absolute:** a pitch-by-time piano roll and an absolute pitch-class profile;
- **learned:** MERT-v1-95M audio embeddings.

**Hypotheses.**

- **H1.** The key-relative code predicts similarity ratings better than the absolute code.
- **H2 (contour).** A motif and its transposition are rated more similar than the same motif and its inversion, and more similar than the same motif and its retrograde (Dowling, 1978).
- **H3 (manipulation check for Study 3).** Each designed look-alike pair is rated more similar than the corresponding role-matched pair. For example, T1.a against T3.c, which share rhythm and contour, is rated above T1.a against T3.a, which share only their role. This must hold for Study 3's cross-mappings to pit look against role for listeners. The MERT code does *not* rank the look-alikes highest (`reports/design_check_mert.md`), so the outcome is not guaranteed. If H3 fails, the look-alikes are redesigned (closer register, texture and key) and re-tested before Study 3.

**Research question RQ1.** How does the MERT code compare with the symbolic codes?

## 2. Design plan

**Study type.** Experiment; within-subjects with counterbalanced lists.

**Blinding.** Participants are not told how any pair was constructed.

**Study design.**

- **Stimuli.** The 64 motifs of the 16 themes, each rendered as an isolated two-bar excerpt with its own accompaniment through the standard pipeline, plus single-motif transformations.
- **Pairs.** About 240 pairs from three strata:
  - (a) all 6 within-theme pairs of each theme (96);
  - (b) motif versus its own transposition, inversion, retrograde or mode change (64; 16 per transformation, each motif used once);
  - (c) cross-theme pairs (about 80), sampled to cover the range of key-relative similarity evenly (quintile-stratified);
  - (d) for every designed cross-mapping, both the look-alike pair and the role-matched pair (for H3).

  *DECISION: final counts per stratum.*
- **Lists.** Two lists of about 120 pairs, with each pair in one list and order within the pair counterbalanced.
- **Trial.** Motif A (about 4–5 s), 0.75 s of silence, motif B, then "How similar are these two musical ideas?" (1 = not at all, 7 = identical).
- **Catch trials.** Eight trials in which motif B is exactly motif A.

**Randomization.** List rotation by order of arrival. Trial order is randomized, and no motif appears on consecutive trials.

## 3. Sampling plan

**Existing data.** Registration prior to the creation of data.

**Data collection.** UCLA SONA undergraduates for course credit.

**Sample size.** Provisional N = 60 (30 per list). *DECISION: replaced by the simulation result.*

**Rationale.** Simulation of the H1 model comparison and the H2 contrasts at 90% power, using pilot variance. The provisional N gives 30 ratings per pair.

**Stopping rule.** Stop at the target N per list.

## 4. Variables

**Manipulated variables.** The pair (item), within subjects.

**Measured variables.** Rating (1–7); Gold-MSI Musical Training.

**Indices.** For each pair: S_rel, S_abs and S_mert, the cosine similarity of the two motifs under each code. These are computed from the registered stimulus release and saved in `predictions/S1b_pair_predictors.csv`, with its hash in this registration.

## 5. Analysis plan

**Statistical models.** All are cumulative-link mixed models.

- **H1.** `rating ~ S_rel + (1 + S_rel | participant) + (1 | pair)` against the same model with S_abs. H1 is supported if ΔAIC ≥ 4 favors S_rel. As a secondary check, a Williams test compares the two dependent correlations of each code with the pair-mean ratings.
- **H2.** Within stratum (b): `rating ~ transformation + (1 + transformation | participant) + (1 | motif)`, with planned contrasts of transposition against inversion and transposition against retrograde.
- **H3.** Within stratum (d): `rating ~ pair_type + (1 + pair_type | participant) + (1 | cross_mapping)`, where pair_type is look-alike versus role-matched. H3 is supported if look-alike > role-matched. Each cross-mapping is also reported separately, and any cross-mapping whose look-alike is not rated higher is flagged for redesign.
- **RQ1.** Add the S_mert model to the H1 comparison; report ΔAIC and cross-validated log-likelihood.

**Inference.** α = .05, two-sided; Holm correction across H1, H2's two contrasts, and H3.

**Data exclusion.** The common exclusions apply, plus a mean catch-trial rating below 6.0.

**Missing data.** Trials with playback failures are dropped.

**Exploratory analyses.**

- An MDS or RSA of the full similarity structure.
- Musical-training moderation.
- Which component of the key-relative code (contour, rhythm or pitch-class) carries the fit.
- MERT layer-wise codes.
