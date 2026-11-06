"""Deterministic audio rendering.

Each stimulus is rendered as two stems (melody, accompaniment) through
FluidSynth with one fixed soundfont. Stems are mixed with the melody a fixed
number of LU above the accompaniment, so melody/accompaniment balance is
identical across conditions; the mix is then loudness-normalized, so overall
level is identical too. The renderer is swappable (see ``SOUNDFONT``): an
upgrade to a better sample library changes timbre for *every* stimulus
equally.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

# Pinned copy, so a MuseScore/Muse Hub update can neither break the build nor
# silently change the audio. Restore it from any MuseScore 4 app bundle
# (Contents/Resources/sound/MS Basic.sf3); the hash check catches a different file.
SOUNDFONT = Path(os.environ.get("MUSIPAM_SOUNDFONT", Path.home() / ".venvs/musipam/soundfonts/MS Basic.sf3"))
SOUNDFONT_SHA256 = "5ea2375e8bd7d8e71def1036978c1621e85b66934169b6a2744b27b9b3c2d99c"


def check_soundfont() -> str:
    if not SOUNDFONT.exists():
        raise FileNotFoundError(f"soundfont missing: {SOUNDFONT} (copy MS Basic.sf3 from the MuseScore 4 app bundle)")
    digest = hashlib.sha256(SOUNDFONT.read_bytes()).hexdigest()
    if digest != SOUNDFONT_SHA256 and "MUSIPAM_SOUNDFONT" not in os.environ:
        raise ValueError(f"{SOUNDFONT} has hash {digest[:12]}..., not the pinned {SOUNDFONT_SHA256[:12]}...; "
                         "audio would differ from the recorded stimuli. Set MUSIPAM_SOUNDFONT to use it deliberately.")
    return digest
SR = 44100
TARGET_LUFS = -20.0
MELODY_OVER_ACCOMP_LU = 6.0
PEAK_CEILING_DBFS = -1.0
LEAD_IN_S = 0.10
TAIL_S = 1.50
FADE_S = 0.40


@dataclass
class RenderStats:
    duration_s: float
    lufs: float
    peak_dbfs: float
    melody_lufs_raw: float
    accomp_lufs_raw: float
    limited: bool


def fluidsynth(mid: Path, wav: Path) -> None:
    # dynamic sample loading: ~4.6x faster with the compressed .sf3, bit-identical output
    cmd = ["fluidsynth", "-ni", "-q", "-F", str(wav), "-r", str(SR), "-g", "0.5",
           "-o", "audio.file.format=float", "-o", "synth.dynamic-sample-loading=1",
           str(SOUNDFONT), str(mid)]
    subprocess.run(cmd, check=True, capture_output=True)


def _load(path: Path) -> np.ndarray:
    x, sr = sf.read(str(path), always_2d=True, dtype="float64")
    if sr != SR:
        raise ValueError(f"{path}: sample rate {sr}")
    return x


def mix_master(mel_wav: Path, acc_wav: Path, music_end_s: float, out_wav: Path, out_mp3: Path) -> RenderStats:
    m, a = _load(mel_wav), _load(acc_wav)
    n = max(len(m), len(a))
    m = np.pad(m, ((0, n - len(m)), (0, 0)))
    a = np.pad(a, ((0, n - len(a)), (0, 0)))
    meter = pyln.Meter(SR)
    lm, la = meter.integrated_loudness(m), meter.integrated_loudness(a)
    mix = m + a * 10 ** ((lm - MELODY_OVER_ACCOMP_LU - la) / 20)

    # trim: keep the music plus a fixed tail, fade the tail end, add lead-in
    keep = int(round((music_end_s + TAIL_S) * SR))
    mix = mix[:keep] if len(mix) >= keep else np.pad(mix, ((0, keep - len(mix)), (0, 0)))
    nf = int(FADE_S * SR)
    mix[-nf:] *= np.linspace(1.0, 0.0, nf)[:, None]
    mix = np.vstack([np.zeros((int(LEAD_IN_S * SR), mix.shape[1])), mix])

    mix *= 10 ** ((TARGET_LUFS - meter.integrated_loudness(mix)) / 20)
    peak = 20 * np.log10(np.max(np.abs(mix)))
    limited = peak > PEAK_CEILING_DBFS
    if limited:  # never clip: pull the whole file down (reported, not hidden)
        mix *= 10 ** ((PEAK_CEILING_DBFS - peak) / 20)
        peak = PEAK_CEILING_DBFS
    sf.write(str(out_wav), mix, SR, subtype="PCM_16")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out_wav), "-codec:a", "libmp3lame",
                    "-b:a", "192k", str(out_mp3)], check=True)
    return RenderStats(duration_s=len(mix) / SR, lufs=meter.integrated_loudness(mix), peak_dbfs=float(peak),
                       melody_lufs_raw=float(lm), accomp_lufs_raw=float(la), limited=bool(limited))
