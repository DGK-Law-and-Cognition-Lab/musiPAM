# musiPAM v2 — Stimulus specification

Draft 0.2 · 2026-11-06 · status: **for audition and revision by D. Kamper**

---

## 1. What these stimuli are for

musiPAM asks whether the analogical-mapping algorithm that explains verbal analogy (PAM; Lu, Ichien & Holyoak, 2022) and visual analogy (visiPAM; Webb, Fu, Bihl, Holyoak & Lu, 2023) also explains musical analogy. PAM needs each analog as a graph, so every stimulus here is built from known parts with known relations between them:

- **Node** = a motif. Every theme has exactly four, each two bars long.
- **Edge** = a relation between two motifs: order, transposition, contour, rhythm, harmonic function, restatement.

| Study | Task | What this set supplies |
|---|---|---|
| 0 Norming | Recognize, rate, mark motif boundaries | The 16 themes as composed |
| 1a Perceived derivation | Hear theme, hear variation, rate "how much is this a version of the theme?" (1–7) | 11 conditions × 16 themes = 176 stimuli |
| 1b Motif similarity | Rate pairs of motifs | Motif onset times (`manifest.csv`) and every note (`note_events.csv`) |
| 1c Relation similarity | "Is the change A1→A2 the same kind of change as B1→B2?" | Motif pairs with computed relation vectors (`*.graph.json`) |
| 2 Theme↔variation mapping | Click the part of the variation that corresponds to a marked part of the theme | Ground-truth correspondences (`src` field of every node) |
| 3 Cross-theme mapping | Same task across themes | 24 same-skeleton analog pairs, 8 of them with a designed cross-mapping, and 96 different-skeleton pairs |

Study 1 validates the representations: 1b validates the node codes and 1c validates the relation codes. Studies 2–3 test mapping.

## 2. The themes

Each theme is 8 bars, made of 4 motifs × 2 bars, built on one of four relational skeletons. All 16 were composed for this study; nursery tunes are retired. [STUDY_PLAN.md](STUDY_PLAN.md) explains why the set is 4 skeletons × 4 realizations.

| Theme | Skeleton | Key | Meter, tempo | Accompaniment | Music |
|---|---|---|---|---|---|
| T1 Pastorale | sentence | D major | 4/4, ♩ = 100 | Alberti bass | 19.2 s |
| T3 Lament | sentence | F minor | 4/4, ♩ = 96 | march | 20.0 s |
| T5 Canticle | sentence | G minor | 3/4, ♩ = 76 | chorale | 18.9 s |
| T6 Barcarolle | sentence | A major | 6/8, ♩. = 56 | barcarolle | 17.1 s |
| T2 Valse | period | C minor | 3/4, ♩ = 84 | waltz | 17.1 s |
| T4 Berceuse | period | E major | 6/8, ♩. = 52 | berceuse rocking bass | 18.5 s |
| T7 Promenade | period | B♭ major | 4/4, ♩ = 108 | broken-chord arpeggios | 17.8 s |
| T8 Elegy | period | B minor | 4/4, ♩ = 96 | sustained chords | 20.0 s |
| T9 Ländler | rounded | F major | 3/4, ♩ = 88 | waltz | 16.4 s |
| T10 Nocturne | rounded | F♯ minor | 6/8, ♩. = 50 | berceuse rocking bass | 19.2 s |
| T11 March | rounded | E minor | 4/4, ♩ = 104 | march | 18.5 s |
| T12 Chorale | rounded | A♭ major | 4/4, ♩ = 92 | chorale | 20.9 s |
| T13 Cascade | chain | E♭ major | 4/4, ♩ = 112 | Alberti bass | 17.1 s |
| T14 Romance | chain | C♯ minor | 4/4, ♩ = 100 | broken-chord arpeggios | 19.2 s |
| T15 Sarabande | chain | D minor | 3/4, ♩ = 80 | sustained chords | 18.0 s |
| T16 Siciliana | chain | D♭ major | 6/8, ♩. = 48 | barcarolle | 20.0 s |

Across all 176 stimuli the music lasts 12.6–26.1 s; the faster tempo condition is shortest and augmentation longest. Instruments: melody on clarinet, accompaniment on piano (the timbre condition uses violin and harp).

### Balance: no surface property predicts the skeleton

- **Mode.** Each skeleton has two major and two minor themes.
- **Meter.** Each skeleton has two themes in 4/4, one in 3/4 and one in 6/8.
- **Key.** All 16 keys are different.
- **Accompaniment.** Eight idioms, each used by exactly two themes, always in different skeletons.
- **Cross-mapping pairs.** All eight flip mode and differ in key, tempo and accompaniment; four of them also differ in meter.

