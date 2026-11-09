# Learned relations in the musiPAM design check

The relation model was trained only on generated pairs of folk-tune motifs (`train_bart.py`); it never saw a musiPAM motif. Here its relation vectors replace the hand-built edges of the 176 stimuli, and stimgen's design check is rerun (motif nodes stay on the key-relative code).

## Does the model name the designed relations?

For each theme, the relations its skeleton was built on, and what the model calls them.

| Theme | Skeleton | Edge | Built as | Model's top relation (p) | Rank of the built relation |
|---|---|---|---|---|---|
| T1 | sentence | a → a′ | seq_up_1 | seq_up_1 (1.00) | 1 |
| T2 | period | a₁ → a₂ | repeat | repeat (0.99) | 1 |
| T2 | period | b → c | consequent | pitch_new (0.67) | 2 |
| T3 | sentence | a → a′ | seq_up_1 | seq_up_1 (0.03) | 1 |
| T4 | period | a₁ → a₂ | repeat | repeat (0.99) | 1 |
| T4 | period | b → c | consequent | inversion (0.92) | 4 |
| T5 | sentence | a → a′ | seq_up_1 | seq_up_2 (0.14) | 2 |
| T6 | sentence | a → a′ | seq_up_1 | seq_up_1 (0.32) | 1 |
| T7 | period | a₁ → a₂ | repeat | repeat (1.00) | 1 |
| T7 | period | b → c | consequent | consequent (0.98) | 1 |
| T8 | period | a₁ → a₂ | repeat | repeat (1.00) | 1 |
| T8 | period | b → c | consequent | consequent (0.99) | 1 |
| T9 | rounded | a → a′ | consequent | consequent (1.00) | 1 |
| T10 | rounded | a → a′ | consequent | consequent (0.27) | 1 |
| T11 | rounded | a → a′ | consequent | consequent (1.00) | 1 |
| T12 | rounded | a → a′ | consequent | consequent (0.99) | 1 |
| T13 | chain | a → a′ | seq_down_1 | seq_down_1 (1.00) | 1 |
| T13 | chain | a′ → a″ | seq_down_1 | seq_down_1 (0.86) | 1 |
| T13 | chain | a → a″ | seq_down_2 | seq_down_2 (0.87) | 1 |
| T14 | chain | a → a′ | seq_down_1 | seq_down_1 (1.00) | 1 |
| T14 | chain | a′ → a″ | seq_down_1 | real_down (1.00) | 25 |
| T14 | chain | a → a″ | seq_down_2 | seq_down_2 (0.80) | 1 |
| T15 | chain | a → a′ | seq_down_1 | real_down (1.00) | 21 |
| T15 | chain | a′ → a″ | seq_down_1 | seq_down_3 (1.00) | 16 |
| T15 | chain | a → a″ | seq_down_2 | real_down (1.00) | 3 |
| T16 | chain | a → a′ | seq_down_1 | seq_down_1 (0.99) | 1 |
| T16 | chain | a′ → a″ | seq_down_1 | seq_down_1 (0.99) | 1 |
| T16 | chain | a → a″ | seq_down_2 | seq_down_2 (0.58) | 1 |

The built relation is the model's top choice for 21 of 28 designed edges.

## The design check with each kind of edge

| Edges | Cross-mappings that work | Role mapping wins from w = | Analogs vs controls (AUC) | Analog pairs aligned by role |
|---|---|---|---|---|
| computed | 8/8 | T1→T3 0.5, T2→T4 0.75, T5→T6 0.5, T7→T8 0.75, T9→T10 1, T11→T12 0.5, T13→T14 0.25, T15→T16 0.5 | 87% | 24/24 |
| learned | 5/8 | T1→T3 –, T2→T4 0.75, T5→T6 –, T7→T8 0.75, T9→T10 –, T11→T12 0.5, T13→T14 0.25, T15→T16 0.75 | 88% | 12/24 |
| learned + order | 8/8 | T1→T3 0.5, T2→T4 0.75, T5→T6 0.5, T7→T8 0.5, T9→T10 0.5, T11→T12 0.5, T13→T14 0.25, T15→T16 0.5 | 92% | 24/24 |
| learned^5 + order | 8/8 | T1→T3 0.5, T2→T4 0.75, T5→T6 0.25, T7→T8 0.5, T9→T10 0.5, T11→T12 0.5, T13→T14 0.25, T15→T16 0.5 | 84% | 23/24 |
| raw differences | 0/8 | T1→T3 –, T2→T4 –, T5→T6 –, T7→T8 –, T9→T10 –, T11→T12 –, T13→T14 –, T15→T16 – | 60% | 6/24 |

## Theme → variation: themes (of 16) whose mapping relations alone recover

| Condition | computed | learned | learned + order | learned^5 + order | raw differences |
|---|---|---|---|---|---|
| transpose | 16 | 16 | 16 | 16 | 16 |
| mode | 16 | 13 | 16 | 16 | 16 |
| ornament | 16 | 13 | 16 | 16 | 16 |
| augment | 16 | 14 | 16 | 16 | 16 |
| reorder | 15 | 16 | 9 | 8 | 16 |
| motif_retro | 9 | 16 | 6 | 5 | 16 |
| invert | 10 | 7 | 12 | 14 | 0 |
| retrograde | 3 | 12 | 3 | 1 | 10 |

Motif-only matching (w = 0) is the same in every row, since only the edges change.
