# musiPAM v2 — Stimulus specification

Draft 0.1 · 2026-11-05 · status: **for audition and revision by D. Kamper**

---

## 1. What these stimuli are for

musiPAM asks whether the analogical-mapping algorithm that explains verbal analogy (PAM; Lu, Ichien & Holyoak, 2022) and visual analogy (visiPAM; Webb, Fu, Bihl, Holyoak & Lu, 2023) also explains musical analogy. PAM needs each analog as a graph, so every stimulus here is built from known parts with known relations between them:

- **Node** = a motif. Every theme has exactly four, each two bars long.
- **Edge** = a relation between two motifs: order, transposition, contour, rhythm, harmonic function, restatement.

| Study | Task | What this set supplies |
|---|---|---|
| 1a Perceived derivation | Hear theme, hear variation, rate "how much is this a version of the theme?" (1–7) | 11 conditions × 4 themes = 44 stimuli |
| 1b Motif similarity | Rate pairs of motifs | Motif onset times (`manifest.csv`) and every note (`note_events.csv`) |
| 1c Relation similarity | "Is the change A1→A2 the same kind of change as B1→B2?" | Motif pairs with computed relation vectors (`*.graph.json`) |
| 2 Theme↔variation mapping | Click the part of the variation that corresponds to a marked part of the theme | Ground-truth correspondences (`src` field of every node) |
| 3 Cross-theme mapping | Same task across themes | Two designed analog pairs (T1↔T3, T2↔T4), each containing a cross-mapping, plus four different-skeleton control pairs |

Study 1 validates the representations: 1b validates the node codes and 1c validates the relation codes. Studies 2–3 test mapping.

## 2. The themes

Each theme is 8 bars, made of 4 motifs × 2 bars. All four were composed for this study; nursery tunes are retired.

| | **T1 Pastorale** | **T2 Valse** | **T3 Lament** | **T4 Berceuse** |
|---|---|---|---|---|
| Key | D major | C minor | F minor | E major |
| Meter, tempo | 4/4, ♩ = 100 | 3/4, ♩ = 84 | 4/4, ♩ = 96 | 6/8, ♩. = 52 |
| Form | sentence: a a′ b c | parallel period: a1 b a2 c | sentence: a a′ b c | parallel period: a1 b a2 c |
| Structural analog of | T3 | T4 | T1 | T2 |
| Accompaniment idiom | Alberti broken chords over a held bass | waltz: bass, chord, chord | march: bass on 1 and 3, chords on 2 and 4 | rocking low-high-mid on each dotted-quarter beat |
| Music duration | 19.2 s | 17.1 s | 20.0 s | 18.5 s |

### Why four themes

The first draft had three themes, which was a proof-of-concept size, not a design decision. Four is the smallest balanced set:

- **A 2 × 2.** Two relational skeletons (sentence, period), each realized twice with different motifs. Every theme has exactly one structural analog and two different-skeleton partners, so each can serve equally as source and target.
- **The key result replicates.** Each analog pair carries its own cross-mapping, in a different pair of roles (opening ↔ closing in T1/T3; contrasting phrase ↔ opening in T2/T4).
- **The analog effect no longer rides on shared meter.** With three themes, the only analog pair (T1–T3) was also the only pair in the same meter, so "more analogous" and "same meter" could not be separated. T2–T4 is an analog pair whose meters differ (3/4 against 6/8). Comparing it with the different-skeleton pairs, which all differ in meter too, tests analogy with meter held different. Each analog pair also flips mode (major ↔ minor), so shared mode can't explain it either.

Instruments: melody on clarinet, accompaniment on piano (the timbre condition uses violin and harp).

### Designed relations (each one is verified automatically)

