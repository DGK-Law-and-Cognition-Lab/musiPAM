"""Accompaniment realization and music21 score construction.

The accompaniment is never fixed audio: it is re-realized for every stimulus
from that stimulus's (transformed) harmonic plan, using the theme's texture
idiom and registers anchored to the stimulus tonic. A fixed accompaniment
under an inverted or retrograded melody would produce clashes, i.e. a surface
cue that something is "wrong", confounding the manipulation.

Velocities follow a metric-accent rule applied identically to every stimulus,
so the music is not mechanically flat but carries no condition-specific
expression.
"""
from __future__ import annotations

import copy

from music21 import (clef, duration, expressions, instrument, meter, note,
                     roman, stream, tempo)
from music21 import chord as m21chord
from music21 import pitch

from .themes import COMPOUND_METERS, STRONG_BEATS, Stim

INSTRUMENTS = {  # name -> (GM program, label)
    "clarinet": (71, "Clarinet"),
    "violin": (40, "Violin"),
    "piano": (0, "Piano"),
    "harp": (46, "Harp"),
}

# Registers are offsets (semitones) from the stimulus tonic reference.
TEXTURES = {
    # Alberti-style broken chords over a held bass, in eighths.
    "alberti": {"unit": 2.0, "bass": (-3, 8), "upper": [(0.5, 0.5, "hi"), (1.0, 0.5, "mid"), (1.5, 0.5, "hi")],
                "bass_dur": "hold"},
    # Waltz: bass on 1, chords on 2 and 3.
    "waltz": {"unit": 3.0, "bass": (-7, 4), "chord_window": (3, 19),
              "upper": [(1.0, 1.0, "chord"), (2.0, 1.0, "chord")], "bass_dur": "hold"},
    # March: bass on 1 and 3, off-beat chords on 2 and 4.
    "march": {"unit": 2.0, "bass": (0, 11), "chord_window": (9, 21),
              "upper": [(1.0, 1.0, "chord")], "bass_dur": 1.0},
    # Berceuse (6/8): rocking low-high-mid on every dotted-quarter beat.
    "berceuse": {"unit": 1.5, "bass": (-8, 3), "upper": [(0.5, 0.5, "hi"), (1.0, 0.5, "mid")],
                 "bass_dur": "hold"},
}


def make_instrument(name: str) -> instrument.Instrument:
    prog, label = INSTRUMENTS[name]
    inst = instrument.Instrument()
    inst.instrumentName = label
    inst.partName = label
    inst.midiProgram = prog
    return inst


# --------------------------------------------------------------------------
# timeline helpers
# --------------------------------------------------------------------------
def chord_timeline(s: Stim) -> list[tuple[float, float, str]]:
    out, t = [], 0.0
    for seg in s.segments:
        for ch in seg.chords:
            out.append((t, t + ch.dur, ch.fig))
            t += ch.dur
    return out


def _active(tl, t):
    for a, b, f in tl:
        if a - 1e-9 <= t < b - 1e-9:
            return a, b, f
    raise ValueError(f"no chord at {t}")


def _place(p: pitch.Pitch, lo: int, hi: int) -> pitch.Pitch:
    """Copy of ``p`` (same spelling) in the octave that lands inside [lo, hi]."""
    q = copy.deepcopy(p)
    for octave in range(0, 9):
        q.octave = octave
        if lo <= q.midi <= hi:
            return q
    raise ValueError(f"{p.name} has no octave in [{lo}, {hi}]")


def _above(p: pitch.Pitch, floor_midi: int) -> pitch.Pitch:
    """Lowest copy of ``p`` strictly above ``floor_midi``."""
    q = copy.deepcopy(p)
    for octave in range(0, 10):
        q.octave = octave
        if q.midi > floor_midi:
            return q
    raise ValueError


