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
| invert | nodes + edges | ✗ b | ✗ b | ✗ b | ✓ a1 | ✓ a1 |
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
| invert | nodes + edges | ✗ c | ✗ c | ✗ a | ✓ a | ✓ a |
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
| invert | nodes + edges | ✗ c | ✗ b | ✗ b | ✗ b | ✓ a1 |
| retrograde | nodes + edges | ✗ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |

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
| invert | nodes + edges | ✗ a1 | ✗ a2 | ✓ a1 | ✓ a1 | ✓ a1 |
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
| invert | nodes + edges | ✗ c | ✗ a | ✗ a | ✓ a | ✓ a |
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
| invert | nodes + edges | ✗ a1 | ✗ b | ✗ b | ✓ a1 | ✓ a1 |
| retrograde | nodes + edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |

## Cross-theme mapping of the designed analogs (truth = relational roles)

The label shows where the *cross-mapped* source motif landed: T1's a (whose shape T3's c copies) and T2's b (whose shape T4's a1/a2 copy).

| pair | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| T1 → T3 [rel] | a → ? | ✗ c | ✗ c | ✓ a | ✓ a | ✓ a |
| T1 → T3 [abs] | a → ? | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| T2 → T4 [rel] | b → ? | ✗ a1 | ✗ a2 | ✓ b | ✓ b | ✓ b |
| T2 → T4 [abs] | b → ? | ✗ c | ✓ b | ✓ b | ✓ b | ✓ b |

## Relational similarity between themes

Mean standardized relation similarity (w = 1). *Role map* aligns motifs by position; *best* is the maximum over all 24 alignments. Designed analogs should be the most similar pairs and be best aligned by role.

| pair | kind | role map | best | best alignment is the role map |
|---|---|---|---|---|
| T1 → T2 | different skeleton | 0.20 | 0.26 | no |
| T1 → T3 | **designed analog** | 0.39 | 0.39 | yes |
| T1 → T4 | different skeleton | 0.07 | 0.21 | no |
| T2 → T3 | different skeleton | 0.16 | 0.16 | yes |
| T2 → T4 | **designed analog** | 0.58 | 0.58 | yes |
| T3 → T4 | different skeleton | 0.10 | 0.30 | no |

Without standardization the relational similarity of the role mapping is 0.48 (T1→T3) vs 0.47 (T1→T2): positional relations, identical for any two 4-motif passages, swamp the derivational ones. Standardization is therefore required, and the real PAM implementation will need an equivalent normalization of musical relation vectors.
