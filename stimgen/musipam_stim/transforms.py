"""The transformation grid.

Each condition is defined by what it does to the motif graph:

    nodes = the motifs themselves     edges = relations between motifs

Every transformation acts on the melody *and* the harmonic plan, so the
re-realized accompaniment always agrees with the transformed melody.
"""
from __future__ import annotations

from music21 import interval
from music21 import key as m21key
from music21 import pitch

from .theory import (KeyInfo, chord_pcs, invert_rn, minor_alterations,
                     remap_progression)
from .themes import THEMES, MNote, Stim

CONDITIONS: list[tuple[str, str, str]] = [
    ("identity", "control",
     "The theme as composed."),
    ("timbre", "surface",
     "Melody clarinet -> violin, accompaniment piano -> harp. Notes identical."),
    ("tempo", "surface",
     "Tempo x1.3. Notes identical."),
    ("transpose", "probe: pitch coding",
     "Whole passage down a tritone, the most distant key. Unchanged under key-relative "
     "coding; every node changes under absolute-pitch coding."),
    ("mode", "nodes only",
     "Parallel mode (major <-> minor). Scale degrees 3, 6, 7 altered; contour, rhythm, "
     "form and relations intact."),
    ("ornament", "nodes only",
     "Passing tones fill melodic thirds; neighbor-note turns decorate long notes. "
     "Every structural tone keeps its onset."),
    ("augment", "probe: time coding",
     "Motif 2 in rhythmic augmentation (x2). Under scale-free rhythm coding only the "
     "duration relations change; under absolute coding node 2 changes as well."),
    ("reorder", "temporal edges",
     "Motifs 2 and 3 exchange places. Every motif identical; only temporal relations change "
     "(derivational ones such as 'a' is a sequence of a' survive)."),
    ("motif_retro", "temporal edges",
     "Motif order reversed (4 3 2 1); each motif intact and played forwards."),
    ("invert", "nodes + edges",
     "Diatonic inversion about scale degree 3: the tonic triad maps onto itself, "
     "dominant and subdominant exchange. Harmony inverted with the melody."),
    ("retrograde", "nodes + edges",
     "Note-level retrograde: the whole passage backwards, melody and harmony."),
]
CELL = {c: cell for c, cell, _ in CONDITIONS}
DESCRIPTION = {c: d for c, _, d in CONDITIONS}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def flat_notes(s: Stim) -> list[MNote]:
    return [n for seg in s.segments for n in seg.notes]


def note_chord_figs(s: Stim) -> list[str]:
    """Roman numeral active at each melody note's onset."""
    figs = []
    for seg in s.segments:
        spans, t, acc = [], 0.0, 0.0
        for ch in seg.chords:
            spans.append((acc, acc + ch.dur, ch.fig))
            acc += ch.dur
        for n in seg.notes:
            figs.append(next(f for a, b, f in spans if a - 1e-9 <= t < b - 1e-9))
            t += n.dur
    return figs


def _all_figs(s: Stim) -> list[str]:
    return [ch.fig for seg in s.segments for ch in seg.chords]


def _set_figs(s: Stim, figs: list[str]) -> None:
    it = iter(figs)
    for seg in s.segments:
        for ch in seg.chords:
            ch.fig = next(it)


def _weighted_mean_midi(notes: list[MNote]) -> float:
    return sum(n.p.midi * n.dur for n in notes) / sum(n.dur for n in notes)


def _respell_melody(s: Stim, dnns: list[int], only_added: bool = False) -> None:
    """Spell melody notes at the given diatonic positions in ``s.k``.

    Minor keys get context-dependent raised 6th/7th degrees (see
    ``theory.minor_alterations``). With ``only_added`` the composed notes
    keep their original pitches and only ornamental notes are re-spelled.
    """
    ki = KeyInfo(s.k)
    pcsets = [chord_pcs(f, s.k) for f in note_chord_figs(s)]
    alters = minor_alterations(dnns, pcsets, ki)
    for n, d, a in zip(flat_notes(s), dnns, alters):
        if only_added and n.kind not in ("passing", "neighbor"):
            continue
        n.p = ki.spell(d, a)


# --------------------------------------------------------------------------
# transformations
# --------------------------------------------------------------------------
def t_identity(s: Stim) -> Stim:
    return s.clone("identity")


def t_timbre(s: Stim) -> Stim:
    c = s.clone("timbre")
    c.melody_inst, c.accomp_inst = "violin", "harp"
    return c


def t_tempo(s: Stim) -> Stim:
    c = s.clone("tempo")
    c.bpm = round(s.bpm * 1.3)
    return c


