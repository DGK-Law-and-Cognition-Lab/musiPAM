# Track A: BART-style relation model on the symbolic motif code

One regularized logistic classifier per relation on the pair code [a, b, b − a, |b − a|, a·b] of a generic symbolic motif code; a pair's relation vector is its profile of probabilities over the 26 relations. Trained on 100,278 generated pairs from Essen tunes (see `build_pairs.py`).

| Test | New tunes, same collection (Essen) | New collection (Irish and Scottish) |
|---|---|---|
| Relation recognized (top choice) | 96% | 89% |
| Correct relation among top 3 | 100% | 98% |
| Leak check: model that sees only A | 7% | 6% |
| Chance | 4% | 4% |
| Four-term analogies, learned relation vectors | 99% | 95% |
| Four-term analogies, raw motif-code differences (B − A) | 64% | 64% |
| Four-term analogies, raw pair code | 55% | 43% |
| Four-term analogies, chance | 25% | 25% |
| Natural relations found in real tunes (new tunes): 1446 pairs | 77% | |
| Natural relations found in real tunes (new collection): 1798 pairs | | 73% |

## Per relation (recall of the top choice, and AUC of the relation's own probability)

| Relation | Family | New tunes: recall | AUC | New collection: recall | AUC |
|---|---|---|---|---|---|
| repeat | repetition | 100% | 1.00 | 98% | 0.99 |
| octave_up | repetition | 100% | 1.00 | 97% | 1.00 |
| octave_down | repetition | 100% | 1.00 | 98% | 1.00 |
| seq_up_1 | sequence | 95% | 1.00 | 83% | 0.98 |
| seq_up_2 | sequence | 86% | 0.99 | 77% | 0.92 |
| seq_up_3 | sequence | 95% | 1.00 | 79% | 0.97 |
| seq_down_1 | sequence | 96% | 1.00 | 77% | 0.95 |
| seq_down_2 | sequence | 88% | 0.99 | 82% | 0.97 |
| seq_down_3 | sequence | 92% | 1.00 | 79% | 0.98 |
| real_up | sequence | 99% | 1.00 | 93% | 0.97 |
| real_down | sequence | 100% | 1.00 | 91% | 0.97 |
| inversion | contour | 99% | 1.00 | 96% | 1.00 |
| retrograde | contour | 99% | 1.00 | 98% | 1.00 |
| retro_inversion | contour | 95% | 1.00 | 79% | 0.97 |
| augmentation | rhythm | 100% | 1.00 | 97% | 1.00 |
| diminution | rhythm | 100% | 1.00 | 98% | 1.00 |
| rhythm_new | rhythm | 98% | 1.00 | 94% | 0.99 |
| pitch_new | rhythm | 94% | 1.00 | 91% | 0.98 |
| mode_change | mode | 100% | 1.00 | 96% | 1.00 |
| ornament | elaboration | 100% | 1.00 | 97% | 1.00 |
| reduction | elaboration | 100% | 1.00 | 97% | 1.00 |
| fragment | fragmentation | 81% | 0.99 | 84% | 0.98 |
| opening_kept | restatement | 86% | 1.00 | 60% | 0.98 |
| ending_kept | restatement | 99% | 1.00 | 96% | 1.00 |
| consequent | function | 97% | 1.00 | 87% | 1.00 |
| unrelated | none | 98% | 1.00 | 98% | 0.99 |

## New tunes: most frequent confusions (true → chosen, count)

- opening_kept → fragment: 118
- fragment → opening_kept: 105
- seq_down_2 → seq_down_3: 85
- seq_down_3 → seq_down_2: 77
- seq_up_2 → seq_up_1: 69
- seq_up_2 → seq_up_3: 69
- seq_up_1 → seq_up_2: 49
- fragment → consequent: 47

**Natural relations (new tunes):** repeat 100% (n = 400); seq_up_1 96% (n = 24); seq_up_2 73% (n = 15); seq_up_3 20% (n = 5); seq_down_1 87% (n = 31); seq_down_2 79% (n = 19); seq_down_3 100% (n = 20); opening_kept 50% (n = 400); ending_kept 76% (n = 400); consequent 89% (n = 132)

**Compositions (new tunes, never seen in training):** seq_up_1+ornament: both parts in top 2 0%, in top 3 2% (n = 255); inversion+augmentation: both parts in top 2 26%, in top 3 37% (n = 299); retrograde+octave_up: both parts in top 2 79%, in top 3 93% (n = 300); seq_down_2+diminution: both parts in top 2 2%, in top 3 10% (n = 299)

## New collection: most frequent confusions (true → chosen, count)

- opening_kept → fragment: 321
- seq_down_1 → seq_down_2: 145
- seq_down_3 → seq_down_2: 130
- seq_up_3 → seq_up_2: 127
- seq_down_2 → seq_down_3: 118
- seq_up_2 → seq_up_3: 96
- seq_up_2 → real_up: 84
- seq_up_1 → real_up: 77

**Natural relations (new collection):** repeat 98% (n = 400); octave_up 100% (n = 13); octave_down 100% (n = 5); seq_up_1 84% (n = 51); seq_up_2 86% (n = 21); seq_up_3 100% (n = 6); seq_down_1 69% (n = 74); seq_down_2 88% (n = 24); seq_down_3 100% (n = 4); opening_kept 40% (n = 400); ending_kept 70% (n = 400); consequent 79% (n = 400)

**Compositions (new collection, never seen in training):** seq_up_1+ornament: both parts in top 2 1%, in top 3 11% (n = 244); inversion+augmentation: both parts in top 2 15%, in top 3 25% (n = 300); retrograde+octave_up: both parts in top 2 60%, in top 3 80% (n = 300); seq_down_2+diminution: both parts in top 2 8%, in top 3 21% (n = 297)