def _upper_members(rn: roman.RomanNumeral, n_max: int) -> list[pitch.Pitch]:
    """Chord members for the upper voices: drop the bass member of 4-note
    chords, then the fifth if still too many."""
    members = list(rn.pitches)
    if len(members) > n_max:
        bass_pc = rn.bass().pitchClass
        members = [p for p in members if p.pitchClass != bass_pc] or members
    if len(members) > n_max and rn.fifth is not None:
        members = [p for p in members if p.pitchClass != rn.fifth.pitchClass]
    return members[:n_max]


def _voicings(members: list[pitch.Pitch], lo: int, hi: int) -> list[list[pitch.Pitch]]:
    """All close-position voicings (rotations) that fit inside [lo, hi]."""
    out = []
    for r in range(len(members)):
        order = members[r:] + members[:r]
        try:
            first = _place(order[0], lo, lo + 11)
        except ValueError:
            continue
        v = [first]
        for p in order[1:]:
            v.append(_above(p, v[-1].midi))
        if v[-1].midi <= hi:
            out.append(v)
    return out


# --------------------------------------------------------------------------
# realization
# --------------------------------------------------------------------------
def realize_accompaniment(s: Stim) -> tuple[list, list]:
    """Return (bass_events, upper_events) as lists of (offset, dur, pitches, fig)."""
    tex = TEXTURES[s.texture]
    tl = chord_timeline(s)
    total = s.total_ql
    unit = tex["unit"]
    blo, bhi = (s.tonic_ref + x for x in tex["bass"])

    # bass: every unit start and every chord change
    starts = sorted({round(u * unit, 6) for u in range(int(round(total / unit)))} | {round(a, 6) for a, _, _ in tl})
    bass = []
    for i, t in enumerate(starts):
        nxt = starts[i + 1] if i + 1 < len(starts) else total
        _, _, fig = _active(tl, t)
        rn = roman.RomanNumeral(fig, s.k)
        dur = nxt - t if tex["bass_dur"] == "hold" else min(tex["bass_dur"], nxt - t)
        bass.append((t, dur, [_place(rn.bass(), blo, bhi)], fig))

    upper = []
    prev_voicing = None
    for u in range(int(round(total / unit))):
        u0 = u * unit
        for off, dur, role in tex["upper"]:
            t = u0 + off
            _, cb, fig = _active(tl, t)
            dur = min(dur, cb - t)  # never sound a chord tone into the next chord
            rn = roman.RomanNumeral(fig, s.k)
            if role in ("hi", "mid"):
                b = [ps[0] for (bt, _bd, ps, _f) in bass if bt <= t + 1e-9][-1]  # bass sounding at t
                ups = sorted((_above(p, b.midi) for p in _upper_members(rn, 2)), key=lambda q: q.midi)
                if len(ups) < 2:
                    ups = ups + [_above(ups[0], ups[0].midi)]
                upper.append((t, dur, [ups[1] if role == "hi" else ups[0]], fig))
            else:
                clo, chi = (s.tonic_ref + x for x in tex["chord_window"])
                cands = _voicings(_upper_members(rn, 3), clo, chi)
                if not cands:
                    raise ValueError(f"{s.stim_id}: no voicing for {fig} in [{clo},{chi}]")
                if prev_voicing is None:
                    centre = (clo + chi) / 2
                    v = min(cands, key=lambda c: abs(sum(p.midi for p in c) / len(c) - centre))
                else:
                    v = min(cands, key=lambda c: sum(abs(a.midi - b.midi) for a, b in zip(c, prev_voicing)))
                prev_voicing = v
                upper.append((t, dur, v, fig))
    return bass, upper


# --------------------------------------------------------------------------
# velocities
# --------------------------------------------------------------------------
def _metric_velocity(offset: float, meter_str: str, base: int) -> int:
    """Downbeat +10, secondary strong beat +4, off-beat -6 (beat = quarter in
    simple meters, dotted quarter in compound meters)."""
    num, den = (int(x) for x in meter_str.split("/"))
    bar_ql = num * 4.0 / den
    pos = offset % bar_ql
    unit = 1.5 if meter_str in COMPOUND_METERS else 1.0
    if abs(pos) < 1e-9:
        v = base + 10
    elif any(abs(pos - b) < 1e-9 for b in STRONG_BEATS.get(meter_str, (0.0,))):
        v = base + 4
    elif abs(pos / unit - round(pos / unit)) > 1e-9:
        v = base - 6
    else:
        v = base
    return max(1, min(127, v))


