"""Write one example pair per relation as MusicXML, to check the transforms by eye and ear.

    ~/.venvs/musipam/bin/python examples.py

Writes examples/NN_<relation>.musicxml: A (two bars), a bar's rest, then B.
Open them in MuseScore. One base motif is used for every relation that applies
to it, so the examples can be compared directly. Every mode is written on its
white-key tonic (C major, A minor, D dorian, G mixolydian), so the key
signature is always empty and any accidental is part of the relation.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from music21 import expressions, key, metadata, meter, note, pitch, stream  # noqa: E402

from musipam_rel.motif import LETTERS, NAT_PC, Motif  # noqa: E402
from musipam_rel.paths import DATA, EXAMPLES  # noqa: E402
from musipam_rel.relations import NAMES, RELATIONS  # noqa: E402

TONIC = {"major": "C", "ionian": "C", "minor": "A", "aeolian": "A", "dorian": "D", "mixolydian": "G",
         "phrygian": "E", "lydian": "F", "locrian": "B"}
ACC = {-2: "--", -1: "-", 0: "", 1: "#", 2: "##"}


def spell(m: Motif) -> list[pitch.Pitch]:
    t = TONIC[m.mode]
    ti = LETTERS.index(t)
    out = []
    for s, x in zip(m.semis(), m.h):
        midi = 60 + NAT_PC[t] + s
        letter_i = ti + x
        letter, octave = LETTERS[letter_i % 7], 4 + letter_i // 7
        acc = midi - (12 * (octave + 1) + NAT_PC[letter])
        out.append(pitch.Pitch(f"{letter}{ACC[acc]}{octave}"))
    return out


def score(A: Motif, B: Motif, title: str, subtitle: str) -> stream.Score:
    p = stream.Part()
    p.insert(0, meter.TimeSignature(A.meter))
    p.insert(0, key.KeySignature(0))
    gap = A.bar  # one bar's rest between A and B
    for label, m, t0 in (("A", A, 0.0), (f"B: {title}", B, A.span + gap)):
        p.insert(t0, expressions.TextExpression(label))
        for pp, on, d in zip(spell(m), m.on, m.dur):
            p.insert(t0 + on, note.Note(pp, quarterLength=d))
    end = A.span + gap + B.span
    end += (-end) % A.bar  # finish the last bar
    p.makeRests(fillGaps=True, inPlace=True)
    last = p.highestTime
    if last < end:
        p.insert(last, note.Rest(quarterLength=end - last))
    sc = stream.Score()
    sc.insert(0, metadata.Metadata(title=title, movementName=subtitle, composer="musiPAM relation inventory"))
    sc.insert(0, p)
    return sc


def main() -> int:
    rows = [json.loads(line) for line in open(DATA / "pairs_test_in.jsonl")]
    by_base = defaultdict(dict)
    for r in rows:
        by_base[r["base"]].setdefault(r["label"], r)
    best = max(by_base, key=lambda b: (len(by_base[b]), -b))
    first = {}
    for r in rows:
        first.setdefault(r["label"], r)
    EXAMPLES.mkdir(parents=True, exist_ok=True)
    lines = ["# Example pairs, one per relation", "",
             f"Base motif: `{by_base[best][next(iter(by_base[best]))]['A']['src']}` (Essen collection) wherever the "
             "relation applies to it; otherwise the first motif it applies to. Open the `.musicxml` files in MuseScore.", "",
             "| File | Relation | B is |", "|---|---|---|"]
    for k, (name, _family, desc) in enumerate(RELATIONS, 1):
        r = by_base[best].get(name) or first.get(name)
        if r is None:
            continue
        A, B = Motif.from_json(r["A"]), Motif.from_json(r["B"])
        fn = f"{k:02d}_{name}.musicxml"
        score(A, B, name, desc).write("musicxml", fp=str(EXAMPLES / fn))
        lines.append(f"| `{fn}` | {name} | {desc}{' (other base motif)' if name not in by_base[best] else ''} |")
    (EXAMPLES / "README.md").write_text("\n".join(lines) + "\n")
    print(f"{len(lines) - 6} examples -> {EXAMPLES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
