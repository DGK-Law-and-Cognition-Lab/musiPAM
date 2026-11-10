"""Render the Study 0 anchor melodies and the practice melody (musipam_stim/anchors.py).

    ~/.venvs/musipam/bin/python build_anchors.py [--out ../stimuli/anchors] [--renderer muse|fluidsynth]

Same rendering path as build.py (Muse Sounds stems, mix, -20 LUFS), so a renderer change
applies to the anchors too. Writes MusicXML, MIDI, WAV, MP3, manifest.csv and renderer.json.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # keep __pycache__ out of Google Drive

import argparse
import json
import tempfile
from pathlib import Path

from build import _drop_encoding_date, _write_csv, render_stims, renderer_info
from musipam_stim.anchors import ANCHORS, anchor_stim
from musipam_stim.arrange import INSTRUMENTS, build_score, realize_accompaniment
from musipam_stim.render import LEAD_IN_S


def crossings(s) -> int:
    """Melody notes that sound at or below a simultaneous accompaniment note."""
    _, upper = realize_accompaniment(s)
    n, t = 0, 0.0
    for seg in s.segments:
        for mn in seg.notes:
            if mn.p is not None:
                top = [max(p.midi for p in ps) for (u, d, ps, _) in upper if u < t + mn.dur - 1e-9 and u + d > t + 1e-9]
                n += bool(top) and max(top) >= mn.p.midi
            t += mn.dur
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent / "stimuli" / "anchors"))
    ap.add_argument("--renderer", choices=("muse", "fluidsynth"), default="muse")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="musipam_anchors_"))
    (out / "renderer.json").write_text(json.dumps(renderer_info(args.renderer, scratch), indent=1) + "\n")
    stims = {aid: anchor_stim(aid) for aid in ANCHORS}
    done = render_stims([(s, out) for s in stims.values()], scratch, args.renderer)
    failed = [c for r in done.values() for c in r["checks"] if not c.ok and c.severity == "error"]
    rows = []
    for aid, a in ANCHORS.items():
        s = stims[aid]
        sid = s.stim_id
        score = build_score(s)
        xml = out / f"{sid}.musicxml"
        score.write("musicxml", fp=str(xml))
        _drop_encoding_date(xml)
        score.write("midi", fp=str(out / f"{sid}.mid"))
        music_s = s.total_ql * 60.0 / s.bpm
        r = done[sid]
        onsets, t = [], 0.0
        for seg in s.segments:
            onsets.append(t * 60.0 / s.bpm + LEAD_IN_S)
            t += seg.dur
        x = crossings(s)
        rows.append({
            "id": sid, "anchor": aid, "kind": a.kind, "title": a.title, "source": a.source, "excerpt": a.excerpt,
            "key": f"{s.k.tonic.name} {s.k.mode}", "meter": s.meter, "bpm": s.bpm,
            "bars": round(s.total_ql / s.bar_ql), "music_s": round(music_s, 3),
            "melody_instrument": INSTRUMENTS[s.melody_inst][1], "accomp_instrument": INSTRUMENTS[s.accomp_inst][1],
            "boundaries_s": " ".join(f"{o:.3f}" for o in onsets[1:]),
            "renderer": r["renderer"], "melody_sound": r["melody_sound"], "accomp_sound": r["accomp_sound"],
            "melody_onset_offset_ms": r["melody_onset_offset_ms"], "accomp_onset_offset_ms": r["accomp_onset_offset_ms"],
            "musicxml": xml.name, "midi": f"{sid}.mid", "wav": f"{sid}.wav", "mp3": f"{sid}.mp3",
            "duration_s": r["duration_s"], "lufs": r["lufs"], "peak_dbfs": r["peak_dbfs"], "wav_sha256": r["wav_sha256"],
        })
        print(f"  built {sid}: {a.title}, {rows[-1]['bars']} bars, {r['duration_s']:.1f} s, {r['lufs']:.1f} LUFS, "
              f"onsets {r['melody_onset_offset_ms']:+d}/{r['accomp_onset_offset_ms']:+d} ms, "
              f"melody/accompaniment crossings: {x}", flush=True)
    _write_csv(out / "manifest.csv", rows)
    print(f"{len(rows)} melodies -> {out}")
    for c in failed:
        print(f"  FAIL {c.stim_id} {c.name}: {c.detail}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
