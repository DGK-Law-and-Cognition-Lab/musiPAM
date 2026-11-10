# musiPAM relations ("music BART")

A learned model of the relation between two motifs, so that musiPAM's graph edges can come from learning rather than from features we designed. It follows BART for words: one classifier per relation, trained on labeled examples, and a pair is represented by its profile of probabilities over all the relations. The full rationale is in [`../docs/RELATION_MODEL.md`](../docs/RELATION_MODEL.md).

Music has one advantage over words: a relation is an operation on a score, so correctly labeled examples can be generated in any number. Here they are generated from about 12,700 traditional tunes that ship with music21, never from the musiPAM stimuli.

## Results so far (v0, symbolic motif code)

- It recognizes the relation of a new pair 96% of the time on new Essen tunes, and 89% on the Irish and Scottish collections (chance 4%).
- It solves four-term analogies 99% and 95% of the time; raw differences between motif codes manage 64%.
- It names 21 of the 28 relations the musiPAM skeletons were built on, though it never saw a musiPAM motif.
- As musiPAM's edges (with the three positional features), it makes all eight cross-mappings work and separates analogs from controls better than the hand-built relations (AUC 92% vs 87%; all 24 analog pairs aligned by role with either).
- It does not yet recognize two relations applied together, and in minor keys it mistakes some sequences for real transpositions.

Details: [`reports/track_a_symbolic.md`](reports/track_a_symbolic.md) and [`reports/musipam_learned_edges.md`](reports/musipam_learned_edges.md).

## Run it

Use the same Python environment as `stimgen` (`~/.venvs/musipam`). From this folder:

```bash
~/.venvs/musipam/bin/python build_corpus.py
```

```bash
~/.venvs/musipam/bin/python build_pairs.py
```

```bash
~/.venvs/musipam/bin/python train_bart.py
```

```bash
~/.venvs/musipam/bin/python apply_musipam.py
```

```bash
~/.venvs/musipam/bin/python examples.py
```

```bash
~/.venvs/musipam/bin/python audit_examples.py
```

| Step | What it does | Time |
|---|---|---|
| `build_corpus.py` | Cuts the Essen, O'Neill, Aird and Ryan collections into two-bar motifs | ~5 min |
| `build_pairs.py` | Makes labeled pairs: one per relation per base motif, plus held-out compositions and relations found in real tunes | seconds |
| `train_bart.py` | Track A: fits the relation model on the symbolic motif code and tests it → `reports/track_a_symbolic.md` | a few minutes |
| `apply_musipam.py` | Uses the model's relation vectors as the edges of the 176 musiPAM stimuli and reruns the design check → `reports/musipam_learned_edges.md` | ~1 min |
| `examples.py` | Writes one example per relation as MusicXML → `examples/` | seconds |
| `audit_examples.py` | Reads each example back from its MusicXML, checks it against the relation's definition with independent rules, and scores it with the model → `examples/AUDIT.md` | seconds |

Generated data and trained weights go to `~/musipam-data/relations` (set `MUSIPAM_REL_DATA` to move it). They stay outside Google Drive and out of git, because they are large, rebuildable, and derived from collections whose terms we haven't checked for redistribution.

## What's where

```
relations/
├── build_corpus.py  build_pairs.py  train_bart.py  apply_musipam.py  examples.py
├── musipam_rel/
│   ├── motif.py      motifs in key-relative scale steps; loader for the musiPAM stimuli
│   ├── relations.py  THE INVENTORY: the 26 relations and the transforms that make them
│   ├── features.py   the generic symbolic motif code and the pair encoding
│   └── bart.py       the BART-style model (one logistic classifier per relation) and test helpers
├── reports/          results (committed)
└── examples/         one MusicXML example per relation, for checking by ear, and their audit (AUDIT.md)
```

## Changing the inventory

Every relation is a short function in `musipam_rel/relations.py`, listed in `RELATIONS` with a one-line description. To drop one, delete its line from `RELATIONS`; to add one, add a line and a branch in `make()`. Then rerun `build_pairs.py` and `train_bart.py`. Check new transforms by ear with `examples.py` first.

## Next steps

1. **Audit the inventory by ear** (D. Kamper). The rule-and-model audit is done (2026-11-09, [`examples/AUDIT.md`](examples/AUDIT.md)): all 26 examples match their definitions, and the model ranks the illustrated relation first in all 26. Whether each B is a fair, musical instance of its relation still needs a listener: open `examples/` in MuseScore, or play them on the audition page. Three points to judge by ear: `ornament` only ever adds passing tones in thirds and upper-neighbor figures at the ends of long notes; `octave_down`, `seq_down_2` and `seq_down_3` fall below the stimuli's melodic range at the examples' register; and `opening_kept` (p = 0.54) is the relation the model is least sure of, next to its close relative `consequent`.
2. **Track A on learned motif codes.** Swap the symbolic code for MERT (render a subset of pairs to audio with stimgen's renderer) and for CLaMP 3's symbolic encoder. This asks which music models carry which relations.
3. **Track B.** A small trained encoder over the notes of both motifs, for the relations Track A misses.
4. **Natural test sets** beyond the within-tune search: fugue subjects and answers, theme-and-variation sets.
5. **Study 1c.** Freeze the model and its predictions for the musiPAM relation pairs before the study is registered.
