# musiPAM study plan

Draft 0.2 · 2026-11-06 · D. Kamper (with Claude) · companion to [STIMULUS_SPEC.md](STIMULUS_SPEC.md)

musiPAM asks whether listeners map one passage of music onto another by **relational role**, the way PAM (Lu, Ichien & Holyoak, 2022) and visiPAM (Webb et al., 2023) explain verbal and visual analogy. The program has a stimulus-norming study, three similarity experiments that validate the representations PAM needs, and two mapping experiments that test PAM directly.

| Study | Question | Task | Who |
|---|---|---|---|
| **0** Norming | Are the themes unfamiliar and natural, and do listeners hear the four motifs where we put them? | Recognize, rate, mark motif boundaries | 40, musicians and non-musicians |
| **1a** Perceived derivation | Which transformations keep "the same theme", and do motifs *plus relations* predict that better than motifs alone? | Theme → variation, rate 1–7 | ≈100 undergraduates |
| **1b** Motif similarity | Which motif representation matches what listeners hear: key-relative, absolute, or learned (MERT)? | Motif A vs motif B, rate 1–7 | ≈60 undergraduates |
| **1c** Relation similarity | Do listeners hear a change between motifs as an abstract relation that recurs across different motifs? | Change A1→A2 vs change B1→B2, rate 1–7 | ≈60 undergraduates |
| **2** Theme ↔ variation mapping | Which part of a variation do listeners map onto a given part of the theme, and does relation-weighted PAM predict it? | Click the corresponding motif | 64 musicians + 64 non-musicians |
| **3** Cross-theme mapping | Can listeners map *different* pieces by role, and does a look-alike motif pull them off it? | Click the corresponding motif | 64 musicians + 64 non-musicians |

All sample sizes are provisional. Each will be set by a simulation-based power analysis using Study 0 and pilot variance before its preregistration is registered.

---

## How many themes is fair? Sixteen.

**The target is 16 themes: 4 relational skeletons × 4 realizations, plus one spare per skeleton.** All 16 are composed and pass every automated check (2026-11-06); the four spares are not yet written.

| Skeleton | Motif form | Distinctive relations | Realizations |
|---|---|---|---|
| Sentence | a a′ b c | a′ = a one step higher; b fragments a's head; c cadences | T1, T3, T5, T6 |
| Period | a1 b a2 c | a1 = a2 exactly; b half cadence; c restates b, then closes | T2, T4, T7, T8 |
| Rounded | a b c a′ | the opening returns at the end; b and c contrast | T9, T10, T11, T12 |
| Sequence chain | a a′ a″ b | a restated twice more, each a step lower; b cadences | T13, T14, T15, T16 |

**Why more than four.** Four themes cannot support any claim beyond those four tunes. To generalize, themes have to be a random effect, and their variance can't be estimated from four. That is the "language-as-fixed-effect" problem (Clark, 1973). With few stimuli, adding participants barely raises power (Judd, Westfall & Kenny, 2012; Westfall, Kenny & Judd, 2014).

**Why this shape.** Study 3's unit is the *analog pair*, so the grid has to produce many pairs.

| Grid | Themes | Analog pairs | Different-skeleton pairs | Skeletons |
|---|---|---|---|---|
| **4 × 4 (recommended)** | 16 | **24** (8 cross-mapped, 16 clean) | 96 | 4 |
| 8 × 2 | 16 | 8 | 112 | 8 |
| 2 × 8 | 16 | 56 | 64 | 2 |

The 4 × 4 grid balances both directions of generalization: across skeletons, so the result isn't about "sentence versus period", and across realizations, so it isn't about one pair of tunes. In each skeleton, two of its six analog pairs carry a designed cross-mapping (T1→T3 and T5→T6; T2→T4 and T7→T8; T9→T10 and T11→T12; T13→T14 and T15→T16) and four are clean. That gives Study 3 a cross-mapped-versus-clean contrast for free.

**Why not more than sixteen.** Every theme needs composition, your audition, norming, and a designed relational structure. Sixteen already supports by-item random effects, and Study 0's power simulation will say whether more is needed before any main study runs.

**What makes it fair, beyond the number:**

