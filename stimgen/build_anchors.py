"""Render the Study 0 anchor melodies and the practice melody (musipam_stim/anchors.py).

    ~/.venvs/musipam/bin/python build_anchors.py [--out ../stimuli/anchors]

Same rendering path as build.py (stems, mix, -20 LUFS), so a renderer change applies to
the anchors too. Writes MusicXML, MIDI, WAV, MP3 and manifest.csv.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # keep __pycache__ out of Google Drive

import argparse
import tempfile
from pathlib import Path

from build import _drop_encoding_date, _write_csv, sha256
from musipam_stim.anchors import ANCHORS, anchor_stim
from musipam_stim.arrange import INSTRUMENTS, build_score, realize_accompaniment
from musipam_stim.render import LEAD_IN_S, check_soundfont, fluidsynth, mix_master


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
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="musipam_anchors_"))
    print(f"soundfont sha256 {check_soundfont()[:16]}... ok", flush=True)
    rows = []
    for aid, a in ANCHORS.items():
        s = anchor_stim(aid)
        sid = s.stim_id
        score = build_score(s)
        xml = out / f"{sid}.musicxml"
        score.write("musicxml", fp=str(xml))
        _drop_encoding_date(xml)
        score.write("midi", fp=str(out / f"{sid}.mid"))
        mel_mid, acc_mid = scratch / f"{sid}_mel.mid", scratch / f"{sid}_acc.mid"
        build_score(s, parts=("melody",), annotate=False).write("midi", fp=str(mel_mid))
        build_score(s, parts=("accomp",), annotate=False).write("midi", fp=str(acc_mid))
        mel_wav, acc_wav = scratch / f"{sid}_mel.wav", scratch / f"{sid}_acc.wav"
        fluidsynth(mel_mid, mel_wav)
        fluidsynth(acc_mid, acc_wav)
        music_s = s.total_ql * 60.0 / s.bpm
        st = mix_master(mel_wav, acc_wav, music_s, out / f"{sid}.wav", out / f"{sid}.mp3")
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
            "musicxml": xml.name, "midi": f"{sid}.mid", "wav": f"{sid}.wav", "mp3": f"{sid}.mp3",
            "duration_s": round(st.duration_s, 3), "lufs": round(st.lufs, 2), "peak_dbfs": round(st.peak_dbfs, 2),
            "wav_sha256": sha256(out / f"{sid}.wav"),
        })
        print(f"  built {sid}: {a.title}, {rows[-1]['bars']} bars, {st.duration_s:.1f} s, "
              f"{st.lufs:.1f} LUFS, melody/accompaniment crossings: {x}", flush=True)
    _write_csv(out / "manifest.csv", rows)
    print(f"{len(rows)} melodies -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
