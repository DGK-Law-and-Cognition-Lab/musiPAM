# Study 0 — Stimulus norming (preregistration draft)

*Draft 0.1, 2026-11-06. Fields follow the OSF Preregistration template. Shared methods: [README](README.md).*

## 1. Study information

**Title.** musiPAM Study 0: Norming novel musical themes for familiarity, naturalness and motif segmentation.

**Authors.** David G. Kamper, Hongjing Lu, Keith J. Holyoak (UCLA). *DECISION: author list and order.*

**Description.** musiPAM tests analogical mapping between musical passages. Its stimuli are newly composed eight-bar themes, each designed as four two-bar motifs with specified relations among them. Before any hypothesis-testing study, each theme must be shown to be:

1. **unfamiliar**, so that responses reflect perception rather than memory;
2. **natural**, heard as real music rather than an exercise;
3. **segmented as designed**: listeners must hear motif boundaries where the design places them, because Studies 2 and 3 ask listeners to map motifs.

This study applies fixed retention criteria to every theme.

**Hypotheses.** None. This is a norming study with preregistered item-selection criteria (Section 5).

## 2. Design plan

**Study type.** Observational norming; within-subjects.

**Blinding.** Participants are not told that the melodies were composed for the study, or that some are well known.

**Study design.** Every participant hears every melody in three blocks, with the block order counterbalanced across participants (Latin square):

- **Familiarity.** "Have you heard this melody before?" (yes / no / not sure), then "How familiar is it?" (1 = not at all, 7 = very).
- **Naturalness.** "How natural does this sound as a piece of music?" (1–7). Then "How much do you like it?" (1–7, exploratory).
- **Segmentation.** After one complete listening, a second listening during which the participant presses the space bar "each time a new musical idea begins". A practice melody is used first.

**Randomization.** Melody order is randomized within each block.

## 3. Sampling plan

**Existing data.** Registration prior to the creation of data.

**Data collection.**

- **Non-musicians.** UCLA SONA participants for course credit.
- **Musicians.** Students of the Herb Alpert School of Music, or Prolific participants screened for at least 5 years of formal training, paid at the Prolific-recommended rate.

**Sample size.** 40 included participants: 20 musicians and 20 non-musicians.

**Rationale.** With n = 40 raters and a rating SD of about 1.5, each item's mean has a standard error of about 0.24 scale points. That is adequate to apply the thresholds below. The segmentation proportions have 95% CI half-widths of at most ±0.15.

**Stopping rule.** Stop when 40 participants meeting the inclusion criteria have completed the study.

## 4. Variables

**Stimuli.**

- **Composed themes.** All composed themes (the identity versions of 16 main themes and 4 spares) from musiPAM stimulus set *vX.Y* (*Zenodo DOI at registration*).
- **Familiarity anchors.** Four public-domain melodies rendered through the same pipeline: Ode to Joy, Greensleeves, Frère Jacques, Amazing Grace. *DECISION: final anchor list.*

**Measured variables.** Recognition (yes / no / not sure), familiarity (1–7), naturalness (1–7), liking (1–7), and key-press times in the segmentation block (s, relative to audio onset).

**Indices.**

- **Recognition rate.** The proportion of "yes" responses.
- **Boundary agreement,** for each designed motif boundary (the onsets of bars 3, 5 and 7): the proportion of participants who press at least once within −0.25 to +1.0 s of the boundary. The window allows for response lag.

## 5. Analysis plan

**Retention criteria.** A theme is retained only if it meets all three:

1. Recognition rate below 10%, mean familiarity below 3.0, and mean familiarity at least 2.0 points below the mean of the four anchor melodies.
2. Mean naturalness of at least 4.0.
3. Each of its three designed boundaries has boundary agreement of at least 40%.

*DECISION: thresholds.* The values above are the proposal; once registered they are fixed.

**Validity checks of the measures.**

- The anchor melodies must reach a mean familiarity of at least 5.0. If they don't, the familiarity measure is treated as invalid and the study is rerun with a revised measure.
- Segmentation validity: across all themes, the rate of key presses near designed boundaries must exceed the rate near non-boundary barlines (bars 2, 4, 6 and 8), tested with a paired permutation test. If it doesn't, the segmentation criterion cannot certify any theme.

**Replacement rule.** A theme that fails is revised or replaced. It must then pass the same criteria in a new sample of at least 20 participants before entering any main study. Each skeleton must end with four retained realizations, and spares fill in first.

**Data exclusion.** The common exclusions apply (README). In addition, a participant who makes no key press on more than half of the segmentation trials is excluded from the segmentation indices only.

**Missing data.** Items with missing responses are dropped per participant; there is no imputation.

**Exploratory analyses.**

- Musician versus non-musician differences on each index.
- Liking.
- Boundary agreement at the level of beats within motifs.

## 6. Other

This study has no hypotheses about mapping. Its results are used only to select stimuli and to estimate variance for the power simulations of Studies 1–3.
