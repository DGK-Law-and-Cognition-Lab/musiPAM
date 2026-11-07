"""The relation inventory, and the motif-level transforms that instantiate it.

Labels come from music theory (Schoenberg, 1967; Caplin, 1998; Lewin, 1987),
not from the musiPAM stimulus design. Every relation is directed: a pair is
(A, B), and B is what the relation makes of A.

`make(name, A, rng, pool)` returns (A, B, params) or None when the relation
doesn't apply to A (for example, a mode change on a motif that has no 3rd,
6th or 7th degree, which would leave it unchanged).
"""
from __future__ import annotations

import random

from .motif import EPS, SCALES, Motif

# (name, family, what B is)
RELATIONS: list[tuple[str, str, str]] = [
    ("repeat", "repetition", "A again, note for note"),
    ("octave_up", "repetition", "A an octave higher"),
    ("octave_down", "repetition", "A an octave lower"),
    ("seq_up_1", "sequence", "A moved up one scale step (diatonic sequence)"),
    ("seq_up_2", "sequence", "A moved up two scale steps"),
    ("seq_up_3", "sequence", "A moved up three scale steps"),
    ("seq_down_1", "sequence", "A moved down one scale step"),
    ("seq_down_2", "sequence", "A moved down two scale steps"),
    ("seq_down_3", "sequence", "A moved down three scale steps"),
    ("real_up", "sequence", "A moved up 1-5 semitones exactly (real transposition), leaving the key"),
    ("real_down", "sequence", "A moved down 1-5 semitones exactly, leaving the key"),
    ("inversion", "contour", "A's intervals mirrored about its first note, in scale steps"),
    ("retrograde", "contour", "A backwards, pitches and rhythm"),
    ("retro_inversion", "contour", "A mirrored and backwards"),
    ("augmentation", "rhythm", "A in notes twice as long"),
    ("diminution", "rhythm", "A in notes half as long"),
    ("rhythm_new", "rhythm", "A's pitches in another motif's rhythm"),
    ("pitch_new", "rhythm", "A's rhythm with another motif's pitches"),
    ("mode_change", "mode", "A in the parallel mode (major <-> minor)"),
    ("ornament", "elaboration", "A decorated with passing tones and neighbor-note turns"),
    ("reduction", "elaboration", "A with its decorations removed (the inverse of ornament)"),
    ("fragment", "fragmentation", "A's first bar twice, the second time a step higher or lower"),
    ("opening_kept", "restatement", "A's first bar with a new second bar that doesn't end on the tonic"),
    ("ending_kept", "restatement", "a new first bar followed by A's second bar"),
    ("consequent", "function", "A ends away from the tonic; B keeps A's first bar and closes on the tonic"),
    ("unrelated", "none", "a motif from another tune, in the same key and register"),
]
NAMES = [r[0] for r in RELATIONS]
INDEX = {n: i for i, n in enumerate(NAMES)}
# Held out of training entirely; used to test whether the model generalizes to compositions.
COMPOSITIONS = [("seq_up_1", "ornament"), ("inversion", "augmentation"),
                ("retrograde", "octave_up"), ("seq_down_2", "diminution")]


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def canonical_minor(m: Motif) -> Motif:
    """Minor-key spelling by rule: 7^ is raised when it steps up to the tonic, and
    6^ when it steps up to a raised 7^ (melodic minor); otherwise natural minor."""
    if m.mode not in ("minor", "aeolian"):
        return m
    alt = [0] * m.n
    for i in range(m.n - 1, -1, -1):
        d, nxt = m.h[i] % 7, (m.h[i + 1] if i + 1 < m.n else None)
        if d == 6 and nxt == m.h[i] + 1:
            alt[i] = 1
        elif d == 5 and nxt == m.h[i] + 1 and alt[i + 1] == 1:
            alt[i] = 1
    return m.with_(alt=alt)


def diatonic(m: Motif, h: list[int], **kw) -> Motif:
    return canonical_minor(m.with_(h=h, alt=[0] * len(h), **kw))


def shift(m: Motif, k: int) -> Motif:
    return diatonic(m, [x + k for x in m.h])


def bars(m: Motif):
    """Indices of the notes in bar 1 and bar 2, or None if a note crosses the barline."""
    b1 = [i for i in range(m.n) if m.on[i] < m.bar - EPS]
    b2 = [i for i in range(m.n) if m.on[i] >= m.bar - EPS]
    if not b1 or not b2 or any(m.on[i] + m.dur[i] > m.bar + EPS for i in b1) or abs(m.span - 2 * m.bar) > EPS:
        return None
    return b1, b2


