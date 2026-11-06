# Design check with learned representations (MERT-v1-95M)

Same exact matcher as design_check.md (a proxy, not PAM), with motif nodes coded by MERT embeddings of the audio participants hear. Unlike the symbolic codes, MERT also sees timbre and tempo, so those conditions are included. ✓ = the theme's motifs map onto their own transformed selves (identical a1/a2 count as one class); the label is where the theme's first motif landed.

## MERT motifs + computed relations

**T1**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ c | ✓ a | ✓ a | ✓ a | ✓ a |
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
| timbre | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| tempo | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| transpose | probe: pitch coding | ✗ c | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ c | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| retrograde | nodes + edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |

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
| invert | nodes + edges | ✗ a | ✓ a | ✓ a | ✓ a | ✓ a |
| retrograde | nodes + edges | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |

**T4**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| tempo | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| transpose | probe: pitch coding | ✗ c | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| retrograde | nodes + edges | ✓ a1 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |

**Cross-theme analogs** (label = where the cross-mapped source motif landed)

| pair | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| T1 → T3 | a → ? | ✗ b | ✓ a | ✓ a | ✓ a | ✓ a |
| T2 → T4 | b → ? | ✗ c | ✓ b | ✓ b | ✓ b | ✓ b |

**Relational similarity between themes** (role alignment / best of 24)

| pair | kind | role | best | best is role |
|---|---|---|---|---|
| T1 → T2 | different skeleton | 0.20 | 0.26 | no |
| T1 → T3 | **analog** | 0.39 | 0.39 | yes |
| T1 → T4 | different skeleton | 0.07 | 0.21 | no |
| T2 → T3 | different skeleton | 0.16 | 0.16 | yes |
| T2 → T4 | **analog** | 0.58 | 0.58 | yes |
| T3 → T4 | different skeleton | 0.10 | 0.30 | no |

## MERT motifs + MERT difference-vector relations (fully learned)

**T1**

| condition | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| timbre | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| tempo | surface | ✓ a | ✓ a | ✓ a | ✓ a | ✓ a |
| transpose | probe: pitch coding | ✗ c | ✓ a | ✓ a | ✓ a | ✓ a |
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
| timbre | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| tempo | surface | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| transpose | probe: pitch coding | ✗ c | ✗ c | ✗ c | ✗ c | ✗ c |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ c | ✗ c | ✗ c | ✗ c | ✗ c |
| retrograde | nodes + edges | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |

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
| transpose | probe: pitch coding | ✗ c | ✗ c | ✗ c | ✗ c | ✗ c |
| mode | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| ornament | nodes only | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| augment | probe: time coding | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| reorder | temporal edges | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |
| motif_retro | temporal edges | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 | ✓ a2 |
| invert | nodes + edges | ✗ a1 | ✗ a1 | ✗ a1 | ✗ a1 | ✗ a1 |
| retrograde | nodes + edges | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 | ✓ a1 |

**Cross-theme analogs** (label = where the cross-mapped source motif landed)

| pair | grid cell | w=0 | w=0.25 | w=0.5 | w=0.75 | w=1 |
|---|---|---|---|---|---|---|
| T1 → T3 | a → ? | ✗ b | ✗ a | ✗ a | ✗ a | ✗ a |
| T2 → T4 | b → ? | ✗ c | ✗ c | ✗ c | ✗ c | ✗ c |

**Relational similarity between themes** (role alignment / best of 24)

| pair | kind | role | best | best is role |
|---|---|---|---|---|
| T1 → T2 | different skeleton | -0.01 | 0.14 | no |
| T1 → T3 | **analog** | -0.03 | 0.11 | no |
| T1 → T4 | different skeleton | -0.15 | 0.11 | no |
| T2 → T3 | different skeleton | -0.15 | 0.24 | no |
| T2 → T4 | **analog** | 0.12 | 0.16 | no |
| T3 → T4 | different skeleton | -0.02 | 0.21 | no |