1. **Balance.** Within each skeleton, the four realizations span both modes (two major, two minor) and several meters, tempi, keys and accompaniment idioms. No surface property may predict the skeleton.
2. **Selection by preregistered criteria.** Compose the 16 plus four spares, and keep a theme only if it passes Study 0's familiarity, naturalness and segmentation criteria. Those criteria are fixed in advance and say nothing about the hypotheses.
3. **The design check runs on every theme and is reported in full,** including cells that don't come out as predicted (T1's inversion doesn't).

---

## Who takes part

- **Studies 0–1** use UCLA SONA undergraduates. Musical training is measured as a continuous moderator (the Gold-MSI Musical Training subscale; Müllensiefen et al., 2014), and its effects are exploratory.
- **Studies 2–3** recruit two groups, because that's where the theory makes its expertise prediction: experts weight relations more (Chi, Feltovich & Glaser, 1981; Novick, 1988), so they should show a larger PAM relation weight.
  - *Musicians*: at least 5 years of formal training and currently playing at least 1 hour a week. Recruited from the Herb Alpert School of Music and Prolific.
  - *Non-musicians*: under 2 years of training and not currently playing. Recruited through SONA.
- **Every study** requires headphones. Participants must pass a Huggins-pitch headphone screen (at least 5 of 6 trials correct; Milne et al., 2021), which the 2024 study lacked. Every study also includes catch trials and the Gold-MSI.

---

## Study 0 — Stimulus norming

**Stimuli.** The identity version of all 20 composed themes (16 plus spares), plus four public-domain melodies rendered identically (Ode to Joy, Greensleeves, Frère Jacques, Amazing Grace) to anchor the familiarity scale.

**Tasks** (three blocks, order counterbalanced):

1. **Familiarity.** "Have you heard this melody before?" (yes / no / unsure), then a 1–7 familiarity rating.
2. **Naturalness.** "How natural does this sound as a piece of music?" (1–7), plus liking (exploratory).
3. **Segmentation.** On a second listening, press a key whenever a new musical idea begins.

**Retention criteria.** A theme is kept if all three hold:

- fewer than 10% of participants recognize it, and its mean familiarity is below 3.0 and at least 2 points below the known melodies;
- its mean naturalness is at least 4.0;
- each of its three designed motif boundaries is marked by at least 40% of participants, within −0.25 to +1.0 s of the boundary.

A theme that fails is revised or replaced and re-normed (n ≥ 20) before any main study.

**Also.** An unregistered usability pilot of the click-the-motif interface for Studies 2–3.

## Study 1a — Perceived derivation

**Task.** Hear the theme, hear a variation, then answer "How much does this sound like a version of the theme?" (1–7).

**Stimuli.** 16 themes × 10 transformations. Five counterbalanced lists, each covering every theme in two conditions (32 trials, about 30 minutes), plus identity catch trials in which the variation is the theme itself.

**Hypotheses:**

1. Surface changes (timbre, tempo) are rated higher than every structural transformation.
2. Tritone transposition is rated higher than mode change and ornamentation (relative pitch coding).
3. Transformations that keep derivational relations (transpose, mode, ornament, augment, reorder, motif-order retrograde) are rated higher than those that change motifs and relations together (invert, retrograde).
4. Item ratings are better predicted by motif similarity *plus* relation similarity than by motif similarity alone. The key-relative motif code beats the absolute one.

**Model link.** All similarity predictors are computed from the stimulus graphs before data collection and frozen in the preregistration, so hypothesis 4 is a fully confirmatory model test.

## Study 1b — Motif similarity

**Task.** Hear motif A, then motif B, and rate their similarity (1–7).

**Stimuli.** The 64 motifs (16 themes × 4) plus transformed single motifs. Pairs are sampled within themes, across themes, and between a motif and its own transformations: about 240 pairs in 2 lists.

**Hypotheses:**

1. The key-relative motif code predicts ratings better than the absolute code.
2. Transposed pairs are rated more similar than inverted or retrograded pairs (contour; Dowling, 1978).
3. MERT embedding similarity predicts the ratings, compared against the symbolic codes.

## Study 1c — Relation similarity

**Task.** Hear A1→A2, then B1→B2, and answer "How similar is the change from A1 to A2 to the change from B1 to B2?" (1–7).

