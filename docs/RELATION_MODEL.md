# musiPAM — learning musical relations ("music BART")

Draft 0.1 · 2026-11-06 · D. Kamper (with Claude) · for discussion with B. Yang, K. Holyoak and H. Lu · companion to [STUDY_PLAN.md](STUDY_PLAN.md)

---

## Status (2026-11-06): Track A v0 is built and works

The code is in [`../relations/`](../relations) (run instructions in its README). The model is trained on 100,278 generated pairs from Essen tunes, using the symbolic motif code. It never saw a musiPAM motif.

| Test | Result | Reference |
|---|---|---|
| Relation recognized, new Essen tunes | 96% | chance 4% |
| Relation recognized, new collection (Irish and Scottish) | 89% | chance 4% |
| Leak check: a model that sees only A | 6–7% | chance 4% |
| Four-term analogies (new tunes / new collection) | 99% / 95% | raw differences: 64% / 64% |
| Relations found in real tunes | 77% / 73% | repeats ~100%, kept openings 40–50% |
| Compositions never seen in training | mostly poor | a linear model doesn't combine relations; see Track B |
| musiPAM: the designed relations named correctly (top choice) | 21 of 28 | misses are mainly in the minor-key chains |
| musiPAM design check, learned relations + position | all 8 cross-mappings; analogs vs controls 92%; 24/24 aligned by role | hand-built relations: 8/8, 87%, 24/24 |
| musiPAM design check, raw differences | 0/8 cross-mappings; 60% | — |

Learned relations, from a model that never saw the stimuli, separate analogs from controls better than the relations we built by hand. Under the lab's PAM itself (`v2/pam/`), they map all 24 same-skeleton theme pairs by role, against 21 with the computed relations. The main open problem is chromaticism: in minor keys the stimuli's harmony-driven raised 6ths and 7ths make some sequences look like real transpositions (T14, T15). Training on harmonic-minor variants should fix that. The motif code underneath is still ours, so the next step is Track A on MERT and CLaMP 3 inputs. Reports: `relations/reports/track_a_symbolic.md` and `relations/reports/musipam_learned_edges.md`.

## 1. The problem

PAM maps one graph onto another. Each graph needs two kinds of vectors:

- **Nodes.** In the verbal model these are word embeddings (Word2Vec). In musiPAM they are motif codes: the symbolic key-relative and absolute codes, or MERT.
- **Edges.** In the verbal model these are relation vectors from BART, which was *trained* to recognize relations. In musiPAM they are 16 relation features that we computed by hand from the score (§6 of [STIMULUS_SPEC.md](STIMULUS_SPEC.md)).

The hand-built edges work in the design check, but a reviewer can fairly say they were designed alongside the stimuli. The obvious learned substitute, the difference between two MERT embeddings (B − A), fails: as relation vectors, these differences leave analog pairs and controls indistinguishable (AUC 55%, chance; `reports/design_check_mert.md`). The reason is that an audio embedding moves for every reason at once (pitch content, register, rhythm, texture), so the difference reflects how much changed rather than how it changed. Word2Vec differences are a weak relation code for words for the same reason (Ichien, Lu & Holyoak, 2022).

**Goal:** a model whose output for an ordered motif pair (A, B) is similar for pairs related in the same way, whatever the motifs are. With it, musiPAM's edges come from learning, and the whole graph (learned nodes and learned edges) matches what PAM does for words.

## 2. What BART does, and what to copy

BART (Lu, Chen & Holyoak, 2012; Lu, Wu & Holyoak, 2019) has three properties worth copying exactly:

1. **Supervised by examples.** Each relation is learned from example pairs that instantiate it.
2. **A relation vector is a profile over learned relations.** A new pair is represented by its probability of instantiating each learned relation, and two relation instances are compared by comparing those profiles.
3. **It generalizes to new items.** It recognizes a learned relation in pairs of words it has never seen.

The music version keeps all three. Music has one advantage over words: we can *generate* correctly labeled pairs without limit, because musical relations are operations we can carry out on a score.

**The details**, from Lu, Ichien & Holyoak (2022), which describe the BART that PAM uses:

- Each relation is learned from about 20 positive and 70 negative word pairs; PAM's BART knows 270 relations.
- A pair's input is its two Word2Vec embeddings (600 dimensions), augmented with the same features reordered by the size of the difference between the two words (1,200 in all). Ranking by difference lines up features that play similar roles across pairs without knowing which features matter, which helps because embedding features are entangled.
- Logistic regression with elastic-net regularization selects features; Bayesian logistic regression then estimates each relation's weights, with a contrast prior (the second word's weight starts as the negative of the first's).
- PAM's edge vector is 540-dimensional: the 270 relation probabilities, plus 270 probabilities that the first word plays the relation's first role.
- Relation vectors are compared by cosine, after raising them to the 5th power, which predicts human relation similarity better (Ichien et al., 2021).

