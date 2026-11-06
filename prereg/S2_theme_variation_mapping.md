# Study 2 — Theme ↔ variation mapping (preregistration draft)

*Draft 0.1, 2026-11-06. Fields follow the OSF Preregistration template. Shared methods: [README](README.md).*

## 1. Study information

**Title.** musiPAM Study 2: Mapping the parts of a transformed theme. A test of probabilistic analogical mapping in music.

**Authors.** David G. Kamper, Hongjing Lu, Keith J. Holyoak (UCLA). *DECISION: author list.*

**Description.** PAM (Lu, Ichien & Holyoak, 2022) finds correspondences between two analogs by trading off the similarity of their parts against the similarity of the parts' relations, with a weight w. Listeners hear a theme with one motif marked, then a transformed version, and indicate which part of the variation corresponds to the marked motif. The transformations dissociate motif identity, serial position and relational role. The two groups test whether musical expertise raises the weight on relations, as expertise does in other domains (Chi, Feltovich & Glaser, 1981; Novick, 1988).

**Hypotheses.**

- **H1 (derivation over position).** When reordering (motif swap or motif-order retrograde) has moved the probed motif, listeners choose the moved motif more often than the motif now occupying the probe's serial position.
- **H2 (relative pitch).** Accuracy after tritone transposition is not lower than after a timbre change (non-inferiority margin of 10 percentage points).
- **H3 (relations disambiguate identical parts).** When the probe is one of two identical motifs (a1/a2 in periods) and both copies remain in the variation, listeners choose the relationally correct copy on more than 50% of the trials on which they choose either copy.
- **H4 (PAM).** Relation-weighted PAM (w > 0) predicts trial-level choices better than object-only PAM (w = 0), in each group.
- **H5 (expertise).** The fitted relation weight w is higher for musicians than for non-musicians.

## 2. Design plan

**Study type.** Experiment: mixed design, with group between subjects and condition and theme within.

**Blinding.** Participants are not told the transformation.

**Study design.**

- **Items.** 16 themes × 9 conditions (the 8 structural transformations plus timbre as an easy control) × 4 probe positions. Lists sample about 48 test trials per participant, balanced so that each theme × condition cell is equally probed at every position across participants.
- **Catch trials.** Four identity trials, where the variation is the theme itself and the correct answer is the same segment.
- **Practice.** Two practice trials with feedback, using a practice theme.
- **Trial.**
  1. The theme plays, with its four-segment timeline displayed.
  2. The probe motif replays alone while its segment is highlighted.
  3. The variation plays under an unlabeled four-segment timeline.
  4. The participant clicks the segment that "corresponds to the highlighted part of the theme". Any segment of either passage can be replayed before responding; replays are logged.
- **Interface.** Segment boundaries are drawn at the designed motif boundaries, validated in Study 0.

**Randomization.** Lists rotate within each group. Trial order is randomized, with no theme on consecutive trials.

## 3. Sampling plan

**Existing data.** Registration prior to the creation of data.

**Data collection.**

- **Musicians.** At least 5 years of formal training and currently playing at least 1 hour a week. Recruited from the Herb Alpert School of Music and through Prolific screening; paid.
- **Non-musicians.** Under 2 years of training and not currently playing. Recruited through UCLA SONA for credit.

**Sample size.** Provisional: 64 per group (128 in total). *DECISION: replaced by the simulation result.*

**Rationale.** H5 is the sample-limiting test. n = 64 per group gives 80% power for a between-group difference of d = 0.5 in participant-level w (two-sided α = .05). The final N comes from simulating the hierarchical PAM fit with pilot data.

**Stopping rule.** Stop at the target N per group.

## 4. Variables

**Manipulated variables.** Condition, theme and probe position (within subjects); group (between).

**Measured variables.** The chosen segment (1–4), the response time, segment replays, and the Gold-MSI Musical Training subscale.

**Indices.**

- **Identity choice:** the segment containing the probe's transformed self.
- **Position choice:** the segment at the probe's serial position.
- **Model predictions,** fixed before data collection and saved with a hash in `predictions/S2_trial_model_probs.csv`: for every item, the predicted choice probabilities under PAM at w ∈ {0, 0.1, …, 1}. Three versions are computed, using the key-relative, absolute and MERT node codes. *DECISION: the primary node code for H4–H5; proposed key-relative, with the others as robustness checks.*

## 5. Analysis plan

**Statistical models.**

- **H1.** On reorder and motif-order-retrograde trials where identity and position choices differ, restricted to trials on which one of the two was chosen: `chose_identity ~ 1 + (1 | participant) + (1 | theme)`, a logistic mixed model. H1 is supported if the intercept is greater than 0.
- **H2.** `correct ~ condition + (1 + condition | participant) + (1 | theme)` on transposition and timbre trials. The one-sided 95% CI of the accuracy difference (from `emmeans`, on the probability scale) must exclude a difference of 10 percentage points or more in favor of timbre.
- **H3.** The proportion of relationally correct copy choices, tested against 0.5 with `choice ~ 1 + (1 | participant)`.
- **H4.** Fit PAM's mapping probabilities to the choices by maximum likelihood (softmax temperature free), separately per group. Compare w = 0 with w free by likelihood ratio and by participant-blocked 10-fold cross-validation.
- **H5.** A hierarchical version with participant-level w drawn from group-level distributions (`brms` or the lab PAM fitter). H5 is supported if the 95% interval of w_musicians − w_non-musicians is above 0.

**Inference.** α = .05; H2 is one-sided by construction; Holm correction across H1–H5.

**Data exclusion.** The common exclusions apply, plus identity catch-trial accuracy below 75%.

**Missing data.** Trials with no response within 60 s after the variation ends are dropped.

**Exploratory analyses.**

- The distribution of errors after inversion and retrograde, compared with the model-predicted distributions.
- Replays as a measure of uncertainty.
- Effects of skeleton.
- Gold-MSI as a continuous predictor of w.
