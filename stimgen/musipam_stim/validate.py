"""Objective checks. Nothing here certifies musical quality or familiarity —
those need listeners. These checks certify that each stimulus is what the
design says it is."""
from __future__ import annotations

from dataclasses import dataclass

from .theory import KeyInfo, chord_pcs
from .themes import STRONG_BEATS, THEMES, Stim
from .transforms import flat_notes, note_chord_figs

RANGES = {"clarinet": (50, 94), "violin": (55, 100)}  # comfortable sounding ranges (MIDI)


@dataclass
class Check:
    stim_id: str
    name: str
    ok: bool
    detail: str = ""
    severity: str = "error"  # "error" fails the build; "info" is reported only


def _seq(s: Stim):
    return [(n.p.nameWithOctave, n.dur) for n in flat_notes(s)]


def _onsets(notes):
    t, out = 0.0, []
    for n in notes:
        out.append(t)
        t += n.dur
    return out


def check_stim(s: Stim, ident: Stim) -> list[Check]:
    sid, out = s.stim_id, []
    add = lambda name, ok, detail="", sev="error": out.append(Check(sid, name, bool(ok), detail, sev))

    # --- form -------------------------------------------------------------
    add("whole_bars", abs(s.total_ql / s.bar_ql - round(s.total_ql / s.bar_ql)) < 1e-9,
        f"{s.total_ql} ql = {s.total_ql / s.bar_ql:g} bars")
    t, on_bar = 0.0, True
    for seg in s.segments:
        on_bar &= abs(t / s.bar_ql - round(t / s.bar_ql)) < 1e-9
        t += seg.dur
    add("motifs_on_barlines", on_bar)
    add("harmony_matches_melody", all(abs(sum(c.dur for c in g.chords) - g.dur) < 1e-9 for g in s.segments))
    add("four_motifs_each_once", sorted(g.src for g in s.segments) == [0, 1, 2, 3],
        " ".join(g.label for g in s.segments))

    # --- melody/harmony agreement ----------------------------------------
    figs = note_chord_figs(s)
    strong, hits = 0, 0
    for n, t0, f in zip(flat_notes(s), _onsets(flat_notes(s)), figs):
        pos = t0 % s.bar_ql
        if any(abs(pos - b) < 1e-9 for b in STRONG_BEATS.get(s.meter, (0.0,))):
            strong += 1
            hits += n.p.pitchClass in chord_pcs(f, s.k)
    rate = hits / strong if strong else 1.0
    add("strong_beat_chord_tones", rate >= 0.6, f"{hits}/{strong} = {rate:.0%} (accented dissonances are by design)",
        "info" if rate >= 0.6 else "error")

    # --- playability --------------------------------------------------------
    lo, hi = RANGES[s.melody_inst]
    mids = [n.p.midi for n in flat_notes(s)]
    add("melody_in_range", lo <= min(mids) and max(mids) <= hi,
        f"{min(mids)}-{max(mids)} vs {s.melody_inst} {lo}-{hi}")
    aug2 = [(a.p.nameWithOctave, b.p.nameWithOctave) for a, b in zip(flat_notes(s), flat_notes(s)[1:])
            if abs(b.p.diatonicNoteNum - a.p.diatonicNoteNum) == 1 and abs(b.p.midi - a.p.midi) == 3]
    add("no_augmented_seconds", not aug2, ", ".join(f"{a}-{b}" for a, b in aug2) or "none", "info")

    # --- the transformation did exactly what it claims ----------------------
    c = s.condition
    I, S = flat_notes(ident), flat_notes(s)
    if c in ("identity", "timbre", "tempo"):
        add("notes_identical", _seq(s) == _seq(ident))
    elif c == "transpose":
        add("exact_tritone_shift", len(I) == len(S) and all(b.p.midi - a.p.midi == -6 and a.dur == b.dur
                                                              for a, b in zip(I, S)))
    elif c == "mode":
        ki = KeyInfo(s.k)
        diffs = [(a, b) for a, b in zip(I, S) if a.p.midi != b.p.midi]
        add("only_degrees_3_6_7_move_one_semitone",
            len(I) == len(S) and all(a.p.diatonicNoteNum == b.p.diatonicNoteNum for a, b in zip(I, S))
            and all(abs(a.p.midi - b.p.midi) == 1 and ki.degree_of(b.p) in (2, 5, 6) for a, b in diffs),
            f"{len(diffs)} notes altered")
    elif c == "ornament":
        on_s = dict(zip([round(x, 6) for x in _onsets(S)], S))
        kept = all(round(t0, 6) in on_s and on_s[round(t0, 6)].p.midi == n.p.midi
                   for n, t0 in zip(I, _onsets(I)))
        add("structural_tones_keep_onsets", kept, f"+{len(S) - len(I)} ornamental notes")
    elif c == "augment":
        a, b = ident.segments[1].notes, s.segments[1].notes
        add("motif2_durations_doubled", all(x.p.midi == y.p.midi and abs(y.dur - 2 * x.dur) < 1e-9
                                            for x, y in zip(a, b)) and len(a) == len(b))
        add("other_motifs_untouched", all([(n.p.midi, n.dur) for n in s.segments[i].notes] ==
                                          [(n.p.midi, n.dur) for n in ident.segments[i].notes] for i in (0, 2, 3)))
    elif c in ("reorder", "motif_retro"):
        by_src = {g.src: [(n.p.midi, n.dur) for n in g.notes] for g in ident.segments}
        add("motifs_intact", all([(n.p.midi, n.dur) for n in g.notes] == by_src[g.src] for g in s.segments),
            " ".join(g.label for g in s.segments))
    elif c == "invert":
        di = [b.p.diatonicNoteNum - a.p.diatonicNoteNum for a, b in zip(I, I[1:])]
        ds = [b.p.diatonicNoteNum - a.p.diatonicNoteNum for a, b in zip(S, S[1:])]
        add("diatonic_intervals_negated", ds == [-x for x in di] and [n.dur for n in I] == [n.dur for n in S],
            f"axis {s.notes_meta.get('axis')}")
    elif c == "retrograde":
        add("exact_reversal", [(n.p.midi, n.dur) for n in S] == [(n.p.midi, n.dur) for n in I][::-1])
    return out