- **Sequential repetition (T1, T3).** a′ is a moved up one diatonic step, in the same rhythm.
- **Fragmentation (T1, T3).** b is three copies of the head of a, in a's head rhythm, rising in sequence to a note held over V7.
- **Identical nodes (T2).** a2 is identical to a1. Only their relations tell them apart: a1 is followed by the half-cadence phrase b, a2 by the closing phrase c. c restates b's opening and then cadences on the tonic.
- **Structural analog (T3 ≅ T1).** T3 shares T1's skeleton and inter-motif relations, but its motifs are new, and its key, mode, tempo and accompaniment idiom all differ.
- **Cross-mapping (T1 → T3).** T3's closing motif c has exactly the rhythm and diatonic contour of T1's *opening* motif a. T3's own opening motif a resembles T1's a in neither respect. Object similarity therefore says T1.a ↔ T3.c, while relational role says T1.a ↔ T3.a. This is the classic cross-mapping design (Gentner & Toupin, 1986; Markman & Gentner, 1993; Richland, Morrison & Holyoak, 2006), now built in music.
- **Structural analog (T4 ≅ T2).** T4 is a period like T2: a1 = a2 exactly, b ends on a half cadence, and c restates b's opening (same rhythm, same first two notes) and closes on the tonic. Its motifs, key, mode, meter and accompaniment idiom are all new.
- **Cross-mapping (T2 → T4).** T4's repeated opening idea (a1 = a2) has exactly the rhythm and scale-degree contour of T2's *contrasting* phrase b, in major. T4's own b resembles T2's b in neither respect. Object similarity says T2.b ↔ T4.a1 or T4.a2; relational role says T2.b ↔ T4.b.

## 3. The transformation grid

Each condition is chosen for what it does to the graph: whether it changes the nodes (motif content), the edges (relations), both, or neither.

| Condition | Grid cell | Exact rule |
|---|---|---|
| identity | control | As composed. |
| timbre | surface | Clarinet → violin, piano → harp. The notes are identical. |
| tempo | surface | Tempo × 1.3. The notes are identical. |
| transpose | probe: pitch coding | The whole passage moves down a tritone, the most distant key (D→A♭, c→f♯, f→b, E→B♭). Nothing changes under key-relative coding; every node changes under absolute-pitch coding. |
| mode | nodes only | Parallel mode (major ↔ minor). Only scale degrees 3, 6 and 7 move, each by one semitone. Minor uses context rules: the leading tone is raised over dominant harmony, and degree 6 is raised beside a raised 7th, so no augmented seconds occur. |
| ornament | nodes only | Passing tones fill melodic thirds, and neighbor-note turns decorate long notes. Every structural tone keeps its onset. |
| augment | probe: time coding | Motif 2 only is played in rhythmic augmentation (× 2). With scale-free rhythm coding only the duration relations change; with absolute coding node 2 changes too. |
| reorder | temporal edges | Motifs 2 and 3 exchange places. Every motif is identical. |
| motif_retro | temporal edges | The motif order is reversed (4 3 2 1), and each motif still plays forwards. |
| invert | nodes + edges | Diatonic inversion about scale degree 3. The tonic triad maps onto itself, dominant and subdominant exchange, and the harmony is inverted along with the melody. |
| retrograde | nodes + edges | The whole passage plays backwards, melody and harmony together. |

The **"far corner"** of the grid has new nodes but the same edges. That is the two cross-theme analog pairs (T1 ↔ T3 and T2 ↔ T4), so it needs no separate condition.

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

- the texture idiom;
- the registers, anchored to the tonic so they move with transposition;
- the instruments;
- a metric-accent velocity rule, applied identically to every stimulus.

## 5. Audio

| Parameter | Value |
|---|---|
| Renderer | FluidSynth 2.4.3, MS Basic soundfont (MuseScore 4.5.1), deterministic |
| Mixing | Melody and accompaniment are rendered as separate stems; the melody is mixed **+6 LU** above the accompaniment, identically for every stimulus |
| Loudness | Every file is normalized to **−20 LUFS** (all 44 measure −20.0) |
| Peaks | −8.5 to −11.8 dBFS; no clipping, and no limiting was needed |
| Timing | 100 ms of silence before the music; a 1.5 s tail with a 0.4 s fade; 44.1 kHz, 16-bit WAV, plus 192 kbps MP3 |

**Sound quality is the weakest link.** MS Basic is a General MIDI bank: adequate for audition and piloting, not for data collection. Every stimulus goes through the same renderer, so an upgrade changes timbre for all stimuli equally.

**Muse Sounds status (2026-11-06).** A Muse Sounds subscription is installed. VSL Piano I, VSL Strings I and VSL Harp have downloaded; VSL Woodwinds I, which supplies the clarinet, has not yet. Command-line rendering does **not** yet use Muse Sounds: with the Muse Sounds profile active, MuseScore 4.7.6 produced audio identical to the basic soundfont (waveform correlation 1.0). The likely route is to assign the Muse Sounds instruments once in the MuseScore app, save that file, and copy its per-part playback settings into every generated score. That will only work if command-line export honors explicitly assigned Muse Sounds, which remains to be tested.

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

