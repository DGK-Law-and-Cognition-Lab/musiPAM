# PAM on the musiPAM stimuli

PAM is the lab's model (Lu, Ichien & Holyoak, 2022), run through a Python port of `TestMapping_PAMfunc.m` that matches the MATLAB original to machine precision (`validate.py`). α is PAM's node weight (`objweight`): α = 0 maps by relations only; larger α gives motif similarity more weight. The paper used α = 0.1 for word triplets, 1 for texts, and 2 vs 1 for younger vs older children.

## Summary

| Node code | Edge code | Cross-mappings: role match with relations only | Cross-mappings: look-alike at higher α too | Analogs vs controls (AUC of the analogy score, α = 0 / 1 / 4) | Analogs mapped by role (α = 0 / 1 / 4) |
|---|---|---|---|---|---|
| key-relative motifs | computed relations (raw) | 5/8 | 5/8 | 67% / 64% / 60% | 16 / 9 / 5 of 24 |
| key-relative motifs | computed relations (standardized) | 8/8 | 8/8 | 80% / 68% / 64% | 21 / 15 / 5 of 24 |
| key-relative motifs | learned relations | 8/8 | 7/8 | 73% / 64% / 56% | 24 / 23 / 6 of 24 |
| key-relative motifs | learned relations, 5th power | 8/8 | 6/8 | 71% / 60% / 56% | 24 / 23 / 6 of 24 |
| absolute-pitch motifs | computed relations (standardized) | 8/8 | 3/8 | 80% / 76% / 45% | 21 / 19 / 5 of 24 |
| MERT motifs | computed relations (standardized) | 8/8 | 2/8 | 80% / 78% / 71% | 21 / 19 / 15 of 24 |
| MERT motifs | learned relations, 5th power | 8/8 | 0/8 | 71% / 71% / 74% | 24 / 24 / 24 of 24 |

## key-relative motifs, computed relations (raw)