def check_designed_relations(stims: dict[str, Stim]) -> list[Check]:
    """The relational skeleton the themes were composed to have."""
    out = []

    def steps(notes):
        return [b.p.diatonicNoteNum - a.p.diatonicNoteNum for a, b in zip(notes, notes[1:])]

    for tid in ("T1", "T3"):
        a, a2, b = (stims[tid].segments[i].notes for i in (0, 1, 2))
        out.append(Check(tid, "a'_is_a_up_one_diatonic_step",
                         len(a) == len(a2) and all(y.p.diatonicNoteNum - x.p.diatonicNoteNum == 1 and x.dur == y.dur
                                                   for x, y in zip(a, a2))))
        head = [n.dur for n in a][: 3 if tid == "T1" else 2]
        bd = [n.dur for n in b]
        k = len(head)
        out.append(Check(tid, "b_fragments_a_head_rhythm",
                         bd[: 3 * k] == head * 3, f"head {head}, b {bd}"))
    # periods: identical a1/a2; c shares b's rhythm and opening notes, then closes elsewhere
    for tid, k in (("T2", 5), ("T4", 2)):
        segs = stims[tid].segments
        out.append(Check(tid, "a1_equals_a2", [(n.p.midi, n.dur) for n in segs[0].notes] ==
                         [(n.p.midi, n.dur) for n in segs[2].notes]))
        b, c = segs[1].notes, segs[3].notes
        out.append(Check(tid, "c_restates_b_then_cadences",
                         [n.dur for n in b] == [n.dur for n in c]
                         and [n.p.midi for n in b[:k]] == [n.p.midi for n in c[:k]]
                         and b[-1].p.midi != c[-1].p.midi, f"shared opening notes: {k}"))

    # cross-mappings: a motif in one role copies the shape of the partner theme's motif in another
    for (src, si), (dst, di), name in ((("T1", 0), ("T3", 3), "cross_mapping_T3c_has_T1a_shape"),
                                       (("T2", 1), ("T4", 0), "cross_mapping_T4a_has_T2b_shape")):
        x, y = stims[src].segments[si].notes, stims[dst].segments[di].notes
        out.append(Check(f"{src}/{dst}", name, [n.dur for n in x] == [n.dur for n in y] and steps(x) == steps(y),
                         f"steps {steps(x)}"))
    for a, b, name in (("T1", "T3", "T3a_differs_from_T1a"), ("T2", "T4", "T4a_differs_from_T2a")):
        x, y = stims[a].segments[0].notes, stims[b].segments[0].notes
        out.append(Check(f"{a}/{b}", name, [n.dur for n in x] != [n.dur for n in y] and steps(x) != steps(y)))
    return out


def check_audio(sid: str, stats, expected_s: float) -> list[Check]:
    return [
        Check(sid, "loudness_on_target", abs(stats.lufs - (-20.0)) <= 0.5, f"{stats.lufs:.2f} LUFS"),
        Check(sid, "no_clipping", stats.peak_dbfs <= -1.0 + 1e-6, f"peak {stats.peak_dbfs:.2f} dBFS"),
        Check(sid, "peak_limiting_not_needed", not stats.limited, "", "info"),
        Check(sid, "duration_as_expected", abs(stats.duration_s - expected_s) < 0.05,
              f"{stats.duration_s:.2f}s vs {expected_s:.2f}s"),
    ]