**Stimuli.** Nine relation types (identity, step up, step down, inversion, retrograde, augmentation, ornamentation, mode change, fragmentation), plus an unrelated contrast. Each relation type is instantiated on several different base motifs, and the A and B base motifs always differ.

**Hypotheses:**

1. Pairs sharing a relation type are rated more similar than pairs with different relation types.
2. Ratings follow the standardized relation-vector similarity, beyond the similarity of the motifs involved.

**Model link.** This is the musical counterpart of validating BART's relation vectors against human relation similarity (Ichien, Lu & Holyoak, 2022). It is the step that licenses the relation half of PAM.

## Study 2 — Theme ↔ variation mapping

**Task.** The theme plays, then one motif replays highlighted on its timeline. The variation plays under an unlabeled four-segment timeline, and the participant clicks the corresponding segment. Segments can be replayed.

**Stimuli.** 16 themes × 8 structural transformations, plus timbre as an easy control. The probe position is counterbalanced, at about 48 trials per participant.

**Hypotheses:**

1. In the reordering conditions, listeners pick the moved motif over the motif now in the same serial position (derivation over position).
2. Transposition accuracy is not lower than timbre accuracy (non-inferiority test).
3. When the probe has an identical twin (a1/a2 in periods), the relationally correct copy is chosen more than half the time.
4. Relation-weighted PAM predicts choices better than object-only PAM in both groups.
5. The fitted relation weight is higher for musicians.

## Study 3 — Cross-theme mapping

**Task.** The same interface, but the target is a *different* theme.

**Items.** 24 analog pairs (8 cross-mapped, 16 clean) and 24 sampled different-skeleton pairs. On cross-mapped trials, the probe is always the motif with a look-alike.

**Hypotheses:**

1. On analog pairs, the role match is chosen above chance (25%).
2. On cross-mapped pairs, role-match choices fall below the clean-pair rate, and the look-alike is chosen above chance (object competition).
3. Musicians choose the role match more often on cross-mapped trials.
4. Relation-weighted PAM beats object-only PAM, with a higher relation weight for musicians.

This is the design of the classic cross-mapping studies (Gentner & Toupin, 1986; Markman & Gentner, 1993; Richland, Morrison & Holyoak, 2006), in music.

---

## Where the models come in, including transformer embeddings

The behavioral studies don't depend on any model. The models are the competing *predictions* the studies test. There are three layers:

1. **Motif (node) representations.**
   - Two symbolic codes, key-relative and absolute. They are interpretable, but they were hand-designed alongside the stimuli.
   - **Learned audio embeddings from a pretrained transformer: MERT-v1-95M** (`m-a-p/MERT-v1-95M` on HuggingFace), trained self-supervised on about 160,000 hours of music, with MusicFM as a robustness check.

   The learned code is essential to the argument. PAM maps over Word2Vec and visiPAM over learned visual embeddings. If musiPAM used only features chosen by the people who built the stimuli, a reviewer could call the result circular. MERT embeds the audio participants actually hear, with no knowledge of the design.
2. **Relation (edge) representations.** The computed symbolic relation vectors, and learned relations from MERT, starting with difference vectors (A′ − A). A trained relation model, a "music BART", comes later; the plan is in [RELATION_MODEL.md](RELATION_MODEL.md). B. Yang's Word2Vec experience maps directly onto this step.
3. **Mapping.** The lab's PAM code (H. Lu). The brute-force design check stands in for it until then.

**MERT results on all 16 themes (2026-11-06; `stimuli/reports/design_check_mert.md`):**

- **As a motif code, MERT works within pieces.** It is robust to timbre and tempo changes, but it codes pitch absolutely: tritone transposition breaks object-only matching in all 16 themes, and relations repair it.
- **MERT barely hears note order.** A retrograde matches its theme on motifs alone in all 16 themes, because a time-averaged audio embedding changes little when a motif runs backwards.
- **MERT only partly hears the designed look-alikes.** It ranks the look-alike first among the target's four motifs in 3 of the 8 pairs and last in 2. The look-alikes match in contour and rhythm, while MERT weighs key, register and texture. Study 1b includes a manipulation check that listeners hear the look-alikes as similar before Study 3 relies on them.
- **Raw MERT difference vectors do not capture musical relations.** As relation vectors they leave analogs and controls indistinguishable (AUC 52%). Learned relations therefore need a trained relation model, as BART was trained for words; the plan is in [RELATION_MODEL.md](RELATION_MODEL.md).

