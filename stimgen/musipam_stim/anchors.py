"""Well-known public-domain melodies for Study 0: familiarity anchors and the practice melody.

They go through the themes' pipeline unchanged: the same notation, the same accompaniment
rule (``arrange.py``), clarinet over piano as in the identity condition, and the same mix and
loudness target (``render.py``). So the anchors differ from the themes only in being well known.

Each excerpt starts at the beginning of the tune, so it is recognized from the first notes,
and ends on the tonic. Where a tune opens with a pickup, a first bar of accompaniment carries
it (``r`` = rest). Where the opening phrase ends on the dominant, the excerpt borrows the
tune's own tonic ending, as noted per melody. Study 0's anchor list is still a DECISION in
prereg/S0_norming.md; this module holds the proposal.
"""
from __future__ import annotations

from dataclasses import dataclass

from music21 import key as m21key

from .themes import DUR, MNote, Segment, Stim, _pitch, parse_harmony


@dataclass
class Anchor:
    anchor_id: str
    title: str
    kind: str                    # "anchor" | "practice"
    source: str
    excerpt: str
    key: str
    meter: str
    bpm: float
    texture: str
    tonic_ref: int
    segments: list[tuple[str, str]]  # (melody, harmony), two bars each
    composer: str = "Traditional"


ANCHORS: dict[str, Anchor] = {
    "A1": Anchor(
        "A1", "Ode to Joy", "anchor",
        source="Beethoven, Symphony No. 9, finale (1824). Public domain.",
        excerpt="Bars 1-8 (the first two phrases), in C major.",
        key="C", meter="4/4", bpm=104, texture="alberti", tonic_ref=48, composer="Ludwig van Beethoven",
        segments=[
            ("E5/q E5/q F5/q G5/q | G5/q F5/q E5/q D5/q", "I:4 | V:4"),
            ("C5/q C5/q D5/q E5/q | E5/q. D5/e D5/h", "I:4 | I:2 V:2"),
            ("E5/q E5/q F5/q G5/q | G5/q F5/q E5/q D5/q", "I:4 | V:4"),
            ("C5/q C5/q D5/q E5/q | D5/q. C5/e C5/h", "I:4 | V:2 I:2"),
        ],
    ),
    "A2": Anchor(
        "A2", "Frère Jacques", "anchor",
        source="Traditional French round (18th century). Public domain.",
        excerpt="The whole round, sung once, in B-flat major.",
        key="B-", meter="4/4", bpm=108, texture="march", tonic_ref=44,
        segments=[
            ("Bb4/q C5/q D5/q Bb4/q | Bb4/q C5/q D5/q Bb4/q", "I:4 | I:4"),
            ("D5/q Eb5/q F5/h | D5/q Eb5/q F5/h", "I:4 | I:4"),
            ("F5/e G5/e F5/e Eb5/e D5/q Bb4/q | F5/e G5/e F5/e Eb5/e D5/q Bb4/q", "I:4 | I:4"),
            ("Bb4/q F4/q Bb4/h | Bb4/q F4/q Bb4/h", "I:1 V:1 I:2 | I:1 V:1 I:2"),
        ],
    ),
    "A3": Anchor(
        "A3", "Greensleeves", "anchor",
        source="Traditional English (16th century). Public domain.",
        excerpt="The pickup and bars 9-15: the verse's second phrase, which opens exactly as the "
                "first does and closes on the tonic. A minor.",
        key="a", meter="3/4", bpm=92, texture="waltz", tonic_ref=45,
        segments=[
            ("r/h A4/q | C5/h D5/q", "i:3 | i:3"),
            ("E5/q. F5/e E5/q | D5/h B4/q", "III:3 | VII:3"),
            ("G4/q. A4/e B4/q | C5/q. B4/e A4/q", "v:3 | i:3"),
            ("G#4/q. F#4/e G#4/q | A4/h.", "V:3 | i:3"),
        ],
    ),
    "A4": Anchor(
        "A4", "Amazing Grace", "anchor",
        source="Hymn tune \"New Britain\" (1829). Public domain.",
        excerpt="The pickup and bars 1-6 of the first phrase, closed with the tonic final note of "
                "the second phrase (\"... now I see\"). G major.",
        key="G", meter="3/4", bpm=76, texture="chorale", tonic_ref=43, composer="Traditional (hymn tune \"New Britain\")",
        segments=[
            ("r/h D4/q | G4/h B4/e G4/e", "I:3 | I:3"),
            ("B4/h A4/q | G4/h E4/q", "I:3 | IV:3"),
            ("D4/h D4/q | G4/h B4/e G4/e", "I:3 | I:3"),
            ("B4/h A4/q | G4/h.", "I:2 V7:1 | I:3"),
        ],
    ),
    "P1": Anchor(
        "P1", "Twinkle, Twinkle, Little Star", "practice",
        source="French melody \"Ah! vous dirai-je, maman\" (18th century). Public domain.",
        excerpt="The whole tune (12 bars), in F major.",
        key="F", meter="4/4", bpm=100, texture="alberti", tonic_ref=46,
        composer="Traditional (\"Ah! vous dirai-je, maman\")",
        segments=[
            ("F4/q F4/q C5/q C5/q | D5/q D5/q C5/h", "I:4 | IV:2 I:2"),
            ("Bb4/q Bb4/q A4/q A4/q | G4/q G4/q F4/h", "IV:2 I:2 | V7:2 I:2"),
            ("C5/q C5/q Bb4/q Bb4/q | A4/q A4/q G4/h", "I:2 IV:2 | I:2 V:2"),
            ("C5/q C5/q Bb4/q Bb4/q | A4/q A4/q G4/h", "I:2 IV:2 | I:2 V:2"),
            ("F4/q F4/q C5/q C5/q | D5/q D5/q C5/h", "I:4 | IV:2 I:2"),
            ("Bb4/q Bb4/q A4/q A4/q | G4/q G4/q F4/h", "IV:2 I:2 | V7:2 I:2"),
        ],
    ),
}


def _melody(spec: str, bar_ql: float, where: str) -> list[MNote]:
    """Like ``themes.parse_melody``, plus rests (``r/h``), which only anchors use."""
    notes = []
    for i, bar in enumerate(spec.split("|")):
        toks = [t.split("/") for t in bar.split()]
        if abs(sum(DUR[d] for _, d in toks) - bar_ql) > 1e-9:
            raise ValueError(f"{where}: melody bar {i + 1} does not fill a {bar_ql}-ql bar")
        notes += [MNote(None, DUR[d], "rest") if p == "r" else MNote(_pitch(p), DUR[d]) for p, d in toks]
    return notes


def anchor_stim(anchor_id: str) -> Stim:
    a = ANCHORS[anchor_id]
    num, den = (int(x) for x in a.meter.split("/"))
    bar_ql = num * 4.0 / den
    segs = [Segment(f"m{i + 1}", i, _melody(mel, bar_ql, f"{anchor_id}.m{i + 1}"),
                    parse_harmony(harm, bar_ql, f"{anchor_id}.m{i + 1}"))
            for i, (mel, harm) in enumerate(a.segments)]
    return Stim(theme_id=anchor_id, condition=a.kind, k=m21key.Key(a.key), meter=a.meter, bpm=a.bpm,
                segments=segs, texture=a.texture, tonic_ref=a.tonic_ref,
                notes_meta={"title": f"{a.title} (musiPAM {a.kind} {anchor_id})",
                            "composer": f"{a.composer}; arranged by the musiPAM stimulus pipeline (v2)"})