**How v0 differs, and what to add:**

- *Inputs.* v0 classifies the pair code [a, b, b − a, |b − a|, a · b] of a symbolic motif code whose features are already disentangled (contour, rhythm, pitch classes), so ranking adds little there. Add BART's difference ranking for MERT and CLaMP 3 inputs, whose features are entangled like Word2Vec's.
- *Estimation.* v0 uses L2-regularized logistic regression. Add elastic-net selection and the Bayesian contrast prior, so the method is BART's own.
- *Direction.* v0 has no role vector. Direction is built into the inventory instead, as inverse pairs (augmentation and diminution, ornament and reduction, up and down).
- *Power transform.* Tested on the musiPAM edges: it lowered analog-versus-control separation from 92% to 84% under our per-dimension standardization. Retest with PAM's own normalization.

## 3. The relation inventory

The label set should come from music theory, not from our stimulus design, so that the relations aren't ours. Three standard sources cover it: Schoenberg's catalogue of motive variation (*Fundamentals of Musical Composition*, 1967), Caplin's formal functions (*Classical Form*, 1998), and Lewin's transformational theory (*Generalized Musical Intervals and Transformations*, 1987), which treats a relation between two musical objects as the transformation that maps one onto the other.

| Family | Relations (A → B) | Parameters |
|---|---|---|
| Repetition | exact; reharmonized; octave displacement | octave ±1 |
| Sequence | diatonic (tonal) sequence; real (chromatic) transposition | ±1 to ±4 steps; semitones |
| Contour | inversion; retrograde; retrograde inversion | inversion axis |
| Rhythm | augmentation; diminution; same pitches with a new rhythm; same rhythm with new pitches; metric displacement | ×2, ×½; shift in beats |
| Mode | parallel major ↔ minor | — |
| Elaboration | ornamentation (passing tones, neighbors, turns); reduction (its inverse) | density |
| Fragmentation | head repeated; liquidation; extension | head length |
| Partial restatement | same opening, new ending; same ending, new opening | split point |
| Function | antecedent → consequent (half cadence → authentic cadence) | — |
| None | unrelated (contrast) | — |

Relations are **directed**: augmentation is the inverse of diminution, and ornamentation of reduction. PAM's edges are directed too. **Compositions** (for example, a sequence that is also ornamented) are held out of training and used to test generalization.

## 4. Training data: the pair factory

**Base motifs.** Two-bar segments of real melodies, not our own. About 12,700 public-domain folk tunes already ship with music21: the Essen collection (8,514 songs), O'Neill's *1850 Melodies* (2,009), *Aird's Airs* (1,180) and *Ryan's Mammoth Collection* (1,059), plus the Bach chorales. That is tens of thousands of motifs. Generated motifs from `theory.py` add controlled cases.

**Pairs.** For each base motif, apply each transformation with motif-level versions of `stimgen/musipam_stim/transforms.py`, transforming the harmony along with the melody, exactly as the stimuli do. Every pair is stored with its label and parameters.

**Rules that keep the labels honest:**

- **Same surface within a pair, varied across pairs.** Key, register, tempo and (for audio) instruments are drawn at random per pair and shared by A and B, so the only systematic difference between A and B is the relation.
- **Ambiguity is detected, not ignored.** If two transformations produce the same notes (inverting a symmetric motif can equal reversing it), the pair gets both labels.
- **Unrelated pairs** come from different tunes, matched for key and meter.
- **The 64 musiPAM motifs never enter training.** Exact-match and near-duplicate filters run against them.

**Scale.** About 20,000 base motifs × 30 relations ≈ 600,000 labeled pairs. Symbolic generation needs no audio, so it takes minutes to an hour, faster if the factory works on plain note lists rather than music21 objects. A subset (about 50,000 pairs) is rendered to audio through the existing FluidSynth pipeline, for audio-input models.

**Natural pairs, for testing only.** These are relations that musicians made, not our code:

