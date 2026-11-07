"""A generic symbolic motif code, and the pair encoding the relation model reads.

The motif code describes pitch and time in the key, with no knowledge of the
relation inventory: a time-normalized contour (in scale steps and in
semitones), onset positions, the distributions of durations, pitch classes,
scale degrees and melodic intervals, and a few summary numbers.

A pair (A, B) is encoded as [a, b, b - a, |b - a|, a * b], the standard
relation-agnostic way to compare two vectors (as in natural-language
inference models). The classifiers on top are what learn the relations.
"""
from __future__ import annotations

import numpy as np

from .motif import Motif

GRID = 24
BLOCKS = [("contour", GRID), ("chromatic contour", GRID), ("onsets", GRID), ("durations", 7), ("absolute time", 3),
          ("pitch classes", 12), ("scale degrees", 7), ("intervals", 15), ("summary", 6)]
DIM = sum(n for _, n in BLOCKS)


def motif_code(m: Motif) -> np.ndarray:
    h = np.asarray(m.h, float)
    s = np.asarray(m.semis(), float)
    on, dur, span, n = np.asarray(m.on, float), np.asarray(m.dur, float), float(m.span), m.n
    t = (np.arange(GRID) + 0.5) / GRID * span
    idx = np.clip(np.searchsorted(on, t, side="right") - 1, 0, n - 1)  # the note sounding (or last begun) at t
    contour, chrom = h[idx] / 7.0, s[idx] / 12.0
    onsets = np.zeros(GRID)
    onsets[np.minimum((on / span * GRID).astype(int), GRID - 1)] = 1.0
    rel = np.clip(np.floor(np.log2(np.maximum(dur / span, 2.0 ** -7)) + 7).astype(int), 0, 6)
    durations = np.bincount(rel, minlength=7) / n
    absolute = np.array([np.log2(span), np.log2(n), np.log2(dur).mean()])
    pcs = np.bincount(np.mod(s.astype(int), 12), weights=dur, minlength=12) / dur.sum()
    degrees = np.bincount(np.mod(h.astype(int), 7), weights=dur, minlength=7) / dur.sum()
    iv = np.clip(np.diff(h), -7, 7).astype(int) + 7
    intervals = np.bincount(iv, minlength=15) / max(1, n - 1)
    summary = np.array([h.mean() / 7, h[0] / 7, h[-1] / 7, (h.max() - h.min()) / 7,
                        float(m.h[-1] % 7 == 0), float(m.h[0] % 7 == 0)])
    return np.concatenate([contour, chrom, onsets, durations, absolute, pcs, degrees, intervals, summary])


def codes(motifs: list[Motif]) -> np.ndarray:
    return np.stack([motif_code(m) for m in motifs]).astype(np.float32)


def pair_code(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """[a, b, b - a, |b - a|, a * b] along the last axis."""
    return np.concatenate([a, b, b - a, np.abs(b - a), a * b], axis=-1)
