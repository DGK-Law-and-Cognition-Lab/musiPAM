# Audit of the relation examples

Each example file (A, a bar's rest, then B) was read back from its MusicXML and checked against the relation's definition with rules written independently of the code that made it (`audit_examples.py`). Then the trained model (`bart_symbolic.npz`) scored the pair. *p* is the model's probability for the relation the file illustrates; *rank* is that relation's place among all 26.

| File | Relation | Definition check | B's range | Accidentals in B | Model's top relation (p) | p, rank of this relation |
|---|---|---|---|---|---|---|
| `01_repeat.musicxml` | repeat | pass: same pitches and rhythm | 52-64 | none | repeat (1.00) | 1.00, 1 |
| `02_octave_up.musicxml` | octave_up | pass: every note +12 semitones, same rhythm | 64-76 | none | octave_up (1.00) | 1.00, 1 |
| `03_octave_down.musicxml` | octave_down | pass: every note -12 semitones, same rhythm | 40-52 (outside the stimuli's range) | none | octave_down (1.00) | 1.00, 1 |
| `04_seq_up_1.musicxml` | seq_up_1 | pass: every note +1 scale steps, same rhythm, still in the key | 53-65 | none | seq_up_1 (1.00) | 1.00, 1 |
| `05_seq_up_2.musicxml` | seq_up_2 | pass: every note +2 scale steps, same rhythm, still in the key | 55-67 | none | seq_up_2 (0.59) | 0.59, 1 |
| `06_seq_up_3.musicxml` | seq_up_3 | pass: every note +3 scale steps, same rhythm, still in the key | 57-69 | none | seq_up_3 (0.86) | 0.86, 1 |
| `07_seq_down_1.musicxml` | seq_down_1 | pass: every note -1 scale steps, same rhythm, still in the key | 50-62 | none | seq_down_1 (1.00) | 1.00, 1 |
| `08_seq_down_2.musicxml` | seq_down_2 | pass: every note -2 scale steps, same rhythm, still in the key | 48-60 (outside the stimuli's range) | none | seq_down_2 (0.79) | 0.79, 1 |
| `09_seq_down_3.musicxml` | seq_down_3 | pass: every note -3 scale steps, same rhythm, still in the key | 47-59 (outside the stimuli's range) | none | seq_down_3 (0.89) | 0.89, 1 |
| `10_real_up.musicxml` | real_up | pass: every note +2 semitones, same rhythm, leaves the key | 54-66 | #4, #4, #4, #4 | real_up (1.00) | 1.00, 1 |
| `11_real_down.musicxml` | real_down | pass: every note -2 semitones, same rhythm, leaves the key | 50-62 | b7, b3, b7, b7 | real_down (1.00) | 1.00, 1 |
| `12_inversion.musicxml` | inversion | pass: intervals mirrored about the first note (in scale steps), same rhythm | 50-62 | none | inversion (1.00) | 1.00, 1 |
| `13_retrograde.musicxml` | retrograde | pass: notes and rhythm backwards | 52-64 | none | retrograde (1.00) | 1.00, 1 |
| `14_retro_inversion.musicxml` | retro_inversion | pass: mirrored, then backwards | 50-62 | none | retro_inversion (1.00) | 1.00, 1 |
| `15_augmentation.musicxml` | augmentation | pass: same pitches, every onset and duration x2 | 52-64 | none | augmentation (1.00) | 1.00, 1 |
| `16_diminution.musicxml` | diminution | pass: same pitches, every onset and duration x0.5 | 52-64 | none | diminution (1.00) | 1.00, 1 |
| `17_rhythm_new.musicxml` | rhythm_new | pass: same pitches, a different rhythm of the same length | 52-64 | none | rhythm_new (1.00) | 1.00, 1 |
| `18_pitch_new.musicxml` | pitch_new | pass: same rhythm and first note, new pitches | 53-67 | none | pitch_new (0.97) | 0.97, 1 |
| `19_mode_change.musicxml` | mode_change | pass: same letters and rhythm; only 3rds, 6ths and 7ths altered by a semitone | 51-63 | b6, b3, b3, b3, b3 | mode_change (1.00) | 1.00, 1 |
| `20_ornament.musicxml` | ornament | pass: A's notes kept at their onsets; 5 added notes, each a passing tone or part of a neighbor-note figure | 52-64 | none | ornament (1.00) | 1.00, 1 |
| `21_reduction.musicxml` | reduction | pass: A's notes kept at their onsets; 6 added notes, each a passing tone or part of a neighbor-note figure | 52-64 | none | reduction (1.00) | 1.00, 1 |
| `22_fragment.musicxml` | fragment | pass: bar 1 of A, then bar 1 again a scale step higher or lower | 52-60 | none | fragment (0.74) | 0.74, 1 |
| `23_opening_kept.musicxml` | opening_kept | pass: A's first bar kept, a new second bar that does not end on the tonic | 50-60 | none | opening_kept (0.54) | 0.54, 1 |
| `24_ending_kept.musicxml` | ending_kept | pass: A's second bar kept, a new first bar | 52-64 | none | ending_kept (0.97) | 0.97, 1 |
| `25_consequent.musicxml` | consequent | pass: A ends away from the tonic; B keeps bar 1 and ends on it | 53-62 | none | consequent (1.00) | 1.00, 1 |
| `26_unrelated.musicxml` | unrelated | pass: different intervals and rhythm | 52-64 | none | unrelated (0.82) | 0.82, 1 |

**26/26 examples pass their definition check; the model ranks the illustrated relation first for 26/26.**

Accidentals are scale degrees altered against the key (#7 = raised 7th). B's range is in MIDI note numbers; the stimuli's melodies stay within 50-94.
