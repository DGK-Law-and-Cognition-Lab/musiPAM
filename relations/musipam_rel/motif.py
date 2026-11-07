"""Motifs in key-relative diatonic coordinates.

A motif is a short monophonic melody stored as plain lists, so the relation
transforms are fast and exact:

    h     diatonic height in scale steps above the tonic of octave 4
          (0 = tonic, 7 = the tonic an octave up, -1 = the step below the tonic)
    alt   semitone alteration against the key's scale (0 = diatonic)
    on    onset in quarter notes from the start of the motif
    dur   duration in quarter notes
    span  length of the motif in quarter notes
    bar   bar length in quarter notes
    meter time signature, e.g. "6/8"
    mode  the key's scale: major, minor, dorian, mixolydian, ...
    src   where it came from (collection/file/tune/bar, or stimulus:motif)
"""
from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import asdict, dataclass, replace
from pathlib import Path

LETTERS = "CDEFGAB"
NAT_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
SCALES = {
    "major": (0, 2, 4, 5, 7, 9, 11), "ionian": (0, 2, 4, 5, 7, 9, 11),
    "minor": (0, 2, 3, 5, 7, 8, 10), "aeolian": (0, 2, 3, 5, 7, 8, 10),
    "dorian": (0, 2, 3, 5, 7, 9, 10), "mixolydian": (0, 2, 4, 5, 7, 9, 10),
    "phrygian": (0, 1, 3, 5, 7, 8, 10), "lydian": (0, 2, 4, 6, 7, 9, 11),
    "locrian": (0, 1, 3, 5, 6, 8, 10),
}
EPS = 1e-6


@dataclass
class Motif:
    h: list
    alt: list
    on: list
    dur: list
    span: float
    bar: float
    meter: str
    mode: str
    src: str = ""

    @property
    def n(self) -> int:
        return len(self.h)

    def semis(self) -> list[int]:
        """Chromatic height in semitones above the tonic of octave 4."""
        sc = SCALES[self.mode]
        return [12 * (x // 7) + sc[x % 7] + a for x, a in zip(self.h, self.alt)]

    def signature(self) -> tuple:
        """Exact identity of the notes, for duplicate and ambiguity checks."""
        return (tuple(self.semis()), tuple(self.h), tuple(round(x, 4) for x in self.on),
                tuple(round(x, 4) for x in self.dur), round(self.span, 4))

    def shape(self) -> tuple:
        """Transposition-free identity (steps and rhythm), for the musiPAM hold-out filter."""
        return (tuple(b - a for a, b in zip(self.h, self.h[1:])), tuple(round(x, 3) for x in self.on),
                tuple(round(x, 3) for x in self.dur))

    def tune(self) -> str:
        """The tune a corpus motif came from (everything but the bar number)."""
        return self.src.rsplit("/", 1)[0]

    def with_(self, **kw) -> "Motif":
        return replace(self, **kw)

    def to_json(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_json(d: dict) -> "Motif":
        return Motif(**d)


def height(step: str, octave: int, tonic_step: str) -> int:
    """Scale steps from the tonic of octave 4 to a note, counted by letter name."""
    return (octave * 7 + LETTERS.index(step)) - (4 * 7 + LETTERS.index(tonic_step))


def alteration(h: int, pc: int, tonic_pc: int, mode: str) -> int:
    a = (pc - tonic_pc - SCALES[mode][h % 7]) % 12
    return a - 12 if a > 6 else a


def parse_pitch_name(name: str) -> tuple[str, int, int]:
    """music21 nameWithOctave ("F#4", "B-3", "C##5") -> (letter, accidental, octave)."""
    step, i, acc = name[0], 1, 0
    while i < len(name) and name[i] in "#-":
        acc += 1 if name[i] == "#" else -1
        i += 1
    return step, acc, int(name[i:])


def musipam_motifs(stim_dir: Path) -> dict[str, list[Motif]]:
    """The four melody motifs of every musiPAM stimulus, from note_events.csv and manifest.csv."""
    manifest = {r["stim_id"]: r for r in csv.DictReader(open(stim_dir / "manifest.csv"))}
    notes: dict[str, dict[int, list]] = defaultdict(lambda: defaultdict(list))
    for r in csv.DictReader(open(stim_dir / "note_events.csv")):
        if r["part"] == "melody":
            notes[r["stim_id"]][int(r["motif_pos"])].append(r)
    out = {}
    for sid, by_pos in notes.items():
        m = manifest[sid]
        tonic, mode = m["key"].split()
        t_step, t_pc = tonic[0], (NAT_PC[tonic[0]] + tonic.count("#") - tonic.count("-")) % 12
        num, den = (int(x) for x in m["meter"].split("/"))
        bar = num * 4.0 / den
        mots = []
        for pos in sorted(by_pos):
            rows = by_pos[pos]
            t0 = float(rows[0]["onset_ql"])
            h, alt, on, dur = [], [], [], []
            for r in rows:
                step, _acc, octave = parse_pitch_name(r["pitch"])
                x = height(step, octave, t_step)
                h.append(x)
                alt.append(alteration(x, int(r["midi"]) % 12, t_pc, mode))
                on.append(float(r["onset_ql"]) - t0)
                dur.append(float(r["dur_ql"]))
            span = on[-1] + dur[-1]
            mots.append(Motif(h, alt, on, dur, span, bar, m["meter"], mode, src=f"{sid}:{rows[0]['motif']}"))
        out[sid] = mots
    return out