# --------------------------------------------------------------------------
# score
# --------------------------------------------------------------------------
def _part(name: str, inst_name: str, s: Stim, clef_obj=None) -> stream.Part:
    p = stream.Part()
    p.id = name
    p.partName = name
    p.insert(0, make_instrument(inst_name))
    if clef_obj is not None:
        p.insert(0, clef_obj)
    p.insert(0, s.k.__class__(s.k.tonic.name, s.k.mode))
    p.insert(0, meter.TimeSignature(s.meter))
    if s.meter in COMPOUND_METERS:  # idiomatic dotted-quarter beat; MIDI tempo is unchanged
        p.insert(0, tempo.MetronomeMark(number=round(s.bpm / 1.5, 2), referent=duration.Duration(1.5)))
    else:
        p.insert(0, tempo.MetronomeMark(number=s.bpm))
    return p


def build_score(s: Stim, parts=("melody", "accomp"), annotate: bool = True) -> stream.Score:
    sc = stream.Score()
    sc.insert(0, _metadata(s))
    bar_ql = s.bar_ql
    if "melody" in parts:
        mel = _part(INSTRUMENTS[s.melody_inst][1], s.melody_inst, s, clef.TrebleClef())
        t = 0.0
        for seg in s.segments:
            if annotate:
                te = expressions.TextExpression(seg.label)
                te.placement = "above"
                mel.insert(t, te)
            for n in seg.notes:
                nn = note.Note(copy.deepcopy(n.p), quarterLength=n.dur)
                nn.volume.velocity = _metric_velocity(t, s.meter, 84)
                mel.insert(t, nn)
                t += n.dur
        sc.insert(0, mel)
    if "accomp" in parts:
        bass_ev, up_ev = realize_accompaniment(s)
        acc_label = INSTRUMENTS[s.accomp_inst][1]
        up = _part(f"{acc_label} (upper)", s.accomp_inst, s)
        lo = _part(f"{acc_label} (bass)", s.accomp_inst, s, clef.BassClef())
        last_fig = None
        for t, d, ps, fig in bass_ev:
            n = note.Note(copy.deepcopy(ps[0]), quarterLength=d)
            n.volume.velocity = _metric_velocity(t, s.meter, 62)
            if annotate and fig != last_fig:
                n.addLyric(fig)
            last_fig = fig
            lo.insert(t, n)
        for t, d, ps, _ in up_ev:
            obj = note.Note(copy.deepcopy(ps[0]), quarterLength=d) if len(ps) == 1 else \
                m21chord.Chord([copy.deepcopy(p) for p in ps], quarterLength=d)
            obj.volume.velocity = _metric_velocity(t, s.meter, 50)
            up.insert(t, obj)
        _fill_rests(up, s.total_ql)
        sc.insert(0, up)
        sc.insert(0, lo)
    return sc


def _fill_rests(p: stream.Part, total: float) -> None:
    """Insert explicit rests in the gaps of a sparse part (clean notation)."""
    events = sorted(((e.offset, e.quarterLength) for e in p.notes), key=lambda x: x[0])
    t = 0.0
    for off, ql in events:
        if off > t + 1e-9:
            p.insert(t, note.Rest(quarterLength=off - t))
        t = max(t, off + ql)
    if total > t + 1e-9:
        p.insert(t, note.Rest(quarterLength=total - t))


def _metadata(s: Stim):
    from music21 import metadata
    md = metadata.Metadata()
    md.title = f"musiPAM {s.theme_id} — {s.condition}"
    md.composer = "musiPAM stimulus pipeline (v2)"
    return md