### The four skeletons (each relation is verified automatically)

- **Sentence, a a′ b c (T1, T3, T5, T6).** a′ is a moved up one diatonic step, in the same rhythm. b repeats the head rhythm of a three times, rising in sequence, then holds a note. c cadences.
- **Period, a1 b a2 c (T2, T4, T7, T8).** a2 is identical to a1, so only their relations tell them apart: a1 is followed by b, which ends on a half cadence, and a2 by c. c restates b's opening (the same rhythm and the same first 5, 2, 3 and 4 notes in T2, T4, T7 and T8) and closes on the tonic.
- **Rounded, a b c a′ (T9–T12).** b and c contrast with a. a′ returns with a's first bar and a new second bar, and it closes on the tonic, which a does not.
- **Sequence chain, a a′ a″ b (T13–T16).** a′ is a moved down one diatonic step and a″ two steps, in the same rhythm. b closes on the tonic.

### Cross-mappings

In each skeleton, two of the six analog pairs carry a designed cross-mapping. The target theme contains a **look-alike**: a motif with exactly the rhythm and scale-step contour of a source motif (the probe), but in a different role. The **role match** is the target motif in the probe's position, and it differs from the probe in both rhythm and contour. Both properties are verified automatically. This is the classic cross-mapping design (Gentner & Toupin, 1986; Markman & Gentner, 1993; Richland, Morrison & Holyoak, 2006), built in music.

| Pair | Skeleton | Probe | Look-alike | Role match | Similarity to the probe (key-relative code): look-alike vs role match |
|---|---|---|---|---|---|
| T1 → T3 | sentence | T1.a | T3.c | T3.a | 0.84 vs 0.32 |
| T5 → T6 | sentence | T5.a | T6.c | T6.a | 0.76 vs 0.16 |
| T2 → T4 | period | T2.b | T4.a1 (= a2) | T4.b | 0.96 vs 0.23 |
| T7 → T8 | period | T7.a1 | T8.c | T8.a1 | 0.79 vs 0.23 |
| T9 → T10 | rounded | T9.c | T10.b | T10.c | 0.68 vs 0.29 |
| T11 → T12 | rounded | T11.b | T12.a | T12.b | 0.82 vs 0.19 |
| T13 → T14 | chain | T13.a″ | T14.b | T14.a″ | 0.81 vs 0.47 |
| T15 → T16 | chain | T15.b | T16.a | T16.b | 0.77 vs 0.36 |

Where the skeleton itself creates extra look-alikes:

- **T2 → T4.** T4's a1 and a2 are identical, so both are look-alikes.
- **T7 → T8.** A period's close restates its contrasting phrase, so T8's b resembles the probe as much as the designed look-alike c does (0.81 against 0.79).
- **T11 → T12.** T12's return a′ keeps a's first bar, so it partly resembles the probe (0.79).
- **T13 → T14.** In a chain, a, a′ and a″ share one shape, so a look-alike of one is a look-alike of all three. The probe is a″, the third statement: T14's b has a″'s exact rhythm and steps and, as a chain's b must, ends on the tonic. With the probe on a, the matcher gave the look-alike to a″ and left a on its role match, so the pair could not test the trade-off. The probe moved to a″ on 2026-11-06; no notes changed.
- **T15 → T16.** T16's a, a′ and a″ all carry the look-alike's shape. a′ is the closest of the three (0.99).

**T10 was revised on 2026-11-06** so that its pair would work; its look-alike b is unchanged. T10 used to open with a falling line, like T9's b, so the matcher swapped T10's a and b at every weight and the pair tested nothing. T10 now opens with a rising arpeggio, and its lead-back phrase c ends with a leap up to the leading tone, as T9's c ends high on the dominant.

**T6 and T12 were revised on 2026-11-09**, for PAM (§6). Their role matches had been nearly as similar to the probe as the look-alikes were (0.67 and 0.73), and PAM's normalization then never lets motif similarity win. T6 now opens with a falling tonic arpeggio that climbs back to the 7th over the dominant (its a′ follows a step higher); T12's contrast b steps down from the 5th and leaps back to it over the dominant. The look-alikes are unchanged.

## 3. The transformation grid

Each condition is chosen for what it does to the graph: whether it changes the nodes (motif content), the edges (relations), both, or neither.

