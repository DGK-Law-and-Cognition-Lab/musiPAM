# Design check with learned representations (MERT-v1-95M)

Same exact matcher as design_check.md (a proxy, not PAM), with motif nodes coded by MERT embeddings of the audio participants hear. Unlike the symbolic codes, MERT also sees timbre and tempo, so those conditions are included. ✓ = the theme's motifs map onto their own transformed selves (identical a1/a2 count as one class); the label is where the theme's first motif landed.

## MERT motifs + computed relations

**T1**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ b | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ c | ✗ c | ✗ b | ✗ b | ✗ b |
| retrograde | nodes + edges | ✓ a | ✗ a | ✗ a | ✗ a | ✗ a |

**T2**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a2 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| tempo | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| transpose | probe: pitch coding | ✗ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a2 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| retrograde | nodes + edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |

**T3**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a | ✗ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T4**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| tempo | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| transpose | probe: pitch coding | ✗ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a1 | ✗ b | ✗ c | ✗ c | ✗ c |
| retrograde | nodes + edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |

**T5**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
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
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✗ a' | ✗ a' |
| invert | nodes + edges | ✗ a' | ✗ a | ✗ a | ✗ a | ✗ a |
| retrograde | nodes + edges | ✓ a | ✗ a | ✗ b | ✗ b | ✗ b |

**T7**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| tempo | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| transpose | probe: pitch coding | ✗ b | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| retrograde | nodes + edges | ✓ a1 | ✗ c | ✗ c | ✗ c | ✗ c |

**T8**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a2 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| tempo | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| transpose | probe: pitch coding | ✗ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a1 | ✗ c | ✗ c | ✗ c | ✗ c |
| retrograde | nodes + edges | ✓ a1 | ✗ c | ✗ c | ✗ c | ✗ c |

**T9**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✗ a' | ✗ a' | ✗ a' |

**T10**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✗ a' | ✗ a' | ✗ a' | ✗ a' |
| invert | nodes + edges | ✓ a | ✗ a | ✗ a | ✗ a | ✗ a |
| retrograde | nodes + edges | ✓ a | ✗ a' | ✗ a' | ✗ a' | ✗ a' |

**T11**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ c | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✗ a' | ✗ a' | ✗ a' | ✗ a' |
| invert | nodes + edges | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✗ a' | ✗ a' | ✗ a' | ✗ a' |

**T12**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✗ a | ✗ a | ✗ a | ✗ a |
| motif_retro | temporal edges | ✓ a | ✗ a' | ✗ a' | ✗ a' | ✗ a' |
| invert | nodes + edges | ✗ a | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✗ a' | ✗ a' | ✗ a' | ✗ a' |

**T13**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ b | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✗ a'' | ✗ a'' | ✗ a'' |
| invert | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✗ b | ✗ b | ✗ b | ✗ b |

**T14**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✗ a'' |
| invert | nodes + edges | ✗ a'' | ✗ a'' | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✗ b | ✗ b | ✗ b | ✗ b |

**T15**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✗ a' | ✗ a' | ✗ a' |

**T16**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ b | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✗ a'' | ✗ a'' | ✗ a'' | ✗ a'' |
| invert | nodes + edges | ✗ a'' | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✗ a | ✗ a | ✗ a | ✗ a |

**Cross-mappings** (label = where the source motif landed; look-alike in brackets)

| pair | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| T1 → T3 | a → ? [c, MERT rank 2] | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| T2 → T4 | b → ? [a1, MERT rank 3] | ✓ b | ✓ b | ✓ b | ✓ b | ✓ b |
| T5 → T6 | a → ? [c, MERT rank 3] | ✗ c | ✓ a | ✓ a | ✓ a | ✓ a |
| T7 → T8 | a1 → ? [c, MERT rank 1] | ✗ c | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| T9 → T10 | c → ? [b, MERT rank 1] | ✗ b | ✗ b | ✓ c | ✓ c | ✓ c |
| T11 → T12 | b → ? [a, MERT rank 2] | ✗ a' | ✓ b | ✓ b | ✓ b | ✓ b |
| T13 → T14 | a'' → ? [b, MERT rank 1] | ✗ a' | ✓ a'' | ✓ a'' | ✓ a'' | ✓ a'' |
| T15 → T16 | b → ? [a, MERT rank 3] | ✗ a | ✓ b | ✓ b | ✓ b | ✓ b |

**Relational similarity between themes** (w = 1)

