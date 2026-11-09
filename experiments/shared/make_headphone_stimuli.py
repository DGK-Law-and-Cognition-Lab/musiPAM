"""Headphone-screen stimuli (Huggins pitch; Milne et al., 2021) and a volume-calibration sound.

Each trial is three 1-s bursts of white noise separated by 0.5 s of silence. In one
burst (the target), a narrow band around 600 Hz (±6%) is phase-inverted in the right
ear relative to the left. Over headphones that band is heard as a faint tone; over
loudspeakers the two ears mix and the tone disappears. The other bursts are identical
in both ears. Files are 16-bit stereo WAV: lossy stereo coding could destroy the
interaural phase difference the test depends on.

    make(out_dir) -> [{"file": "hp/hp1.wav", "answer": 2}, ...], "hp/calibration.wav"

Deterministic (fixed seed), so every build makes the same files.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf

SR = 44100
BURST_S, GAP_S, RAMP_S = 1.0, 0.5, 0.01
CENTER_HZ, HALF_BW = 600.0, 0.06
NOISE_RMS = 10 ** (-30 / 20)          # -30 dBFS RMS
ANSWERS = [2, 1, 3, 3, 1, 2]           # target position per trial, balanced


def _ramp(x: np.ndarray) -> np.ndarray:
    n = int(RAMP_S * SR)
    w = np.ones(len(x))
    r = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, n))
    w[:n], w[-n:] = r, r[::-1]
    return x * w


def _burst(rng: np.random.Generator, target: bool) -> np.ndarray:
    n = int(BURST_S * SR)
    left = rng.standard_normal(n)
    right = left.copy()
    if target:
        spec = np.fft.rfft(left)
        f = np.fft.rfftfreq(n, 1 / SR)
        band = (f >= CENTER_HZ * (1 - HALF_BW)) & (f <= CENTER_HZ * (1 + HALF_BW))
        spec[band] *= -1.0                      # interaural phase inversion of the band
        right = np.fft.irfft(spec, n)
    st = np.stack([left, right], 1)
    st *= NOISE_RMS / np.sqrt((st ** 2).mean())
    return np.stack([_ramp(st[:, 0]), _ramp(st[:, 1])], 1)


def make(out_dir: Path) -> tuple[list[dict], str]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(20211001)
    gap = np.zeros((int(GAP_S * SR), 2))
    trials = []
    for i, ans in enumerate(ANSWERS, 1):
        parts = []
        for pos in (1, 2, 3):
            parts += [_burst(rng, pos == ans), gap]
        sf.write(out_dir / f"hp{i}.wav", np.concatenate(parts[:-1]), SR, subtype="PCM_16")
        trials.append({"file": f"{out_dir.name}/hp{i}.wav", "answer": ans})
    # calibration: a soft, slow arpeggio of harmonic tones, about the stimuli's loudness
    t = np.arange(int(0.6 * SR)) / SR
    notes = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 261.63, 196.00] * 2
    tones = []
    for f0 in notes:
        tone = sum(np.sin(2 * np.pi * f0 * k * t) / k ** 1.5 for k in range(1, 6))
        tones.append(tone * np.exp(-3.0 * t))
    x = np.concatenate(tones)
    x = 0.25 * x / np.abs(x).max()
    sf.write(out_dir / "calibration.wav", np.stack([x, x], 1), SR, subtype="PCM_16")
    return trials, f"{out_dir.name}/calibration.wav"


if __name__ == "__main__":
    import sys
    print(make(Path(sys.argv[1] if len(sys.argv) > 1 else "hp")))
