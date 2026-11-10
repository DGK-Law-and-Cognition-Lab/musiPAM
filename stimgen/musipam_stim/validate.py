"""Objective checks. Nothing here certifies musical quality or familiarity —
those need listeners. These checks certify that each stimulus is what the
design says it is."""
from __future__ import annotations

from dataclasses import dataclass

from .theory import KeyInfo, chord_pcs
from .themes import CROSS_MAPPINGS, STRONG_BEATS, THEMES, Stim
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

    def shifted(x, y, k):  # y is x moved k diatonic steps, same rhythm
        return len(x) == len(y) and all(b.p.diatonicNoteNum - a.p.diatonicNoteNum == k and a.dur == b.dur
                                        for a, b in zip(x, y))

    def pd(notes):
        return [(n.p.midi, n.dur) for n in notes]

    def bar(notes, i, bar_ql):
        t, sel = 0.0, []
        for n in notes:
            if i * bar_ql - 1e-9 <= t < (i + 1) * bar_ql - 1e-9:
                sel.append(n)
            t += n.dur
        return sel

    for tid, s in stims.items():
        th, seg, ki = THEMES[tid], [g.notes for g in s.segments], KeyInfo(s.k)

        def add(name, ok, detail=""):
            out.append(Check(tid, name, bool(ok), detail))

        if th.skeleton == "sentence":
            add("a'_is_a_up_one_diatonic_step", shifted(seg[0], seg[1], 1))
            head, bd = [n.dur for n in seg[0]][: th.head], [n.dur for n in seg[2]]
            add("b_fragments_a_head_rhythm", th.head > 0 and bd[: 3 * th.head] == head * 3, f"head {head}, b {bd}")
        elif th.skeleton == "period":
            b, c, k = seg[1], seg[3], th.shared_k
            add("a1_equals_a2", pd(seg[0]) == pd(seg[2]))
            add("c_restates_b_then_cadences",
                k > 0 and [n.dur for n in b] == [n.dur for n in c]
                and [n.p.midi for n in b[:k]] == [n.p.midi for n in c[:k]] and b[-1].p.midi != c[-1].p.midi,
                f"shared opening notes: {k}")
        elif th.skeleton == "rounded":
            add("return_keeps_first_bar", pd(bar(seg[0], 0, s.bar_ql)) == pd(bar(seg[3], 0, s.bar_ql)))
            add("return_changes_second_bar", pd(bar(seg[0], 1, s.bar_ql)) != pd(bar(seg[3], 1, s.bar_ql)))
            add("return_closes_on_tonic_a_does_not",
                ki.degree_of(seg[3][-1].p) == 0 and ki.degree_of(seg[0][-1].p) != 0)
        elif th.skeleton == "chain":
            add("a'_is_a_down_one_diatonic_step", shifted(seg[0], seg[1], -1))
            add("a''_is_a_down_two_diatonic_steps", shifted(seg[0], seg[2], -2))
            add("b_closes_on_tonic", ki.degree_of(seg[3][-1].p) == 0)
        else:
            add("skeleton_declared", False, repr(th.skeleton))

    # cross-mappings: the target motif copies the source motif's rhythm and steps in another role,
    # while the target motif that shares the source motif's role looks different
    for src, si, dst, di in CROSS_MAPPINGS:
        S, D = stims[src].segments, stims[dst].segments
        x, y, r = S[si].notes, D[di].notes, D[si].notes
        out.append(Check(f"{src}/{dst}", f"lookalike_{dst}.{D[di].label}_copies_{src}.{S[si].label}",
                         [n.dur for n in x] == [n.dur for n in y] and steps(x) == steps(y), f"steps {steps(x)}"))
        out.append(Check(f"{src}/{dst}", f"role_match_{dst}.{D[si].label}_differs_from_{src}.{S[si].label}",
                         [n.dur for n in x] != [n.dur for n in r] and steps(x) != steps(r)))
    return out


def check_audio(sid: str, stats, expected_s: float) -> list[Check]:
    return [
        Check(sid, "loudness_on_target", abs(stats.lufs - (-20.0)) <= 0.5, f"{stats.lufs:.2f} LUFS"),
        Check(sid, "no_clipping", stats.peak_dbfs <= -1.0 + 1e-6, f"peak {stats.peak_dbfs:.2f} dBFS"),
        Check(sid, "peak_limiting_not_needed", not stats.limited, "", "info"),
        Check(sid, "duration_as_expected", abs(stats.duration_s - expected_s) < 0.05,
              f"{stats.duration_s:.2f}s vs {expected_s:.2f}s"),
    ]


# Largest tolerated median offset of a stem's onsets from the score. Sample-based instruments
# with soft attacks (clarinet, violin) peak later than plucked or struck ones (piano, harp).
ONSET_TOLERANCE_S = {"melody": 0.05, "accomp": 0.02}


def check_alignment(sid: str, part: str, offset_s: float, n: int, strict: bool) -> Check:
    """The rendered stem's notes start where the score says (median spectral-flux onset offset)."""
    ok = n > 0 and abs(offset_s) <= ONSET_TOLERANCE_S[part]
    return Check(sid, f"{part}_onsets_match_score", ok,
                 f"median {offset_s * 1000:+.0f} ms over {n} onsets", "error" if strict else "info")