- Designed analogs (24): mean role similarity 0.50; role alignment is best in 24/24.
- Different skeletons (96): mean role similarity 0.28.
- Separation (AUC): 87%.

## MERT motifs + MERT difference-vector relations (fully learned)

**T1**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ b | ✗ b | ✗ b | ✗ b | ✗ a' |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ c | ✗ c | ✗ c | ✗ c | ✗ c |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T2**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| tempo | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| transpose | probe: pitch coding | ✗ a1 | ✗ a1 | ✗ a1 | ✗ a1 | ✗ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a2 | ✗ a2 | ✗ a2 | ✗ a2 | ✗ a2 |
| retrograde | nodes + edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |

**T3**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a' | ✗ a' | ✗ a' | ✗ a' | ✗ a' |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a | ✗ a | ✗ a | ✗ a | ✗ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T4**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| tempo | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| transpose | probe: pitch coding | ✗ a1 | ✗ a1 | ✗ a1 | ✗ a1 | ✗ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a1 | ✗ a1 | ✗ a1 | ✗ a1 | ✗ a1 |
| retrograde | nodes + edges | ✓ a2 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |

**T5**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a' | ✗ a' | ✗ a' | ✗ a' | ✗ a' |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ c | ✗ c | ✗ c | ✗ c | ✗ c |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T6**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a | ✗ a | ✗ a | ✗ a | ✗ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a' | ✗ a' | ✗ a' | ✗ a' | ✗ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T7**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| tempo | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| transpose | probe: pitch coding | ✗ b | ✗ b | ✗ b | ✗ b | ✗ b |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a1 | ✗ a1 | ✗ a1 | ✗ a1 | ✗ a1 |
| retrograde | nodes + edges | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |

**T8**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a2 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| tempo | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| transpose | probe: pitch coding | ✗ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| retrograde | nodes + edges | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |

**T9**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a | ✗ c | ✗ c | ✗ c | ✗ c |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a' | ✗ a' | ✗ a' | ✗ a' | ✗ a' |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T10**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a' | ✓ a | ✗ a | ✗ a | ✗ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T11**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ c | ✗ b | ✗ b | ✗ b | ✗ b |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a' | ✗ a' | ✗ a' | ✗ a' | ✗ a' |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T12**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a' | ✓ a | ✓ a | ✓ a | ✓ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a | ✗ c | ✗ c | ✗ c | ✗ c |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T13**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ b | ✗ b | ✗ b | ✗ b | ✗ b |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T14**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a' | ✗ a' | ✗ a' | ✗ a' | ✗ a' |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a'' | ✗ a'' | ✗ a'' | ✗ a'' | ✗ a'' |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T15**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ a' | ✗ a' | ✗ a' | ✗ a' | ✗ a' |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a | ✗ a | ✗ a | ✗ a | ✗ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T16**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ b | ✗ a | ✗ a | ✗ a | ✗ a |
| mode | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| ornament | nodes only | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| augment | probe: time coding | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| reorder | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| motif_retro | temporal edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| invert | nodes + edges | ✗ a'' | ✗ b | ✗ b | ✗ b | ✗ b |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**Cross-mappings** (label = where the source motif landed; look-alike in brackets)

| pair | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| T1 → T3 | a → ? [c, MERT rank 2] | ✗ a' | ✗ a' | ✗ a' | ✗ a' | ✗ a' |
| T2 → T4 | b → ? [a1, MERT rank 3] | ✓ b | ✓ b | ✓ b | ✓ b | ✓ b |
| T5 → T6 | a → ? [c, MERT rank 3] | ✗ c | ✗ c | ✗ c | ✗ c | ✗ c |
| T7 → T8 | a1 → ? [c, MERT rank 1] | ✗ c | ✗ c | ✗ c | ✗ c | ✗ c |
| T9 → T10 | c → ? [b, MERT rank 1] | ✗ b | ✗ b | ✗ b | ✗ b | ✗ b |
| T11 → T12 | b → ? [a, MERT rank 2] | ✗ a' | ✗ a' | ✗ a' | ✗ a' | ✗ a' |
| T13 → T14 | a'' → ? [b, MERT rank 1] | ✗ a' | ✗ a' | ✗ a' | ✗ a' | ✗ a' |
| T15 → T16 | b → ? [a, MERT rank 3] | ✗ a | ✗ a' | ✗ a' | ✗ a' | ✗ a' |

**Relational similarity between themes** (w = 1)

- Designed analogs (24): mean role similarity 0.02; role alignment is best in 3/24.
- Different skeletons (96): mean role similarity 0.01.
- Separation (AUC): 54%.

