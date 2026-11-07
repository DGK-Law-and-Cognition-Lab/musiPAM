# Design check: object vs. relational matching

Exact brute-force graph matching (24 permutations of 4 motifs) — a proxy, **not PAM**. Score = (1-w)·node similarity + w·relation similarity; w=0 is object-only, w=1 relation-only. Relation vectors are standardized per dimension over the whole stimulus set.

Cell entries: **✓** = the theme's motifs map onto their own transformed selves (T2's identical a1/a2 count as one class); **✗** = they do not. The label is where the theme's first motif *a* landed.

## Theme → variation, key/tempo-relative node code

**T1**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ c | ✗ c | ✗ c | ✗ b | ✗ b |
| retrograde | nodes + edges | ✗ a | ✗ a | ✗ a | ✗ a | ✗ a |

**T2**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ b | ✗ c | ✗ c | ✗ c | ✓ a1 |
| retrograde | nodes + edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |

**T3**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ c | ✗ c | ✗ c | ✗ a | ✓ a |
| retrograde | nodes + edges | ✗ b | ✗ b | ✓ a | ✓ a | ✓ a |

**T4**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ c | ✗ c | ✗ c | ✗ c | ✗ c |
| retrograde | nodes + edges | ✗ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |

**T5**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ c | ✗ b | ✗ b | ✗ b | ✗ b |
| retrograde | nodes + edges | ✓ a | ✓ a | ✗ a | ✗ a | ✗ a |

**T6**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ c | ✗ a | ✗ a | ✗ a | ✗ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✗ c |

**T7**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ b | ✗ c | ✓ a1 | ✓ a1 | ✓ a1 |
| retrograde | nodes + edges | ✗ c | ✗ c | ✗ c | ✗ c | ✗ c |

**T8**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ c | ✗ c | ✗ c | ✗ c | ✗ c |
| retrograde | nodes + edges | ✗ c | ✗ c | ✗ c | ✗ c | ✗ c |

**T9**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a' | ✗ a' | ✗ a' | ✗ a' | ✓ a |
| retrograde | nodes + edges | ✗ a' | ✗ a' | ✗ a' | ✗ a' | ✗ a' |

**T10**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✗ a' | ✗ a' | ✗ a' |
| invert | nodes + edges | ✗ b | ✗ b | ✗ a | ✗ a | ✗ a |
| retrograde | nodes + edges | ✗ b | ✗ a' | ✗ a' | ✗ a' | ✗ a' |

**T11**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✗ a' | ✗ a' |
| invert | nodes + edges | ✗ a | ✗ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✗ a | ✗ a' | ✗ a' | ✗ a' | ✗ a' |

**T12**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✗ a' | ✗ a' | ✗ a' |
| invert | nodes + edges | ✗ a' | ✗ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✗ a | ✗ c | ✗ a' | ✗ a' | ✗ a' |

**T13**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✗ a'' | ✗ a'' |
| invert | nodes + edges | ✗ a | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✗ a | ✗ b | ✗ b | ✗ b |

**T14**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✗ a'' |
| invert | nodes + edges | ✗ a'' | ✗ a'' | ✗ a'' | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✗ b | ✗ b | ✗ b |

**T15**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✗ a' | ✗ a' |

**T16**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✗ a'' | ✗ a'' |
| invert | nodes + edges | ✗ a' | ✗ a'' | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✗ a | ✗ a | ✗ a | ✗ a | ✗ a |

## Theme → variation, absolute (piano-roll) node code

**T1**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ c | ✗ c | ✗ c | ✗ b | ✗ b |
| retrograde | nodes + edges | ✓ a | ✗ a | ✗ a | ✗ a | ✗ a |

**T2**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a1 | ✗ a2 | ✗ a2 | ✓ a1 | ✓ a1 |
| retrograde | nodes + edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |

**T3**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ c | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ c | ✗ c | ✗ a | ✗ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T4**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ b | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a1 | ✗ c | ✗ c | ✗ c | ✗ c |
| retrograde | nodes + edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |

**T5**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ c | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a | ✗ b | ✗ b | ✗ b | ✗ b |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✗ a | ✗ a |

**T6**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ b | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a | ✗ a | ✗ a | ✗ a | ✗ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✗ c |

**T7**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ c | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| retrograde | nodes + edges | ✓ a2 | ✓ a2 | ✗ c | ✗ c | ✗ c |

**T8**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ b | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a1 | ✗ c | ✗ c | ✗ c | ✗ c |
| retrograde | nodes + edges | ✗ a2 | ✗ c | ✗ c | ✗ c | ✗ c |

**T9**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ c | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✗ a' | ✗ a' | ✗ a' |

**T10**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ b | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✗ a' | ✗ a' |
| invert | nodes + edges | ✓ a | ✓ a | ✓ a | ✗ a | ✗ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✗ a' | ✗ a' | ✗ a' |

**T11**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✗ a' |
| invert | nodes + edges | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✗ a | ✗ a' | ✗ a' | ✗ a' | ✗ a' |

**T12**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ b | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✗ a' | ✗ a' |
| invert | nodes + edges | ✗ b | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✗ c | ✓ a | ✗ a' | ✗ a' | ✗ a' |

**T13**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ b | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✗ a'' |
| invert | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✗ a | ✗ b | ✗ b |