| Condition | Grid cell | Exact rule |
|---|---|---|
| identity | control | As composed. |
| timbre | surface | Clarinet → violin, piano → harp. The notes are identical. |
| tempo | surface | Tempo × 1.3. The notes are identical. |
| transpose | probe: pitch coding | The whole passage moves down a tritone, the most distant key (each theme's target key is its `tritone_key` in `themes.py`; for example D→A♭ and c→f♯). Nothing changes under key-relative coding; every node changes under absolute-pitch coding. |
| mode | nodes only | Parallel mode (major ↔ minor). Only scale degrees 3, 6 and 7 move, each by one semitone. Minor uses context rules: the leading tone is raised over dominant harmony, degree 6 is raised beside a raised 7th, and a raised 7th that the harmony doesn't require is lowered next to a lowered 6th, so augmented seconds are avoided. |
| ornament | nodes only | Passing tones fill melodic thirds, and neighbor-note turns decorate long notes. Every structural tone keeps its onset. |
| augment | probe: time coding | Motif 2 only is played in rhythmic augmentation (× 2). With scale-free rhythm coding only the duration relations change; with absolute coding node 2 changes too. |
| reorder | temporal edges | Motifs 2 and 3 exchange places. Every motif is identical. |
| motif_retro | temporal edges | The motif order is reversed (4 3 2 1), and each motif still plays forwards. |
| invert | nodes + edges | Diatonic inversion about scale degree 3. The tonic triad maps onto itself, dominant and subdominant exchange, and the harmony is inverted along with the melody. |
| retrograde | nodes + edges | The whole passage plays backwards, melody and harmony together. |

The **"far corner"** of the grid has new nodes but the same edges. That is the 24 same-skeleton analog pairs, so it needs no separate condition.

**A correction to the original grid:** reordering does *not* break relational matching (see §6). Relations such as "a′ is a sequence of a" are derivational, and they survive when a′ moves. Only *temporal* relations change. Reorder therefore tests whether listeners map by serial position or by derivation, which is a useful contrast, but it is not the "edges only" cell as first described.

## 4. Accompaniment policy (changed from the earlier plan)

The earlier plan held the accompaniment fixed. That would have been a confound: an inverted, retrograded or transposed melody over the original chords clashes, and the clash itself signals "not the theme."

Instead, the **harmonic plan is transformed together with the melody**:

- Transposition changes the key.
- A mode change re-qualifies each chord.
- Inversion maps each chord root by the same mirror as the melody.
- Retrograde and reordering move each chord with its notes.

The accompaniment is then re-realized from the transformed plan. Melody and harmony always agree.

What stays fixed is everything else about the accompaniment:

- the texture idiom (one of eight: Alberti bass, waltz, march, berceuse rocking bass, chorale, barcarolle, broken-chord arpeggios, sustained chords);
- the registers, anchored to the tonic so they move with transposition;
- the instruments;
- a metric-accent velocity rule for each meter, applied identically to every stimulus.

## 5. Audio

| Parameter | Value |
|---|---|
| Renderer | FluidSynth 2.4.3, MS Basic soundfont (pinned copy, hash-checked at every build), deterministic |
| Mixing | Melody and accompaniment are rendered as separate stems; the melody is mixed **+6 LU** above the accompaniment, identically for every stimulus |
| Loudness | Every file is normalized to **−20 LUFS** (all 176 measure −20.0) |
| Peaks | −12.0 to −8.2 dBFS; no clipping, and no limiting was needed |
| Timing | 100 ms of silence before the music; a 1.5 s tail with a 0.4 s fade; 44.1 kHz, 16-bit WAV, plus 192 kbps MP3 |

**Sound quality is the weakest link.** MS Basic is a General MIDI bank: adequate for audition and piloting, not for data collection. Every stimulus goes through the same renderer, so an upgrade changes timbre for all stimuli equally.

**Muse Sounds status (2026-11-06).** All four libraries the stimuli need are installed: VSL Woodwinds I (clarinet), VSL Piano I, VSL Strings I (violin) and VSL Harp. Command-line rendering does **not** use them yet: with the Muse Sounds profile active, MuseScore 4.7.6 produced audio identical to the basic soundfont (waveform correlation 1.0), and its track report still listed the basic soundfont for each part. Two routes remain:

1. Assign the Muse Sounds instruments once in the MuseScore app, save that file, and test whether command-line export honors explicitly assigned Muse Sounds. If it does, copy those playback settings into every generated score.
2. If it doesn't, generate one long score per instrument pair (clarinet and piano for 160 stimuli, violin and harp for the 16 timbre versions) that holds those stimuli in sequence, separated by rests. Export each score's melody and accompaniment parts once from the app, and cut the stems at the known onsets. The existing stem mixing, loudness normalization and checks then run unchanged.

## 6. Motif graphs and the design check

Each stimulus's `*.graph.json` holds its four nodes and twelve directed edges.

**Node codes.** There are two, because the design separates them:

- **rel**: time-normalized pitch contour, scale-free rhythm, and a key-relative pitch-class profile.
- **abs**: a blurred piano roll on a fixed pitch/time grid, plus an absolute pitch-class profile.

**Relation vectors.** Each directed edge carries 16 dimensions:

- order: position difference, immediately-next, immediately-previous;
- pitch: register shift, and the diatonic shift of the first and of the last note;
- contour: same contour, retrograde contour;
- rhythm: duration ratio, same rhythm, retrograde rhythm;
- restatement;
- harmonic tension at the end of the first motif, at the start of the second, and its change;
- the melodic junction between the two motifs.

These are computed from the score, as visiPAM computed spatial relations. A learned relation model, a "music BART," is a later upgrade.

**Design check** (`reports/design_check.md`). This is an exact brute-force graph matcher over 24 permutations. It is a proxy for PAM, not PAM. It scores each permutation as (1 − w) × node similarity + w × relation similarity, so w = 0 is object-only matching and w = 1 is relation-only matching. The results:

1. **Transposition with absolute codes.** Object-only matching fails in all 16 themes; any relation weight (w ≥ 0.25) recovers the mapping. With key-relative codes it is invariant. This is the predicted diagnostic for absolute versus relative pitch coding.
2. **All eight cross-mappings work.** In each, object-only matching sends the probe to a look-alike, and the full role mapping wins once relations carry enough weight: from w = 0.25 (T13 → T14), w = 0.5 (T1 → T3, T5 → T6, T11 → T12, T15 → T16), w = 0.75 (T2 → T4, T7 → T8) or w = 1 (T9 → T10). The crossover varies by pair, so the relation weight is identifiable, and fitting it per listener group is the analysis PAM was built for.
3. **Same-skeleton pairs are the most relationally similar.** Their mean role similarity is 0.50 (24 pairs), against 0.28 for different-skeleton pairs (96 pairs, at most 0.58). A random analog pair beats a random control pair 87% of the time (AUC). For all 24 analogs the best of all 24 alignments is the role alignment.
4. **Relation vectors must be standardized.** Unstandardized, T1→T3 and T1→T2 give 0.48 versus 0.47, because positional relations are identical for any two 4-motif passages and swamp the derivational ones. The real PAM implementation will need an equivalent normalization.
5. **The remaining cells** (key-relative code):
   - Mode, ornament and augmentation leave identity recoverable under any weighting in all 16 themes. They are graded node changes, suited to the similarity ratings of Study 1a.
   - Inversion breaks object-only matching in all 16. Relation weighting recovers 10 of them at some weight, but never T1, T4, T5, T6, T8 or T10.
   - Retrograde is matched at every weighting only in T2 and at no weighting in T1, T6, T7, T8, T9, T10, T11, T12 and T16; the rest are matched at some weights.
   - Reordering is matched at every weight in every theme (see "A correction to the original grid" in §3).
   - Reversing the motif order breaks relation-only matching (w = 1) in seven themes: T6, and every rounded and chain theme except T9 and T15 (T10, T11, T12, T13, T14, T16). In periods the true mapping survives at every weight.

**PAM itself** (`pam/reports/pam_check.md`, 2026-11-09). The lab's PAM, run on the same graphs, is stricter than the exhaustive matcher above: its normalization discounts a motif that is similar to every candidate, so a look-alike has to stand out clearly from the role match. After the T6 and T12 revisions (§2), PAM with relations alone maps every probe to its role match, and every pair switches to its look-alike as motif weight rises, at α = 0.5 to 4 depending on the pair (key-relative motifs, standardized computed relations). With the learned relations, all 24 same-skeleton pairs are mapped by role.

**Learned motif codes** (`reports/design_check_mert.md`). The same matcher with motifs coded by MERT-v1-95M embeddings of the audio:

- MERT is robust to timbre and tempo (all 16 themes match at w = 0). It codes pitch absolutely: tritone transposition breaks object-only matching in all 16, and relations repair it.
- MERT barely registers note order. Retrograde matches at w = 0 in all 16 themes, because a time-averaged audio embedding of a motif changes little when the motif runs backwards.
- With MERT motifs and the computed relations, every cross-mapping maps by role from w = 0.25. With motifs only, MERT sends the probe to a look-alike in 5 of the 8 pairs (T5 → T6, T9 → T10, T11 → T12, T13 → T14, T15 → T16). It ranks the look-alike first among the target's four motifs in only 2 pairs, because the look-alikes match in contour and rhythm while MERT weighs key, register and texture.
- With relations taken as MERT difference vectors, nothing maps: analogs and controls are indistinguishable (AUC 55%). Learned relations need a trained relation model ([RELATION_MODEL.md](RELATION_MODEL.md)).

## 7. Validation (`reports/validation_report.md`)

The build ran 2,184 automated checks with 0 errors. They confirm:

- whole bars;
- motif boundaries fall on barlines;
- the harmony spans exactly the melody;
- every motif appears exactly once;
- the melody stays in the instrument's range;
- there are no augmented seconds;
- each transformation does exactly what it claims (exact tritone shift, negated diatonic intervals, exact reversal, structural tones keeping their onsets, and so on);
- every designed relation in §2, including both properties of every cross-mapping, holds;
- loudness, peak level and duration are as specified.

One note remains: T7's parallel-mode version keeps an A–G♭ step across a phrase boundary, where both chords require those pitches.

The share of accented beats that land on chord tones is 75–100% in the themes as composed and 62–100% across all stimuli. Accented dissonances are part of the style, and retrograde lowers the rate because reversal moves notes off the beat.

### Not yet validated

These need listeners:

- **Musical quality and naturalness.** Collect ratings in the pilot.
- **Unfamiliarity.** On 2026-11-06 D. Kamper auditioned T1–T3 and found no resemblance to known tunes. T4–T16 still need the same check. Listeners still need to rate familiarity in the pilot, since an expert ear isn't a sample of undergraduates.
- **Look-alikes.** Whether each look-alike sounds more like its probe than the role match does. Study 1b tests this (H3) before Study 3 relies on it.
- **Motif segmentation.** The four motifs are the composer's segmentation. Whether listeners hear the same boundaries is an empirical question (Deliège's cue abstraction). Run a boundary-tapping pilot before Study 2, because the mapping task assumes these units.

