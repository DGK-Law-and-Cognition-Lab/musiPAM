"""The composed themes and the data model they are parsed into.

Every theme is 8 bars = 4 motifs x 2 bars. Each motif carries its melody
(explicit pitches and durations) and the harmonic plan beneath it (Roman
numerals with durations). The melody is the structural object; the
accompaniment is realized from the harmonic plan by a fixed texture rule
(see ``arrange.py``), so every transformation acts on melody and harmony
together and the two never clash.

Notation: ``"F#4/e"`` = F#4 eighth note. Flats are written ``b`` (``"Db5"``).
Durations: w=4, h.=3, h=2, q.=1.5, q=1, e.=0.75, e=0.5, s=0.25 quarter notes.
Harmony: ``"IV64:2"`` = IV in second inversion for 2 quarter notes.
``|`` marks barlines and is checked, not just decorative.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field

from music21 import key as m21key
from music21 import pitch

DUR = {"w": 4.0, "h.": 3.0, "h": 2.0, "q.": 1.5, "q": 1.0, "e.": 0.75, "e": 0.5, "s": 0.25}


@dataclass
class MNote:
    p: pitch.Pitch
    dur: float
    kind: str = ""  # "" = composed tone; "passing" / "neighbor" / "restrike" = ornamental

    @property
    def added(self) -> bool:
        return self.kind != ""


@dataclass
class ChordSpan:
    fig: str
    dur: float


@dataclass
class Segment:
    """One motif occurrence. ``label`` and ``src`` identify the source motif."""
    label: str
    src: int
    notes: list[MNote]
    chords: list[ChordSpan]

    @property
    def dur(self) -> float:
        return sum(n.dur for n in self.notes)


@dataclass
class Stim:
    theme_id: str
    condition: str
    k: m21key.Key
    meter: str
    bpm: float
    segments: list[Segment]
    texture: str
    tonic_ref: int                 # MIDI of the tonic used to anchor accompaniment registers
    melody_inst: str = "clarinet"
    accomp_inst: str = "piano"
    notes_meta: dict = field(default_factory=dict)

    @property
    def stim_id(self) -> str:
        return f"{self.theme_id}_{self.condition}"

    @property
    def bar_ql(self) -> float:
        num, den = (int(x) for x in self.meter.split("/"))
        return num * 4.0 / den

    @property
    def total_ql(self) -> float:
        return sum(s.dur for s in self.segments)

    def clone(self, condition: str) -> "Stim":
        s = copy.deepcopy(self)
        s.condition = condition
        return s


@dataclass
class Theme:
    theme_id: str
    title: str
    key: str            # music21 key string: "D" major, "c" minor
    meter: str
    bpm: float
    form: str
    texture: str
    tonic_ref: int
    tritone_key: str    # spelling of the key a tritone below
    motifs: list[tuple[str, str, str]]  # (label, melody, harmony)
    character: str = ""


THEMES: dict[str, Theme] = {
    "T1": Theme(
        theme_id="T1", title="Pastorale", key="D", meter="4/4", bpm=100,
        form="sentence (a a' b c)", texture="alberti", tonic_ref=50, tritone_key="A-",
        character="Classical sentence; rising arpeggio basic idea, sequential repetition, "
                  "fragmentation climbing to a held climax, 3-2-7-1 cadence.",
        motifs=[
            ("a",  "D4/e F#4/e A4/q D5/q. C#5/e | B4/q A4/q F#4/h",
                   "I:4 | IV64:2 I:2"),
            ("a'", "E4/e G4/e B4/q E5/q. D5/e | C#5/q B4/q G4/h",
                   "ii:4 | V64:2 ii:2"),
            ("b",  "F#4/e A4/e D5/q G4/e B4/e E5/q | A4/e C#5/e E5/q G5/h",
                   "I6:2 ii6:2 | V7:4"),
            ("c",  "F#5/h E5/q C#5/q | D5/w",
                   "I64:2 V7:2 | I:4"),
        ],
    ),
    "T2": Theme(
        theme_id="T2", title="Valse", key="c", meter="3/4", bpm=84,
        form="parallel period (a1 b a2 c)", texture="waltz", tonic_ref=48, tritone_key="f#",
        character="Slow minor waltz; rising minor-sixth hook, Phrygian half cadence, "
                  "consequent repeats the basic idea exactly (a1 = a2) and closes on the tonic. "
                  "T4 is its structural analog.",
        motifs=[
            ("a1", "G4/q Eb5/h | F5/q D5/q B4/q",
                   "i:3 | V7:3"),
            ("b",  "C5/e Bb4/e Ab4/e G4/e F4/e Ab4/e | G4/h.",
                   "iv6:3 | V:3"),
            ("a2", "G4/q Eb5/h | F5/q D5/q B4/q",
                   "i:3 | V7:3"),
            ("c",  "C5/e Bb4/e Ab4/e G4/e F4/e D4/e | C4/h.",
                   "iv6:2 V7:1 | i:3"),
        ],
    ),
    "T3": Theme(
        theme_id="T3", title="Lament (analog of T1)", key="f", meter="4/4", bpm=96,
        form="sentence (a a' b c)", texture="march", tonic_ref=41, tritone_key="b",
        character="Structural analog of T1: same sentence skeleton and inter-motif relations, "
                  "new motifs. Cross-mapping: its cadence motif c has the contour and rhythm "
                  "of T1's opening motif a.",
        motifs=[
            ("a",  "C5/q. Db5/e C5/q Ab4/q | Bb4/e G4/e E4/e G4/e Ab4/h",
                   "i:4 | V7:2 i:2"),
            ("a'", "Db5/q. Eb5/e Db5/q Bb4/q | C5/e Ab4/e F4/e Ab4/e Bb4/h",
                   "iio6:4 | VI7:2 iio6:2"),
            ("b",  "C4/q. Db4/e Db4/q. Eb4/e | E4/q. F4/e G4/h",
                   "i6:2 iio6:2 | V7:4"),
            ("c",  "F4/e Ab4/e C5/q F5/q. Eb5/e | Db5/q C5/q Ab4/h",
                   "i:2 iv:2 | V7:2 i:2"),
        ],
    ),
    "T4": Theme(
        theme_id="T4", title="Berceuse (analog of T2)", key="E", meter="6/8", bpm=78,
        form="parallel period (a1 b a2 c)", texture="berceuse", tonic_ref=52, tritone_key="B-",
        character="Structural analog of T2: same period skeleton (identical a1/a2, b ending on a "
                  "half cadence, c restating b's opening and closing on the tonic), new motifs, "
                  "key, mode, meter and texture. Cross-mapping: its repeated opening idea a has "
                  "the rhythm and scale-degree contour of T2's contrasting phrase b.",
        motifs=[
            ("a1", "E5/e D#5/e C#5/e B4/e A4/e C#5/e | B4/h.",
                   "I:3 | V7:3"),
            ("b",  "F#4/q A4/e C#5/q. | B4/h.",
                   "ii6:3 | V:3"),
            ("a2", "E5/e D#5/e C#5/e B4/e A4/e C#5/e | B4/h.",
                   "I:3 | V7:3"),
            ("c",  "F#4/q A4/e B4/q. | E4/h.",
                   "ii6:1.5 V7:1.5 | I:3"),
        ],
    ),
}

COMPOUND_METERS = {"6/8", "9/8", "12/8"}
STRONG_BEATS = {"4/4": (0.0, 2.0), "3/4": (0.0,), "6/8": (0.0, 1.5)}  # positions in a bar (ql)


# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------
def _pitch(tok: str) -> pitch.Pitch:
    letter, rest = tok[0], tok[1:]
    octave = rest.lstrip("#b")
    acc = rest[: len(rest) - len(octave)].replace("b", "-")
    return pitch.Pitch(f"{letter}{acc}{octave}")


def _bars(spec: str, item_parser) -> list[list]:
    return [[item_parser(t) for t in bar.split()] for bar in spec.split("|")]


def parse_melody(spec: str, bar_ql: float, where: str) -> list[MNote]:
    bars = _bars(spec, lambda t: MNote(_pitch(t.split("/")[0]), DUR[t.split("/")[1]]))
    for i, bar in enumerate(bars):
        total = sum(n.dur for n in bar)
        if abs(total - bar_ql) > 1e-9:
            raise ValueError(f"{where}: melody bar {i + 1} lasts {total} ql, expected {bar_ql}")
    return [n for bar in bars for n in bar]


def parse_harmony(spec: str, bar_ql: float, where: str) -> list[ChordSpan]:
    bars = _bars(spec, lambda t: ChordSpan(t.split(":")[0], float(t.split(":")[1])))
    for i, bar in enumerate(bars):
        total = sum(c.dur for c in bar)
        if abs(total - bar_ql) > 1e-9:
            raise ValueError(f"{where}: harmony bar {i + 1} lasts {total} ql, expected {bar_ql}")
    return [c for bar in bars for c in bar]


def theme_stim(theme_id: str) -> Stim:
    th = THEMES[theme_id]
    num, den = (int(x) for x in th.meter.split("/"))
    bar_ql = num * 4.0 / den
    segs = []
    for i, (label, mel, harm) in enumerate(th.motifs):
        where = f"{theme_id}.{label}"
        segs.append(Segment(label, i, parse_melody(mel, bar_ql, where), parse_harmony(harm, bar_ql, where)))
    return Stim(theme_id=theme_id, condition="identity", k=m21key.Key(th.key), meter=th.meter,
                bpm=th.bpm, segments=segs, texture=th.texture, tonic_ref=th.tonic_ref)