**T14**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ b | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✗ a'' |
| invert | nodes + edges | ✗ a'' | ✗ a'' | ✗ a'' | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✗ a | ✗ b | ✗ b | ✗ b |

**T15**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✗ a' | ✗ a' |

**T16**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| transpose | probe: pitch coding | ✗ b | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✗ a'' |
| invert | nodes + edges | ✗ a' | ✗ a' | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✗ a' | ✗ a | ✗ a |

## Cross-mappings (truth = relational roles)

Each row is a designed look-alike pair. The label shows where the source motif whose shape the target copies landed in the target theme.

| pair | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| T1 → T3 [rel] | a → ? (look-alike: c) | ✗ c | ✗ c | ✓ a | ✓ a | ✓ a |
| T1 → T3 [abs] | a → ? (look-alike: c) | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| T2 → T4 [rel] | b → ? (look-alike: a1) | ✗ a1 | ✗ a2 | ✗ a2 | ✓ b | ✓ b |
| T2 → T4 [abs] | b → ? (look-alike: a1) | ✗ c | ✓ b | ✓ b | ✓ b | ✓ b |
| T5 → T6 [rel] | a → ? (look-alike: c) | ✗ c | ✓ a | ✓ a | ✓ a | ✓ a |
| T5 → T6 [abs] | a → ? (look-alike: c) | ✗ c | ✗ c | ✗ c | ✓ a | ✓ a |
| T7 → T8 [rel] | a1 → ? (look-alike: c) | ✗ b | ✗ b | ✗ b | ✓ a1 | ✓ a1 |
| T7 → T8 [abs] | a1 → ? (look-alike: c) | ✗ b | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| T9 → T10 [rel] | c → ? (look-alike: b) | ✗ b | ✗ b | ✗ b | ✗ b | ✓ c |
| T9 → T10 [abs] | c → ? (look-alike: b) | ✗ b | ✗ b | ✗ b | ✓ c | ✓ c |
| T11 → T12 [rel] | b → ? (look-alike: a) | ✗ a | ✓ b | ✓ b | ✓ b | ✓ b |
| T11 → T12 [abs] | b → ? (look-alike: a) | ✗ c | ✓ b | ✓ b | ✓ b | ✓ b |
| T13 → T14 [rel] | a'' → ? (look-alike: b) | ✗ b | ✓ a'' | ✓ a'' | ✓ a'' | ✓ a'' |
| T13 → T14 [abs] | a'' → ? (look-alike: b) | ✗ b | ✓ a'' | ✓ a'' | ✓ a'' | ✓ a'' |
| T15 → T16 [rel] | b → ? (look-alike: a) | ✗ a' | ✗ a'' | ✓ b | ✓ b | ✓ b |
| T15 → T16 [abs] | b → ? (look-alike: a) | ✗ a | ✗ b | ✓ b | ✓ b | ✓ b |

## Relational similarity between themes

Mean standardized relation similarity (w = 1). *Role* aligns motifs by position; *best* is the maximum over all 24 alignments. Designed analogs (same skeleton) should be more similar than pairs with different skeletons, and best aligned by role.

- **Designed analogs (24 pairs):** mean role similarity 0.50; best alignment is the role alignment in 23/24.
- **Different skeletons (96 pairs):** mean role similarity 0.28 (max 0.65).
- **Separation:** a random analog pair beats a random control pair 86% of the time (AUC).

| analog pair | skeleton | role | best | best is role |
|---|---|---|---|---|
| T1 → T3 | sentence | 0.32 | 0.32 | yes |
| T1 → T5 | sentence | 0.92 | 0.92 | yes |
| T1 → T6 | sentence | 0.43 | 0.43 | yes |
| T2 → T4 | period | 0.50 | 0.50 | yes |
| T2 → T7 | period | 0.55 | 0.55 | yes |
| T2 → T8 | period | 0.52 | 0.52 | yes |
| T3 → T5 | sentence | 0.36 | 0.36 | yes |
| T3 → T6 | sentence | 0.26 | 0.30 | no |
| T4 → T7 | period | 0.50 | 0.50 | yes |
| T4 → T8 | period | 0.26 | 0.26 | yes |
| T5 → T6 | sentence | 0.41 | 0.41 | yes |
| T7 → T8 | period | 0.50 | 0.50 | yes |
| T9 → T10 | rounded | 0.44 | 0.44 | yes |
| T9 → T11 | rounded | 0.60 | 0.60 | yes |
| T9 → T12 | rounded | 0.56 | 0.56 | yes |
| T10 → T11 | rounded | 0.37 | 0.37 | yes |
| T10 → T12 | rounded | 0.36 | 0.36 | yes |
| T11 → T12 | rounded | 0.79 | 0.79 | yes |
| T13 → T14 | chain | 0.52 | 0.52 | yes |
| T13 → T15 | chain | 0.71 | 0.71 | yes |
| T13 → T16 | chain | 0.75 | 0.75 | yes |
| T14 → T15 | chain | 0.49 | 0.49 | yes |
| T14 → T16 | chain | 0.54 | 0.54 | yes |
| T15 → T16 | chain | 0.41 | 0.41 | yes |

Without standardization the relational similarity of the role mapping is 0.48 (T1→T3) vs 0.47 (T1→T2): positional relations, identical for any two 4-motif passages, swamp the derivational ones. Standardization is therefore required, and the real PAM implementation will need an equivalent normalization of musical relation vectors.