## 8. Provenance (for the methods section)

The themes were drafted by an AI system (Anthropic Claude, model `claude-opus-5-5`, 2026-11-05 to 06) to the written specification above. They require review and revision by the first author before use.

Every note is explicit in `stimgen/musipam_stim/themes.py`, and every transformation is deterministic code. No generative audio model is involved, so no audio derived from training data enters the stimuli. That matters for a project framed by music copyright.

**Suggested wording:** "Themes were drafted with AI assistance to a formal specification and revised by the first author; all transformations were generated programmatically."

| Software | Version |
|---|---|
| Python | 3.12.3 |
| music21 | 10.5.2 |
| numpy | 2.5.4 |
| scipy | 1.18.1 |
| pyloudnorm | 0.2.0 |
| soundfile | 0.14.0 |
| FluidSynth | 2.4.3 |
| MS Basic.sf3 | MuseScore_General v0.2; pinned copy, SHA-256 `5ea2375e8bd7d8e7…` (identical in MuseScore 4.5.1 and 4.7.6) |
| ffmpeg | for MP3 encoding |
| MERT-v1-95M | `m-a-p/MERT-v1-95M`, revision `12af15fe…`, for the learned motif codes only (`embed.py`, `requirements-models.txt`). Its weights are CC BY-NC 4.0 and are not redistributed here. |

A SHA-256 hash of every WAV file is recorded in `manifest.csv`. Builds are deterministic: this build reproduced, byte for byte, the WAV files of the earlier 3-theme and 4-theme builds (33 and 44 files).

## 9. Next steps

1. **Audition T4–T16** (D. Kamper): familiarity ("nothing resembles"), naturalness, and whether each look-alike sounds like its probe. Edit `themes.py` directly; the whole set rebuilds in about 20 minutes, or 35 seconds without audio.
2. **Spares.** Compose one more theme per skeleton for Study 0's selection.
3. **Motif-level clips** for Studies 1b and 1c, rendered from the same pipeline.
4. **Muse Sounds.** Try route 1 in §5, then route 2.
5. **Pilot** with three measures: naturalness and familiarity ratings, boundary tapping, and a first Study 1a run.
6. **Models.** PAM now runs on the stimuli (`pam/`); add the second learned code (see STUDY_PLAN.md, "Which learned models").