def t_transpose(s: Stim) -> Stim:
    c = s.clone("transpose")
    new_k = m21key.Key(THEMES[s.theme_id].tritone_key)
    old_t = pitch.Pitch(f"{s.k.tonic.name}4")
    new_t = pitch.Pitch(f"{new_k.tonic.name}4")
    while new_t.midi > old_t.midi:
        new_t.octave -= 1
    if old_t.midi - new_t.midi != 6:
        raise ValueError(f"{s.theme_id}: {new_k} is not a tritone below {s.k}")
    iv = interval.Interval(old_t, new_t)
    for n in flat_notes(c):
        n.p = n.p.transpose(iv)
    c.k = new_k
    c.tonic_ref = s.tonic_ref - 6
    c.notes_meta["interval"] = iv.directedName
    return c


def t_mode(s: Stim) -> Stim:
    c = s.clone("mode")
    new_mode = "minor" if s.k.mode == "major" else "major"
    c.k = m21key.Key(s.k.tonic.name, new_mode)
    _set_figs(c, remap_progression(_all_figs(s), s.k.mode, new_mode))
    _respell_melody(c, [n.p.diatonicNoteNum for n in flat_notes(c)])
    return c


def t_ornament(s: Stim) -> Stim:
    c = s.clone("ornament")
    seq = flat_notes(c)
    nxt_of = {id(n): (seq[i + 1] if i + 1 < len(seq) else None) for i, n in enumerate(seq)}
    for seg in c.segments:
        out: list[MNote] = []
        for n in seg.notes:
            nxt = nxt_of[id(n)]
            if nxt is None:  # never decorate the final note
                out.append(n)
                continue
            d0, d1 = n.p.diatonicNoteNum, nxt.p.diatonicNoteNum
            if n.dur >= 1.0 and abs(d1 - d0) == 2:            # passing tone through a third
                step = 1 if d1 > d0 else -1
                out += [MNote(n.p, n.dur - 0.5), MNote(_dnn_pitch(d0 + step), 0.5, "passing")]
            elif n.dur >= 2.0:                                  # neighbor-note turn on long notes
                out += [MNote(n.p, n.dur - 1.0), MNote(_dnn_pitch(d0 + 1), 0.5, "neighbor"),
                        MNote(pitch.Pitch(n.p.nameWithOctave), 0.5, "restrike")]
            else:
                out.append(n)
        seg.notes = out
    _respell_melody(c, [n.p.diatonicNoteNum for n in flat_notes(c)], only_added=True)
    return c


def _dnn_pitch(dnn: int) -> pitch.Pitch:
    """Placeholder pitch at a diatonic position (respelled in key later)."""
    p = pitch.Pitch("C4")
    p.diatonicNoteNum = dnn
    return p


def t_augment(s: Stim) -> Stim:
    c = s.clone("augment")
    seg = c.segments[1]
    for n in seg.notes:
        n.dur *= 2
    for ch in seg.chords:
        ch.dur *= 2
    return c


def t_reorder(s: Stim) -> Stim:
    c = s.clone("reorder")
    a, b, cc, d = c.segments
    c.segments = [a, cc, b, d]
    return c


def t_motif_retro(s: Stim) -> Stim:
    c = s.clone("motif_retro")
    c.segments = c.segments[::-1]
    return c


def t_invert(s: Stim) -> Stim:
    c = s.clone("invert")
    ki = KeyInfo(c.k)
    _set_figs(c, remap_progression(_all_figs(s), s.k.mode, s.k.mode, root_map=invert_rn))
    axis = ki.tonic_dnn4 + 2  # scale degree 3, octave 4
    base = [2 * axis - n.p.diatonicNoteNum for n in flat_notes(s)]
    target = _weighted_mean_midi(flat_notes(s))
    best = None
    for shift in (-14, -7, 0, 7, 14):  # octave shifts keep the tonal mapping intact
        _respell_melody(c, [d + shift for d in base])
        dev = abs(_weighted_mean_midi(flat_notes(c)) - target)
        if best is None or dev < best[0]:
            best = (dev, shift)
    _respell_melody(c, [d + best[1] for d in base])
    c.notes_meta["axis"] = KeyInfo(c.k).spell(axis + best[1]).nameWithOctave
    return c


def t_retrograde(s: Stim) -> Stim:
    c = s.clone("retrograde")
    c.segments = c.segments[::-1]
    for seg in c.segments:
        seg.notes = seg.notes[::-1]
        seg.chords = seg.chords[::-1]
    return c


TRANSFORMS = {
    "identity": t_identity, "timbre": t_timbre, "tempo": t_tempo, "transpose": t_transpose,
    "mode": t_mode, "ornament": t_ornament, "augment": t_augment, "reorder": t_reorder,
    "motif_retro": t_motif_retro, "invert": t_invert, "retrograde": t_retrograde,
}