def take(m: Motif, idx: list[int], k: int = 0):
    return [m.h[i] + k for i in idx], [m.on[i] for i in idx], [m.dur[i] for i in idx]


def donors(pool: dict, m: Motif, rng: random.Random, n: int | None = None, tries: int = 12):
    """Random motifs from other tunes with the same bar length and span (and note count, if given)."""
    cands = pool.get((m.bar, m.span, n) if n is not None else (m.bar, m.span), [])
    for _ in range(min(tries, len(cands))):
        d = cands[rng.randrange(len(cands))]
        if d.tune() != m.tune():
            yield d


# --------------------------------------------------------------------------
# transforms: each returns B (a Motif) or None
# --------------------------------------------------------------------------
def real(m: Motif, n: int):
    k = round(n * 7 / 12)  # letter-name shift; the alteration makes up the exact interval
    sc, h, alt = SCALES[m.mode], [x + k for x in m.h], []
    for x, s in zip(h, m.semis()):
        a = s + n - (12 * (x // 7) + sc[x % 7])
        if abs(a) > 2:
            return None
        alt.append(a)
    if not any(alt):
        return None  # still in the key: that is a diatonic sequence, not a real transposition
    return m.with_(h=h, alt=alt)


def inversion(m: Motif) -> Motif:
    return diatonic(m, [2 * m.h[0] - x for x in m.h])


def retrograde(m: Motif) -> Motif:
    idx = list(range(m.n))[::-1]
    return diatonic(m, [m.h[j] for j in idx], on=[m.span - (m.on[j] + m.dur[j]) for j in idx],
                    dur=[m.dur[j] for j in idx])


def scale_time(m: Motif, f: float):
    if f < 1 and min(m.dur) * f < 0.125 - EPS:
        return None
    return m.with_(on=[x * f for x in m.on], dur=[x * f for x in m.dur], span=m.span * f)  # same meter, so same bar


def mode_change(m: Motif):
    if m.mode in ("major", "ionian"):
        alt = []
        for i, x in enumerate(m.h):
            d, nxt = x % 7, (m.h[i + 1] if i + 1 < m.n else None)
            alt.append(-1 if d in (2, 5) else (0 if nxt == x + 1 else -1) if d == 6 else 0)
    elif m.mode in ("minor", "aeolian"):
        alt = [1 if x % 7 in (2, 5, 6) else 0 for x in m.h]
    else:
        return None
    return None if alt == list(m.alt) else m.with_(alt=alt)


def ornament(m: Motif, rng: random.Random):
    h, on, dur, added = [], [], [], 0
    for i in range(m.n):
        x, t, d = m.h[i], m.on[i], m.dur[i]
        nxt = m.h[i + 1] if i + 1 < m.n else None
        legato = i + 1 < m.n and abs(t + d - m.on[i + 1]) < EPS
        if nxt is not None and abs(nxt - x) == 2 and d >= 0.5 - EPS and legato and rng.random() < 0.7:
            h += [x, x + (1 if nxt > x else -1)]
            on += [t, t + d / 2]
            dur += [d / 2, d / 2]
            added += 1
        elif d >= 1.0 - EPS and rng.random() < 0.5:
            q = 0.25
            h += [x, x + 1, x]
            on += [t, t + d - 2 * q, t + d - q]
            dur += [d - 2 * q, q, q]
            added += 1
        else:
            h.append(x)
            on.append(t)
            dur.append(d)
    return diatonic(m, h, on=on, dur=dur) if added else None


def fragment(m: Motif, rng: random.Random):
    b = bars(m)
    if b is None or len(b[0]) < 2:
        return None
    h1, on1, d1 = take(m, b[0])
    s = rng.choice((-1, 1))
    return diatonic(m, h1 + [x + s for x in h1], on=on1 + [t + m.bar for t in on1], dur=d1 + d1)


def opening_kept(m: Motif, rng: random.Random, pool: dict, close: bool = False):
    b = bars(m)
    if b is None or (close and m.h[-1] % 7 == 0):
        return None
    h1, on1, d1 = take(m, b[0])
    for d in donors(pool, m, rng):
        bd = bars(d)
        if bd is None:
            continue
        hx, onx, dx = take(d, bd[1])
        if close:  # land the new ending on the tonic nearest A's last note
            k = 7 * round(m.h[-1] / 7) - hx[-1]
        else:
            k = h1[-1] - hx[0] + rng.choice((-2, -1, 1, 2))
        B = diatonic(m, h1 + [x + k for x in hx], on=on1 + onx, dur=d1 + dx)
        if B.signature() == m.signature() or [x + k for x in hx] == take(m, b[1])[0]:
            continue
        if close != (B.h[-1] % 7 == 0):
            continue
        return B
    return None


def ending_kept(m: Motif, rng: random.Random, pool: dict):
    b = bars(m)
    if b is None:
        return None
    h2, on2, d2 = take(m, b[1])
    for d in donors(pool, m, rng):
        bd = bars(d)
        if bd is None:
            continue
        hx, onx, dx = take(d, bd[0])
        k = h2[0] - hx[-1] + rng.choice((-2, -1, 1, 2))
        if [x + k for x in hx] == take(m, b[0])[0]:
            continue
        return diatonic(m, [x + k for x in hx] + h2, on=onx + on2, dur=dx + d2)
    return None


def rhythm_new(m: Motif, rng: random.Random, pool: dict):
    for d in donors(pool, m, rng, n=m.n):
        if [round(x, 4) for x in d.on] != [round(x, 4) for x in m.on]:
            return m.with_(on=list(d.on), dur=list(d.dur))
    return None


def pitch_new(m: Motif, rng: random.Random, pool: dict):
    steps = [b - a for a, b in zip(m.h, m.h[1:])]
    for d in donors(pool, m, rng, n=m.n):
        if [b - a for a, b in zip(d.h, d.h[1:])] != steps:
            return diatonic(m, [x - d.h[0] + m.h[0] for x in d.h])
    return None


def unrelated(m: Motif, rng: random.Random, pool: dict):
    steps = [b - a for a, b in zip(m.h, m.h[1:])]
    for d in donors(pool, m, rng):
        if [b - a for a, b in zip(d.h, d.h[1:])] == steps or d.on == m.on:
            continue
        k = round(sum(m.h) / m.n - sum(d.h) / d.n)
        return diatonic(m, [x + k for x in d.h], on=list(d.on), dur=list(d.dur))
    return None


# --------------------------------------------------------------------------
def make(name: str, A: Motif, rng: random.Random, pool: dict):
    """One labeled pair (A, B, params) for relation `name`, or None."""
    A = canonical_minor(A)
    p: dict = {}
    if name == "repeat":
        B = A.with_()
    elif name in ("octave_up", "octave_down"):
        B = shift(A, 7 if name == "octave_up" else -7)
    elif name.startswith("seq_"):
        k = int(name[-1]) * (1 if "_up_" in name else -1)
        B = shift(A, k)
    elif name in ("real_up", "real_down"):
        p["semitones"] = n = rng.randint(1, 5) * (1 if name == "real_up" else -1)
        B = real(A, n)
    elif name == "inversion":
        B = inversion(A)
    elif name == "retrograde":
        B = retrograde(A)
    elif name == "retro_inversion":
        B = retrograde(inversion(A))
    elif name in ("augmentation", "diminution"):
        B = scale_time(A, 2.0 if name == "augmentation" else 0.5)
    elif name == "rhythm_new":
        B = rhythm_new(A, rng, pool)
    elif name == "pitch_new":
        B = pitch_new(A, rng, pool)
    elif name == "mode_change":
        B = mode_change(A)
    elif name == "ornament":
        B = ornament(A, rng)
    elif name == "reduction":
        orn = ornament(A, rng)
        return None if orn is None else (orn, A, p)
    elif name == "fragment":
        B = fragment(A, rng)
    elif name == "opening_kept":
        B = opening_kept(A, rng, pool)
    elif name == "consequent":
        B = opening_kept(A, rng, pool, close=True)
    elif name == "ending_kept":
        B = ending_kept(A, rng, pool)
    elif name == "unrelated":
        B = unrelated(A, rng, pool)
    else:
        raise KeyError(name)
    if B is None or (name != "repeat" and B.signature() == A.signature()):
        return None
    return A, B, p


def compose(names: tuple[str, str], A: Motif, rng: random.Random, pool: dict):
    """B = second(first(A)), for the held-out composition test."""
    first = make(names[0], A, rng, pool)
    if first is None:
        return None
    second = make(names[1], first[1], rng, pool)
    if second is None or second[1].signature() == A.signature():
        return None
    return first[0], second[1], {}


def donor_pool(motifs: list[Motif]) -> dict:
    """Index motifs by (bar, span) and by (bar, span, note count), for donor lookups."""
    pool: dict = {}
    for m in motifs:
        pool.setdefault((m.bar, m.span), []).append(m)
        pool.setdefault((m.bar, m.span, m.n), []).append(m)
    return pool