**Cross-mappings: where the probe lands** (role = the motif in the probe's role; look-alike = the designed copy of its shape)

| Pair | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| T1 → T3 | a (role) | a (role) | a (role) | a (role) | c (look-alike) | c (look-alike) |
| T2 → T4 | b (role) | b (role) | b (role) | a1 (look-alike) | a1 (look-alike) | a1 (look-alike) |
| T5 → T6 | c (look-alike) | c (look-alike) | c (look-alike) | c (look-alike) | c (look-alike) | c (look-alike) |
| T7 → T8 | b (look-alike) | b (look-alike) | b (look-alike) | b (look-alike) | b (look-alike) | b (look-alike) |
| T9 → T10 | b (look-alike) | b (look-alike) | b (look-alike) | b (look-alike) | b (look-alike) | b (look-alike) |
| T11 → T12 | b (role) | b (role) | b (role) | a (look-alike) | a (look-alike) | a (look-alike) |
| T13 → T14 | a″ (role) | a″ (role) | a″ (role) | a″ (role) | b (look-alike) | b (look-alike) |
| T15 → T16 | b (role) | b (role) | b (role) | a″ (look-alike) | a′ (look-alike) | a′ (look-alike) |

**Theme → variation: themes (of 16) mapped correctly**

| Condition | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| transpose | 16 | 16 | 16 | 16 | 16 | 15 |
| mode | 16 | 16 | 16 | 16 | 16 | 15 |
| ornament | 16 | 16 | 16 | 16 | 16 | 16 |
| augment | 16 | 16 | 16 | 16 | 16 | 15 |
| reorder | 14 | 15 | 16 | 16 | 16 | 15 |
| motif_retro | 7 | 10 | 10 | 13 | 14 | 15 |
| invert | 7 | 7 | 7 | 2 | 0 | 0 |
| retrograde | 1 | 1 | 1 | 3 | 4 | 6 |

## key-relative motifs, computed relations (standardized)

**Cross-mappings: where the probe lands** (role = the motif in the probe's role; look-alike = the designed copy of its shape)

| Pair | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| T1 → T3 | a (role) | a (role) | a (role) | a (role) | c (look-alike) | c (look-alike) |
| T2 → T4 | b (role) | b (role) | b (role) | a1 (look-alike) | a1 (look-alike) | a1 (look-alike) |
| T5 → T6 | a (role) | a (role) | a (role) | c (look-alike) | c (look-alike) | c (look-alike) |
| T7 → T8 | a1 (role) | a1 (role) | a1 (role) | b (look-alike) | b (look-alike) | b (look-alike) |
| T9 → T10 | c (role) | c (role) | b (look-alike) | b (look-alike) | b (look-alike) | b (look-alike) |
| T11 → T12 | b (role) | b (role) | b (role) | b (role) | a (look-alike) | a (look-alike) |
| T13 → T14 | a″ (role) | a″ (role) | a″ (role) | a″ (role) | a″ (role) | b (look-alike) |
| T15 → T16 | b (role) | b (role) | b (role) | b (role) | a″ (look-alike) | a′ (look-alike) |

**Theme → variation: themes (of 16) mapped correctly**

| Condition | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| transpose | 16 | 16 | 16 | 16 | 16 | 15 |
| mode | 16 | 16 | 16 | 16 | 16 | 15 |
| ornament | 16 | 16 | 16 | 16 | 16 | 16 |
| augment | 16 | 16 | 16 | 16 | 16 | 15 |
| reorder | 15 | 15 | 15 | 16 | 16 | 15 |
| motif_retro | 11 | 11 | 12 | 13 | 14 | 15 |
| invert | 7 | 7 | 7 | 5 | 2 | 0 |
| retrograde | 2 | 2 | 2 | 4 | 5 | 5 |

## key-relative motifs, learned relations

**Cross-mappings: where the probe lands** (role = the motif in the probe's role; look-alike = the designed copy of its shape)

| Pair | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| T1 → T3 | a (role) | a (role) | a (role) | a (role) | a (role) | c (look-alike) |
| T2 → T4 | b (role) | b (role) | b (role) | a1 (look-alike) | a1 (look-alike) | a1 (look-alike) |
| T5 → T6 | a (role) | a (role) | a (role) | a (role) | a (role) | a′ (other) |
| T7 → T8 | a1 (role) | a1 (role) | a1 (role) | a1 (role) | b (look-alike) | b (look-alike) |
| T9 → T10 | c (role) | c (role) | c (role) | c (role) | b (look-alike) | b (look-alike) |
| T11 → T12 | b (role) | b (role) | b (role) | b (role) | a (look-alike) | a (look-alike) |
| T13 → T14 | a″ (role) | a″ (role) | a″ (role) | a″ (role) | a″ (role) | b (look-alike) |
| T15 → T16 | b (role) | b (role) | b (role) | b (role) | a″ (look-alike) | a′ (look-alike) |

**Theme → variation: themes (of 16) mapped correctly**

| Condition | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| transpose | 16 | 16 | 16 | 16 | 16 | 15 |
| mode | 16 | 16 | 16 | 16 | 16 | 15 |
| ornament | 16 | 16 | 16 | 16 | 16 | 16 |
| augment | 16 | 16 | 16 | 16 | 16 | 15 |
| reorder | 1 | 1 | 4 | 8 | 14 | 15 |
| motif_retro | 0 | 0 | 0 | 2 | 5 | 13 |
| invert | 16 | 16 | 16 | 15 | 1 | 0 |
| retrograde | 0 | 0 | 0 | 0 | 1 | 2 |

## key-relative motifs, learned relations, 5th power

**Cross-mappings: where the probe lands** (role = the motif in the probe's role; look-alike = the designed copy of its shape)

| Pair | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| T1 → T3 | a (role) | a (role) | a (role) | a (role) | a (role) | a (role) |
| T2 → T4 | b (role) | b (role) | b (role) | a1 (look-alike) | a1 (look-alike) | a1 (look-alike) |
| T5 → T6 | a (role) | a (role) | a (role) | a (role) | a (role) | a′ (other) |
| T7 → T8 | a1 (role) | a1 (role) | a1 (role) | a1 (role) | b (look-alike) | b (look-alike) |
| T9 → T10 | c (role) | c (role) | c (role) | c (role) | b (look-alike) | b (look-alike) |
| T11 → T12 | b (role) | b (role) | b (role) | b (role) | a (look-alike) | a (look-alike) |
| T13 → T14 | a″ (role) | a″ (role) | a″ (role) | a″ (role) | a″ (role) | b (look-alike) |
| T15 → T16 | b (role) | b (role) | b (role) | b (role) | a″ (look-alike) | a′ (look-alike) |

**Theme → variation: themes (of 16) mapped correctly**

| Condition | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| transpose | 16 | 16 | 16 | 16 | 16 | 15 |
| mode | 16 | 16 | 16 | 16 | 16 | 15 |
| ornament | 16 | 16 | 16 | 16 | 16 | 16 |
| augment | 16 | 16 | 16 | 16 | 16 | 15 |
| reorder | 0 | 0 | 0 | 7 | 14 | 15 |
| motif_retro | 0 | 0 | 0 | 1 | 4 | 13 |
| invert | 16 | 16 | 16 | 16 | 1 | 0 |
| retrograde | 0 | 0 | 0 | 0 | 0 | 2 |

## absolute-pitch motifs, computed relations (standardized)

**Cross-mappings: where the probe lands** (role = the motif in the probe's role; look-alike = the designed copy of its shape)

| Pair | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| T1 → T3 | a (role) | a (role) | a (role) | a (role) | a (role) | a (role) |
| T2 → T4 | b (role) | b (role) | b (role) | b (role) | b (role) | b (role) |
| T5 → T6 | a (role) | a (role) | a (role) | a (role) | c (look-alike) | c (look-alike) |
| T7 → T8 | a1 (role) | a1 (role) | a1 (role) | a1 (role) | b (look-alike) | b (look-alike) |
| T9 → T10 | c (role) | c (role) | b (look-alike) | b (look-alike) | b (look-alike) | b (look-alike) |
| T11 → T12 | b (role) | b (role) | b (role) | b (role) | b (role) | c (other) |
| T13 → T14 | a″ (role) | a″ (role) | a″ (role) | a″ (role) | a″ (role) | a″ (role) |
| T15 → T16 | b (role) | b (role) | b (role) | b (role) | b (role) | b (role) |

**Theme → variation: themes (of 16) mapped correctly**

| Condition | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| transpose | 16 | 16 | 16 | 16 | 16 | 2 |
| mode | 16 | 16 | 16 | 16 | 16 | 16 |
| ornament | 16 | 16 | 16 | 16 | 16 | 15 |
| augment | 16 | 16 | 16 | 16 | 16 | 15 |
| reorder | 15 | 15 | 15 | 16 | 16 | 15 |
| motif_retro | 11 | 12 | 13 | 14 | 16 | 15 |
| invert | 7 | 7 | 7 | 6 | 4 | 2 |
| retrograde | 2 | 2 | 2 | 5 | 9 | 13 |

## MERT motifs, computed relations (standardized)

**Cross-mappings: where the probe lands** (role = the motif in the probe's role; look-alike = the designed copy of its shape)

| Pair | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| T1 → T3 | a (role) | a (role) | a (role) | a (role) | a (role) | a (role) |
| T2 → T4 | b (role) | b (role) | b (role) | b (role) | b (role) | b (role) |
| T5 → T6 | a (role) | a (role) | a (role) | a (role) | a (role) | c (look-alike) |
| T7 → T8 | a1 (role) | a1 (role) | a1 (role) | a1 (role) | a1 (role) | a1 (role) |
| T9 → T10 | c (role) | c (role) | c (role) | b (look-alike) | b (look-alike) | b (look-alike) |
| T11 → T12 | b (role) | b (role) | b (role) | b (role) | b (role) | b (role) |
| T13 → T14 | a″ (role) | a″ (role) | a″ (role) | a″ (role) | a″ (role) | a″ (role) |
| T15 → T16 | b (role) | b (role) | b (role) | b (role) | b (role) | b (role) |

**Theme → variation: themes (of 16) mapped correctly**

| Condition | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| transpose | 16 | 16 | 16 | 16 | 16 | 16 |
| mode | 16 | 16 | 16 | 16 | 16 | 16 |
| ornament | 16 | 16 | 16 | 16 | 16 | 16 |
| augment | 16 | 16 | 16 | 16 | 16 | 16 |
| reorder | 15 | 15 | 15 | 16 | 16 | 16 |
| motif_retro | 11 | 11 | 12 | 12 | 13 | 13 |
| invert | 7 | 7 | 7 | 7 | 5 | 5 |
| retrograde | 2 | 2 | 2 | 2 | 4 | 7 |

## MERT motifs, learned relations, 5th power

**Cross-mappings: where the probe lands** (role = the motif in the probe's role; look-alike = the designed copy of its shape)

| Pair | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| T1 → T3 | a (role) | a (role) | a (role) | a (role) | a (role) | a (role) |
| T2 → T4 | b (role) | b (role) | b (role) | b (role) | b (role) | b (role) |
| T5 → T6 | a (role) | a (role) | a (role) | a (role) | a (role) | a (role) |
| T7 → T8 | a1 (role) | a1 (role) | a1 (role) | a1 (role) | a1 (role) | a1 (role) |
| T9 → T10 | c (role) | c (role) | c (role) | c (role) | c (role) | c (role) |
| T11 → T12 | b (role) | b (role) | b (role) | b (role) | b (role) | b (role) |
| T13 → T14 | a″ (role) | a″ (role) | a″ (role) | a″ (role) | a″ (role) | a″ (role) |
| T15 → T16 | b (role) | b (role) | b (role) | b (role) | b (role) | b (role) |

**Theme → variation: themes (of 16) mapped correctly**

| Condition | α = 0 | α = 0.25 | α = 0.5 | α = 1 | α = 2 | α = 4 |
|---|---|---|---|---|---|---|
| transpose | 16 | 16 | 16 | 16 | 16 | 16 |
| mode | 16 | 16 | 16 | 16 | 16 | 16 |
| ornament | 16 | 16 | 16 | 16 | 16 | 16 |
| augment | 16 | 16 | 16 | 16 | 16 | 16 |
| reorder | 0 | 0 | 0 | 0 | 4 | 12 |
| motif_retro | 0 | 0 | 0 | 0 | 0 | 0 |
| invert | 16 | 16 | 16 | 16 | 16 | 11 |
| retrograde | 0 | 0 | 0 | 0 | 0 | 0 |