1. **Transposition with absolute codes.** Object-only matching fails in all four themes; any relation weight (w ≥ 0.25) recovers the mapping. With key-relative codes it is invariant. This is the predicted diagnostic for absolute versus relative pitch coding.
2. **Both cross-mappings work, at the same crossover.** T1 → T3: object-only matching sends T1.a to T3.c, the look-alike. T2 → T4: it sends T2.b to T4's a1 or a2, the look-alikes. In both pairs the full role mapping wins from w = 0.5. The relation weight is identifiable, and fitting it per listener group is the analysis PAM was built for.
3. **The designed analogs are the most relationally similar pairs.** The relational similarity of the role alignment is 0.58 for T2→T4 and 0.39 for T1→T3. It is at most 0.20 for the four different-skeleton pairs, whose best possible alignment reaches only 0.30. For both analogs, the best of all 24 alignments is the role alignment.
4. **Relation vectors must be standardized.** Unstandardized, T1→T3 and T1→T2 give 0.48 versus 0.47, because positional relations are identical for any two 4-motif passages and swamp the derivational ones. The real PAM implementation will need an equivalent normalization. The T1–T3 results did not change when T4 joined the standardization corpus.
5. **The remaining cells:**
   - Mode, ornament and augmentation leave identity recoverable under any weighting. They are graded node changes, suited to the similarity ratings of Study 1a.
   - With key-relative codes, inversion breaks object-only matching in all four themes. Relation weighting recovers T2 and T3 from w = 0.75 and T4 only at w = 1, but never T1.
   - Retrograde breaks object-only matching in T1, T3 and T4. Relation weighting recovers T4 from w = 0.25 and T3 from w = 0.5, but never T1. T2's retrograde is matched at every weighting.
   - Reordering is covered under "A correction to the original grid" in §3.

## 7. Validation (`reports/validation_report.md`)

The build ran 544 automated checks with 0 errors. They confirm:

- whole bars;
- motif boundaries fall on barlines;
- the harmony spans exactly the melody;
- every motif appears exactly once;
- the melody stays in the instrument's range;
- there are no augmented seconds;
- each transformation does exactly what it claims (exact tritone shift, negated diatonic intervals, exact reversal, structural tones keeping their onsets, and so on);
- every designed relation in §2 holds;
- loudness, peak level and duration are as specified.

The share of accented beats that land on chord tones ranges from 62% to 100%. Accented dissonances are part of the style, and retrograde lowers the rate because reversal moves notes off the beat.

### Not yet validated

These need listeners:

- **Musical quality and naturalness.** Collect ratings in the pilot.
- **Unfamiliarity.** First check passed: on 2026-11-06 D. Kamper auditioned T1–T3 and found no resemblance to known tunes. T4 still needs the same check. Listeners still need to rate familiarity in the pilot, since an expert ear isn't a sample of undergraduates.
- **Motif segmentation.** The four motifs are the composer's segmentation. Whether listeners hear the same boundaries is an empirical question (Deliège's cue abstraction). Run a boundary-tapping pilot before Study 2, because the mapping task assumes these units.

## 8. Provenance (for the methods section)

The themes were drafted by an AI system (Anthropic Claude, model `claude-opus-5-5`, 2026-11-05) to the written specification above. They require review and revision by the first author before use.

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

A SHA-256 hash of every WAV file is recorded in `manifest.csv`. Builds are deterministic: two independent builds produced byte-identical WAV files.

## 9. Next steps

1. **Audition** (D. Kamper). T1–T3 are approved by ear; T4 is new. Edit `themes.py` directly; the whole set rebuilds in a few minutes.
2. **Muse Sounds.** Once VSL Woodwinds I has downloaded, open one stimulus in MuseScore, assign the VSL instruments, and save it as `.mscz`. That file will show whether command-line export can render Muse Sounds. If it can, the renderer swap is one function in `render.py`.
3. **Pilot** with three measures: naturalness and familiarity ratings, boundary tapping, and a first Study 1a run.
4. **Scale** to at least 16 themes, keeping the balanced structure: every skeleton realized more than once, each analog pair with a cross-mapping, and meter and mode varied within analog pairs.
5. **Rendering upgrade** before data collection: Muse Sounds if the test in step 2 works, otherwise another sample library through the same stem pipeline.
6. **Models.** Replace the design-check proxy with the lab's PAM code (H. Lu). Add MERT and MusicFM audio node vectors (a natural first project for B. Yang).