- phrase pairs within folk tunes (repetition, sequence and varied repetition occur naturally);
- subjects and answers in Bach's fugues (real and tonal transposition);
- theme-and-variation sets in public-domain scores;
- variants of the same tune collected from different singers (the Meertens Tune Collections' tune families; license to check).

## 5. Models: two tracks

**Track A: BART on frozen motif codes (first milestone).** Take a frozen motif embedding x: the symbolic key-relative code, CLaMP 3's symbolic encoder, or MERT. For each relation r, fit a regularized logistic regression on the pair [x_A, x_B, x_B − x_A] (BART classified the concatenated pair). The relation vector of a pair is its profile of probabilities (p₁ … p_K), and PAM compares edges by the cosine between profiles. This is the lab's own method transposed to music, so the results compare directly with BART for words. It also answers a question worth publishing on its own: which music models encode which relations in a linearly readable form.

**Track B: a trained relation encoder (if Track A falls short, which is likely for audio codes).** A small transformer reads both motifs' note sequences (scale degree, octave, onset, duration, metric position, chord) and outputs a 64-dimensional relation embedding. It is trained to classify the relation and, with a supervised contrastive loss, to place pairs with the same relation close together whatever their base motifs. A variant puts the same head on frozen MERT or CLaMP 3 frame features.

Order of work: Track A on the symbolic code, then on CLaMP 3 and MERT, then Track B. The symbolic models train in minutes to hours on a laptop. Audio feature extraction runs overnight on CPU, or on UCLA's Hoffman2 cluster.

Positional relations (first, next, last) stay computed. They are trivial and need no learning, so PAM's edges are the learned content relations plus the computed positional ones.

## 6. What counts as working

1. **Held-out motifs and held-out collections.** Train on Essen, test on the Irish and Scottish collections; report accuracy per relation family.
2. **Four-term analogies.** Given A → B, choose which of four C → D pairs is related the same way. This is the musical version of the verbal analogy tests BART was evaluated on, and it pilots the later production study (A : B :: C : ?).
3. **Natural relations.** Does the model call a fugue answer a transposition, and a folk variant's phrase a varied repetition?
4. **Listeners (Study 1c).** The model's relation similarity should predict listeners' relation-similarity ratings better than the computed relations and MERT differences. This is the test Ichien, Lu & Holyoak (2022) ran for words.
5. **musiPAM itself.** As edge vectors: analog-versus-control separation (AUC), the eight cross-mappings, and finally the PAM fits for Studies 2 and 3.

As with every model in the program, predictions are frozen before a study's registration. **Study 1c waits for music BART** (decided 2026-11-06): it is registered once the model, its weights and its predictions for the study's trials are frozen.

## 7. Risks, and how the design handles them

- **Circularity** ("the model just learned your generator"). Labels come from music theory, training motifs from public collections, and the 64 stimulus motifs are held out. The decisive tests are natural pairs and listeners, not our stimuli.
- **Too-clean training pairs.** Generated relations are perfect; real ones are not. Add noise (stray ornaments, small rhythmic changes) to training pairs, and judge the model on natural pairs.
- **Shortcuts.** Balance every relation across keys, meters and collections. Run a one-motif baseline: a model that sees only the base motif A must stay near chance, or the labels leak. (In v0 it reaches 6–7% against 4% chance, because some relations can't be applied to every motif.)
- **Licensing.** The corpora are not redistributed. The repository gets the factory code, and trained weights only if the training data's terms allow.

## 8. A first project for B. Yang (one quarter)

| Weeks | Milestone |
|---|---|
| 1–2 | Read BART, PAM and visiPAM. Run `stimgen`. Write motif-level transforms, and extract two-bar motifs from the Essen collection. |
| 3–4 | Pair factory for the ten families, with ambiguity checks and the hold-out filter. Dataset v0. |
| 5–6 | Track A on the symbolic and CLaMP 3 codes; evaluations 1 and 2. |
| 7–8 | Track A on MERT (render the audio subset); Track B prototype. |
| 9–10 | Natural-pair tests; plug the best model into the design check; short report, with a possible CogSci submission. |

Code lives in `relations/`, next to `stimgen/`, and reuses `theory.py` and the transforms. Brandon's Word2Vec experience transfers directly: Track A is the music counterpart of probing word embeddings for relations.

## 9. Open decisions

- **The inventory** (§3). D. Kamper, as the musician, approves or trims it after auditing `relations/examples/` by ear. *Open.*
- **Symbolic first.** *Decided 2026-11-06:* the symbolic track comes first, then learned inputs.
- **Study 1c timing.** *Decided 2026-11-06:* Study 1c waits for music BART.
- **Compute.** A laptop is enough for Track A; Track B on audio may want Hoffman2.
