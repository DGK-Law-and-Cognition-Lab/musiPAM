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
    tonic_ref: int      # register anchor (MIDI) for the accompaniment windows
    tritone_key: str    # spelling of the key a tritone below
    motifs: list[tuple[str, str, str]]  # (label, melody, harmony)
    character: str = ""
    skeleton: str = ""  # "sentence" | "period" | "rounded" | "chain"
    head: int = 0       # sentence: number of notes in a's head (fragmented in b)
    shared_k: int = 0   # period: number of opening notes c shares with b


THEMES: dict[str, Theme] = {
    "T1": Theme(
        theme_id="T1", title="Pastorale", key="D", meter="4/4", bpm=100,
        form="sentence (a a' b c)", texture="alberti", tonic_ref=50, tritone_key="A-",
        skeleton="sentence", head=3,
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
        skeleton="period", shared_k=5,
        character="Slow minor waltz; rising minor-sixth hook, Phrygian half cadence, "
                  "consequent repeats the basic idea exactly (a1 = a2) and closes on the tonic. "
                  "Its contrasting phrase b is the look-alike source for T4's opening idea.",
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
        theme_id="T3", title="Lament", key="f", meter="4/4", bpm=96,
        form="sentence (a a' b c)", texture="march", tonic_ref=41, tritone_key="b",
        skeleton="sentence", head=2,
        character="Minor-key march-lament with T1's sentence skeleton and new motifs. "
                  "Cross-mapping: its cadence motif c has the contour and rhythm of T1's "
                  "opening motif a.",
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
        theme_id="T4", title="Berceuse", key="E", meter="6/8", bpm=78,
        form="parallel period (a1 b a2 c)", texture="berceuse", tonic_ref=52, tritone_key="B-",
        skeleton="period", shared_k=2,
        character="Lullaby with T2's period skeleton (identical a1/a2, b ending on a half "
                  "cadence, c restating b's opening and closing on the tonic) and new motifs. "
                  "Cross-mapping: its repeated opening idea has the rhythm and scale-degree "
                  "contour of T2's contrasting phrase b.",
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
    # ---------------------------------------------------------------- sentences
    "T5": Theme(
        theme_id="T5", title="Canticle", key="g", meter="3/4", bpm=76,
        form="sentence (a a' b c)", texture="chorale", tonic_ref=48, tritone_key="c#",
        skeleton="sentence", head=3,
        character="Minor-key hymn in 3/4: a rising stepwise idea, its sequence a step higher, "
                  "rising three-note cells to a held high note, and a plain 1-7-1 close. "
                  "Its opening idea is the look-alike source for T6's cadence.",
        motifs=[
            ("a",  "G4/e A4/e Bb4/e D5/q. | C5/q A4/q Bb4/q",
                   "i:3 | iv:1 V:1 i:1"),
            ("a'", "A4/e Bb4/e C5/e Eb5/q. | D5/q Bb4/q C5/q",
                   "iio6:3 | V:1 i6:1 iv6:1"),
            ("b",  "Bb4/e C5/e D5/e C5/e D5/e Eb5/e | D5/e E5/e F#5/e A5/q.",
                   "i6:1.5 iio6:1.5 | V:1.5 V7:1.5"),
            ("c",  "G5/h F#5/q | G5/h.",
                   "i64:2 V7:1 | i:3"),
        ],
    ),
    "T6": Theme(
        theme_id="T6", title="Barcarolle", key="A", meter="6/8", bpm=84,
        form="sentence (a a' b c)", texture="barcarolle", tonic_ref=48, tritone_key="E-",
        skeleton="sentence", head=2,
        character="Major-key barcarolle in 6/8 with the sentence skeleton, closing with a "
                  "cadential hemiola. Cross-mapping: its cadence c has exactly the rhythm and "
                  "contour of T5's opening idea a.",
        motifs=[
            ("a",  "A4/q C#5/e F#5/q. | E5/q D5/e C#5/q.",
                   "I:1.5 vi:1.5 | V:1.5 I:1.5"),
            ("a'", "B4/q D5/e G#5/q. | F#5/q E5/e D5/q.",
                   "ii:1.5 viio6:1.5 | vi:1.5 ii:1.5"),
            ("b",  "C#5/q E5/e D5/q F#5/e | E5/q G#5/e B5/q.",
                   "I6:1.5 ii6:1.5 | V:1.5 V7:1.5"),
            ("c",  "F#4/e G#4/e A4/e C#5/q. | B4/q G#4/q A4/q",
                   "IV:1.5 I6:1.5 | ii6:1 V7:1 I:1"),
        ],
    ),
    # ---------------------------------------------------------------- periods
    "T7": Theme(
        theme_id="T7", title="Promenade", key="B-", meter="4/4", bpm=108,
        form="parallel period (a1 b a2 c)", texture="arpeggio", tonic_ref=48, tritone_key="E",
        skeleton="period", shared_k=3,
        character="Strolling major-key period over rising arpeggios. Its opening idea is the "
                  "look-alike source for T8's b and c.",
        motifs=[
            ("a1", "D5/q F5/q Bb4/q. C5/e | D5/q C5/q A4/h",
                   "I:4 | I:1 V7:3"),
            ("b",  "G4/q. A4/e Bb4/q Eb5/q | C5/h A4/h",
                   "IV:4 | V:4"),
            ("a2", "D5/q F5/q Bb4/q. C5/e | D5/q C5/q A4/h",
                   "I:4 | I:1 V7:3"),
            ("c",  "G4/q. A4/e Bb4/q F5/q | D5/h Bb4/h",
                   "IV:3 V7:1 | I:4"),
        ],
    ),
    "T8": Theme(
        theme_id="T8", title="Elegy", key="b", meter="4/4", bpm=96,
        form="parallel period (a1 b a2 c)", texture="sustained", tonic_ref=46, tritone_key="f",
        skeleton="period", shared_k=4,
        character="Minor-key elegy over sustained chords, with the period skeleton. Cross-mapping: "
                  "its b and c take the rhythm of T7's opening idea, and c its contour too.",
        motifs=[
            ("a1", "F#4/h B4/q. C#5/e | A#4/q C#5/q E5/h",
                   "i:4 | V7:4"),
            ("b",  "E5/q G5/q C#5/q. D5/e | C#5/q A#4/q F#4/h",
                   "iv:2 V:2 | V:4"),
            ("a2", "F#4/h B4/q. C#5/e | A#4/q C#5/q E5/h",
                   "i:4 | V7:4"),
            ("c",  "E5/q G5/q C#5/q. D5/e | E5/q D5/q B4/h",
                   "iv:2 V:2 | V7:1 i:3"),
        ],
    ),
    # ---------------------------------------------------------------- rounded (a b c a')
    "T9": Theme(
        theme_id="T9", title="Ländler", key="F", meter="3/4", bpm=88,
        form="rounded (a b c a')", texture="waltz", tonic_ref=46, tritone_key="B",
        skeleton="rounded",
        character="Rustic major-key waltz in rounded form: the opening returns at the end with "
                  "a cadential close. Its dominant-preparation c is the look-alike source for T10's b.",
        motifs=[
            ("a",  "A4/q. Bb4/e C5/q | F5/h A4/q",
                   "I:3 | I:3"),
            ("b",  "D5/h C5/q | Bb4/q A4/q G4/q",
                   "vi:3 | IV:2 ii:1"),
            ("c",  "G4/e A4/e Bb4/e C5/e D5/e E5/e | G5/h.",
                   "ii6:1.5 V:1.5 | V7:3"),
            ("a'", "A4/q. Bb4/e C5/q | F4/h.",
                   "I:2 V7:1 | I:3"),
        ],
    ),
    "T10": Theme(
        theme_id="T10", title="Nocturne", key="f#", meter="6/8", bpm=75,
        form="rounded (a b c a')", texture="berceuse", tonic_ref=50, tritone_key="c",
        skeleton="rounded",
        character="Minor-key nocturne in 6/8, rounded form: a rising arpeggio that sighs back "
                  "down, a run up to the high third, and a half cadence that leaps to the leading "
                  "tone before the return. Cross-mapping: its contrasting b has exactly the rhythm "
                  "and contour of T9's c.",
        motifs=[
            ("a",  "F#4/q A4/e C#5/q. | B4/q G#4/e A4/q.",
                   "i:3 | V7:1.5 i:1.5"),
            ("b",  "A4/e B4/e C#5/e D5/e E5/e F#5/e | A5/h.",
                   "III:1.5 VI:1.5 | iv7:3"),
            ("c",  "D5/q. B4/q. | G#4/q B4/e E#5/q.",
                   "iiø7:3 | V7:3"),
            ("a'", "F#4/q A4/e C#5/q. | B4/q G#4/e F#4/q.",
                   "i:3 | V7:1.5 i:1.5"),
        ],
    ),
    "T11": Theme(
        theme_id="T11", title="March", key="e", meter="4/4", bpm=104,
        form="rounded (a b c a')", texture="march", tonic_ref=40, tritone_key="b-",
        skeleton="rounded",
        character="Minor-key march in rounded form. Its contrasting b is the look-alike source "
                  "for T12's opening idea.",
        motifs=[
            ("a",  "E5/q B4/q G4/q. A4/e | B4/h G4/h",
                   "i:4 | i:4"),
            ("b",  "A4/q. C5/e B4/q A4/q | G4/q. A4/e F#4/h",
                   "iv:2 V:1 iv:1 | VI:2 iio6:2"),
            ("c",  "F#4/q G4/q A4/q B4/q | C5/q B4/q A4/h",
                   "iio6:3 V:1 | V7:4"),
            ("a'", "E5/q B4/q G4/q. A4/e | G4/q F#4/q E4/h",
                   "i:4 | i:1 V7:1 i:2"),
        ],
    ),
    "T12": Theme(
        theme_id="T12", title="Chorale", key="A-", meter="4/4", bpm=92,
        form="rounded (a b c a')", texture="chorale", tonic_ref=48, tritone_key="D",
        skeleton="rounded",
        character="Major-key chorale in rounded form. Cross-mapping: its opening idea (and so the "
                  "start of its return) has exactly the rhythm and contour of T11's b.",
        motifs=[
            ("a",  "Eb5/q. G5/e F5/q Eb5/q | Db5/q. Eb5/e C5/h",
                   "I:2 ii:1 V7:1 | V7:2 I:2"),
            ("b",  "C5/q F5/q Eb5/q Db5/q | Bb4/w",
                   "vi:2 I:1 IV:1 | ii:4"),
            ("c",  "Bb4/q C5/q Db5/q Eb5/q | G5/h Eb5/h",
                   "ii:3 V:1 | V7:4"),
            ("a'", "Eb5/q. G5/e F5/q Eb5/q | Db5/q. C5/e Ab4/h",
                   "I:2 ii:1 V7:1 | V7:2 I:2"),
        ],
    ),
    # ---------------------------------------------------------------- sequence chains (a a' a'' b)
    "T13": Theme(
        theme_id="T13", title="Cascade", key="E-", meter="4/4", bpm=112,
        form="sequence chain (a a' a'' b)", texture="alberti", tonic_ref=48, tritone_key="A",
        skeleton="chain",
        character="Major-key descending sequence: an arpeggiated idea restated a step lower, then "
                  "another step lower, before a short cadence. Its third statement a'' is the "
                  "look-alike source for T14's cadence.",
        motifs=[
            ("a",   "Eb5/q G5/q Bb5/q. Ab5/e | G5/h F5/h",
                    "I:4 | I:2 V:2"),
            ("a'",  "D5/q F5/q Ab5/q. G5/e | F5/h Eb5/h",
                    "V7:4 | V7:2 I:2"),
            ("a''", "C5/q Eb5/q G5/q. F5/e | Eb5/h D5/h",
                    "vi:4 | vi:2 V:2"),
            ("b",   "C5/q F5/q D5/q Bb4/q | Eb5/w",
                    "IV:1 ii:1 V7:2 | I:4"),
        ],
    ),
    "T14": Theme(
        theme_id="T14", title="Romance", key="c#", meter="4/4", bpm=100,
        form="sequence chain (a a' a'' b)", texture="arpeggio", tonic_ref=46, tritone_key="g",
        skeleton="chain",
        character="Minor-key romance over rising arpeggios: a sighing idea restated twice, each "
                  "a step lower. Cross-mapping: its cadence b has exactly the rhythm and contour "
                  "of T13's a'', the last statement of T13's sequence.",
        motifs=[
            ("a",   "E5/h D#5/q E5/q | G#4/q. A4/e G#4/h",
                    "i:2 V:1 i:1 | i:2 V:2"),
            ("a'",  "D#5/h C#5/q D#5/q | F#4/q. G#4/e F#4/h",
                    "V7:2 i:1 V7:1 | iv:2 V7:2"),
            ("a''", "C#5/h B4/q C#5/q | E4/q. F#4/e E4/h",
                    "i:2 III:1 i:1 | i:2 III:2"),
            ("b",   "B4/q D#5/q F#5/q. E5/e | D#5/h C#5/h",
                    "VII:2 iv:2 | V7:2 i:2"),
        ],
    ),
    "T15": Theme(
        theme_id="T15", title="Sarabande", key="d", meter="3/4", bpm=80,
        form="sequence chain (a a' a'' b)", texture="sustained", tonic_ref=43, tritone_key="g#",
        skeleton="chain",
        character="Minor-key sarabande with its weight on beat two: one idea stated three times, "
                  "each a step lower, then a falling close. Its close b is the look-alike source "
                  "for T16's opening idea.",
        motifs=[
            ("a",   "A4/q D5/h | C#5/q. B4/e A4/q",
                    "i:3 | V:3"),
            ("a'",  "G4/q C5/h | Bb4/q. A4/e G4/q",
                    "VII:3 | iv:3"),
            ("a''", "F4/q Bb4/h | A4/q. G4/e F4/q",
                    "VI:3 | i:3"),
            ("b",   "G4/q. F4/e E4/q | D4/h.",
                    "iv:2 V:1 | i:3"),
        ],
    ),
    "T16": Theme(
        theme_id="T16", title="Siciliana", key="D-", meter="6/8", bpm=72,
        form="sequence chain (a a' a'' b)", texture="barcarolle", tonic_ref=48, tritone_key="G",
        skeleton="chain",
        character="Major-key siciliana in 6/8: a falling four-note idea in siciliano rhythm, "
                  "stated three times, each a step lower. Cross-mapping: that idea has exactly "
                  "the rhythm and contour of T15's close b.",
        motifs=[
            ("a",   "Ab5/q. Gb5/e F5/q | Eb5/h.",
                    "I:3 | V:3"),
            ("a'",  "Gb5/q. F5/e Eb5/q | Db5/h.",
                    "V7:3 | I:3"),
            ("a''", "F5/q. Eb5/e Db5/q | C5/h.",
                    "I:3 | V:3"),
            ("b",   "Bb4/q. Eb5/q. | Db5/h.",
                    "ii:1.5 V7:1.5 | I:3"),
        ],
    ),
}

# Designed cross-mappings: the target motif copies the source motif's rhythm and
# scale-step contour exactly while playing a different role.
# (source theme, source motif index, target theme, target motif index)
CROSS_MAPPINGS = [
    ("T1", 0, "T3", 3), ("T2", 1, "T4", 0), ("T5", 0, "T6", 3), ("T7", 0, "T8", 3),
    ("T9", 2, "T10", 1), ("T11", 1, "T12", 0), ("T13", 2, "T14", 3), ("T15", 3, "T16", 0),
]


def analog_pairs() -> list[tuple[str, str]]:
    """All theme pairs that share a relational skeleton (designed analogs)."""
    ids = list(THEMES)
    return [(a, b) for i, a in enumerate(ids) for b in ids[i + 1:]
            if THEMES[a].skeleton == THEMES[b].skeleton]


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
