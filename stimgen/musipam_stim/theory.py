"""Tonal-theory helpers: scale degrees, spelling, Roman-numeral mapping, minor-mode rules.

Conventions
-----------
* Degree indices are 0-based (0 = tonic ... 6 = leading tone / subtonic).
* "dnn" = music21 diatonicNoteNum (letter-based staff position; C4 = 29).
* Minor keys use the natural-minor scale as their default spelling; raised
  6th/7th degrees are applied by context (see ``minor_alterations``).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from music21 import key as m21key
from music21 import pitch, roman

LETTERS = "CDEFGAB"
NAT_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
SCALE = {"major": [0, 2, 4, 5, 7, 9, 11], "minor": [0, 2, 3, 5, 7, 8, 10]}
TRIAD_QUALITY = {
    "major": ["M", "m", "m", "M", "M", "m", "d"],
    "minor": ["m", "d", "M", "m", "m", "M", "M"],
}
NUMERALS = ["I", "II", "III", "IV", "V", "VI", "VII"]
SEVENTH_FIGURES = {"7", "65", "43", "42", "2"}
_RN_RE = re.compile(r"^(VII|VI|V|IV|III|II|I|vii|vi|v|iv|iii|ii|i)(o|ø|\+)?(.*)$")


class KeyInfo:
    """Degree/spelling arithmetic for one key."""

    def __init__(self, k: m21key.Key):
        self.k = k
        self.mode = k.mode
        self.tonic_letter = LETTERS.index(k.tonic.step)
        self.tonic_pc = k.tonic.pitchClass
        self.tonic_dnn4 = 4 * 7 + self.tonic_letter + 1  # tonic letter, octave 4

    def degree_of_dnn(self, dnn: int) -> int:
        return ((dnn - 1) % 7 - self.tonic_letter) % 7

    def degree_of(self, p: pitch.Pitch) -> int:
        return self.degree_of_dnn(p.diatonicNoteNum)

    def default_pc(self, deg: int) -> int:
        return (self.tonic_pc + SCALE[self.mode][deg]) % 12

    def alteration_of(self, p: pitch.Pitch) -> int:
        a = (p.pitchClass - self.default_pc(self.degree_of(p))) % 12
        return a - 12 if a > 6 else a

    def spell(self, dnn: int, alter: int = 0) -> pitch.Pitch:
        letter_idx = (dnn - 1) % 7
        octave = (dnn - 1) // 7
        target_pc = (self.default_pc(self.degree_of_dnn(dnn)) + alter) % 12
        return spell_letter(letter_idx, octave, target_pc)


def spell_letter(letter_idx: int, octave: int, target_pc: int) -> pitch.Pitch:
    letter = LETTERS[letter_idx]
    a = (target_pc - NAT_PC[letter]) % 12
    if a > 6:
        a -= 12
    if a not in (-2, -1, 0, 1, 2):
        raise ValueError(f"cannot spell pc {target_pc} on letter {letter}")
    acc = {-2: "--", -1: "-", 0: "", 1: "#", 2: "##"}[a]
    return pitch.Pitch(f"{letter}{acc}{octave}")


# --------------------------------------------------------------------------
# Roman numerals
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class RN:
    degree: int     # 0-based root degree
    figure: str     # inversion figure: "", "6", "64", "7", "65", "43", "42"

    @property
    def seventh(self) -> bool:
        return self.figure in SEVENTH_FIGURES


def parse_rn(fig: str) -> RN:
    m = _RN_RE.match(fig)
    if not m:
        raise ValueError(f"unparseable Roman numeral {fig!r}")
    num, _qual, figure = m.groups()
    return RN(NUMERALS.index(num.upper()), figure)


def rn_string(rn: RN, mode: str, dominant: bool = False) -> str:
    """Diatonic Roman-numeral string for ``rn`` in ``mode``.

    ``dominant=True`` applies the harmonic-minor exception: V becomes major and
    VII becomes the diminished leading-tone chord.
    """
    q = TRIAD_QUALITY[mode][rn.degree]
    if dominant and mode == "minor" and rn.degree == 4:
        q = "M"
    if dominant and mode == "minor" and rn.degree == 6:
        q = "d"
    num = NUMERALS[rn.degree]
    if q == "M":
        s = num
    elif q == "m":
        s = num.lower()
    elif rn.seventh and not (dominant and mode == "minor" and rn.degree == 6):
        s = num.lower() + "ø"   # diatonic seventh on a diminished triad is half-diminished
    else:
        s = num.lower() + "o"   # diminished triad, or vii°7 acting as a dominant in minor
    return s + rn.figure


def rn_obj(fig: str, k: m21key.Key) -> roman.RomanNumeral:
    return roman.RomanNumeral(fig, k)


def chord_pcs(fig: str, k: m21key.Key) -> set[int]:
    return {p.pitchClass for p in rn_obj(fig, k).pitches}


TENSION_BY_DEGREE = {0: 0.0, 5: 0.25, 2: 0.25, 1: 0.5, 3: 0.5, 4: 1.0, 6: 1.0}


def tension(fig: str) -> float:
    """Coarse tonal tension: tonic 0, predominant .5, dominant 1."""
    rn = parse_rn(fig)
    if rn.degree == 0 and rn.figure == "64":  # cadential 6/4
        return 0.75
    return TENSION_BY_DEGREE[rn.degree]


def is_dominant_function(rn: RN, next_rn: RN | None) -> bool:
    """V/VII chords that resolve to the tonic (or any V7) act as dominants."""
    if rn.degree not in (4, 6):
        return False
    if rn.degree == 4 and rn.seventh:
        return True
    return next_rn is not None and next_rn.degree == 0


def remap_progression(figs: list[str], src_mode: str, dst_mode: str, root_map=None) -> list[str]:
    """Re-spell a progression for ``dst_mode`` with an optional root-degree map.

    ``root_map(rn) -> RN`` implements e.g. diatonic inversion of the harmony.
    Chord qualities follow the destination mode's diatonic triads, with the
    harmonic-minor exception for chords that function as dominants.
    """
    parsed = [parse_rn(f) for f in figs]
    if root_map is not None:
        parsed = [root_map(r) for r in parsed]
    out = []
    for i, r in enumerate(parsed):
        nxt = parsed[i + 1] if i + 1 < len(parsed) else None
        out.append(rn_string(r, dst_mode, dominant=is_dominant_function(r, nxt)))
    return out


def invert_rn(rn: RN) -> RN:
    """Diatonic inversion about scale degree 3 (index 2): x -> 4 - x.

    Triad roots map r -> -r; seventh-chord roots map r -> -2 - r. The tonic
    triad maps onto itself; dominant and subdominant exchange.
    """
    new = (-rn.degree) % 7 if not rn.seventh else (-2 - rn.degree) % 7
    return RN(new, rn.figure)


# --------------------------------------------------------------------------
# Minor-mode alteration rules for melodies
# --------------------------------------------------------------------------
def minor_alterations(dnns: list[int], chord_pc_sets: list[set[int]], ki: KeyInfo) -> list[int]:
    """Alterations (+1 = raised) for degrees 6/7 of a melody in a minor key.

    Degree 7: raised if the active chord contains the leading tone; natural if
    the chord contains the subtonic; otherwise raised only when it steps up to
    the tonic. Degree 6: follows the chord; otherwise raised only next to a
    raised 7th by step (melodic minor), which prevents augmented seconds.
    """
    n = len(dnns)
    alters = [0] * n
    if ki.mode != "minor":
        return alters
    degs = [ki.degree_of_dnn(d) for d in dnns]
    nat6, nat7 = ki.default_pc(5), ki.default_pc(6)
    r6, r7 = (nat6 + 1) % 12, (nat7 + 1) % 12
    for i in range(n):
        if degs[i] != 6:
            continue
        pcs = chord_pc_sets[i]
        if r7 in pcs:
            alters[i] = 1
        elif nat7 in pcs:
            alters[i] = 0
        else:
            alters[i] = int(i + 1 < n and dnns[i + 1] == dnns[i] + 1)
    for i in range(n):
        if degs[i] != 5:
            continue
        pcs = chord_pc_sets[i]
        if nat6 in pcs:
            alters[i] = 0
        elif r6 in pcs:
            alters[i] = 1
        else:
            up = i + 1 < n and dnns[i + 1] == dnns[i] + 1 and alters[i + 1] == 1
            down = i > 0 and dnns[i - 1] == dnns[i] + 1 and alters[i - 1] == 1
            alters[i] = int(up or down)
    # A raised 7th the harmony doesn't require must not sit a step from a lowered 6th
    # (that would be an augmented second): use the natural 7th instead.
    for i in range(n):
        if degs[i] != 6 or alters[i] != 1 or r7 in chord_pc_sets[i]:
            continue
        for j in (i - 1, i + 1):
            if 0 <= j < n and degs[j] == 5 and alters[j] == 0 and abs(dnns[j] - dnns[i]) == 1:
                alters[i] = 0
    return alters