So the symbolic and learned codes make genuinely different predictions, which is what makes the preregistered comparisons informative.

### Which learned models

MERT alone is not enough. It is one audio model, so its failures (it codes key and register absolutely, and it doesn't hear contour-and-rhythm look-alikes) could be MERT's own rather than a property of learned representations. The fix is a second learned model that sees the notes rather than the sound. With it, the comparison is hand-built versus learned crossed with audio versus symbolic. The set is small and fixed in advance, so the model comparisons can't become a garden of forking paths.

| Role | Model (HuggingFace) | Input | License | What it adds |
|---|---|---|---|---|
| Confirmatory | MERT-v1-95M (`m-a-p/MERT-v1-95M`) | audio | CC BY-NC 4.0 | The standard self-supervised music encoder. Already integrated. |
| Confirmatory | CLaMP 3, symbolic encoder (`sander-wood/clamp3`) | MIDI or ABC | MIT | A learned code that sees only the notes. It is the fair learned rival to the hand-built key-relative code, and it was trained for retrieval, so its embeddings are meant to measure similarity. |
| Robustness | MERT-v1-330M (`m-a-p/MERT-v1-330M`) | audio | CC BY-NC 4.0 | Does model size change the answer? |
| Robustness | MusicFM (`minzwon/MusicFM`) | audio | MIT | A different audio training objective. |
| Exploratory | MuQ (`OpenMuQ/MuQ-large-msd-iter`) | audio | CC BY-NC 4.0 | A newer audio encoder. |
| Exploratory | CLAP (`laion/larger_clap_music`) | audio and text | Apache-2.0 | Semantic similarity (genre, mood), a contrast to structure. |
| Exploratory | Anticipatory Music Transformer (`stanford-crfm/music-medium-800k`) | MIDI | Apache-2.0 | A generative symbolic model; its hidden states were not trained as embeddings. |

The 2024 transformer trained from scratch on MAESTRO is retired. It was small, trained only on piano performances, and is not a published model, so its embeddings would not persuade a reviewer.

Licenses matter for the public repository. The CC BY-NC models' embedding arrays stay out of it, as MERT's do now; the summaries in `reports/` are fine. *DECISION: confirm the confirmatory pair (MERT-v1-95M + CLaMP 3) before the Study 1 preregistrations are registered.*

**All model predictions are computed and frozen before each study's data collection,** recorded with the code version and the stimulus-set DOI. That makes the model comparisons confirmatory rather than post hoc. MERT therefore has to be in place before the Study 1 preregistrations are registered.

---

## Order and preregistration workflow

1. **Stimulus bank.** Done for the 16 themes (2026-11-06): composed, design-checked, MERT-embedded. Still open: the four spares and motif-level clips for Studies 1b and 1c.
2. **Study 0.** Then run power simulations (`simr` / `mixedpower`) and finalize the Study 1 preregistrations.
3. **Studies 1a, 1b and 1c.** Separate samples, which can run in parallel.
4. **Study 2.**
5. **Study 3.**

Each study runs as its own Pavlovia project (its own GitLab repository), built from one shared jsPsych codebase in this repository's `experiments/` folder. Separate projects keep each study's data, piloting status, credits and SONA link apart, and let a registered study's code stay frozen while the next one is built. Studies 1a, 1b and 1c are therefore three projects, not one.

A stimulus-set release is archived on Zenodo, through the GitHub repository, before each registration. Each preregistration names that release's DOI, and each is registered on OSF immediately before its data collection.

Drafts live in [`../prereg/`](../prereg). They are drafts until registered. The sample sizes, thresholds and lists marked **DECISION** are open.

## Later in the dissertation (not yet planned in detail)

- **Production.** Given a theme, its variation, and a new theme, choose or construct the analogous variation of the new theme (an A : B :: C : ? task).
- **Cross-modal.** Map visual analogs (visiPAM stimuli) and musical analogs in the same participants, to test whether one mapping mechanism serves both.
