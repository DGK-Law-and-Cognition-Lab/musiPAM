"""Deterministic audio rendering.

Each stimulus is rendered as two stems (melody, accompaniment). The stems are mixed with the
melody a fixed number of LU above the accompaniment, so the melody/accompaniment balance is
identical across conditions, and the mix is loudness-normalized, so overall level is identical
too. Two renderers, each pinned so that a software update can neither break the build nor
silently change the audio:

- ``muse`` (the default since 2026-11-09): MuseScore 4's command line with Muse Sounds sample
  libraries (free through Muse Hub). Each stem's MusicXML is converted to a MuseScore file, its
  part is given the Muse Sounds instrument listed in ``muse_sounds.json``, and MuseScore exports
  the audio. One MuseScore process converts a batch of stems and another renders it. Before
  rendering, ``check_muse`` compares MuseScore, MuseSampler and the four instrument libraries
  with the pinned fingerprints and renders a fixed reference score, whose audio must match the
  pinned hash bit for bit.
- ``fluidsynth``: FluidSynth with MuseScore's MS Basic soundfont, the original renderer, kept so
  that anyone can rebuild the set with free software alone.

A renderer change affects every stimulus equally. The released audio files, whose hashes are in
manifest.csv, are the canonical stimuli.
"""
from __future__ import annotations

import copy
import ctypes
import hashlib
import json
import os
import re
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

HERE = Path(__file__).resolve().parent
ALLOW_CHANGE = "MUSIPAM_ALLOW_RENDERER_CHANGE" in os.environ

# ---------------------------------------------------------------- FluidSynth + MS Basic
# Pinned copy, so a MuseScore/Muse Hub update can neither break the build nor
# silently change the audio. Restore it from any MuseScore 4 app bundle
# (Contents/Resources/sound/MS Basic.sf3); the hash check catches a different file.
SOUNDFONT = Path(os.environ.get("MUSIPAM_SOUNDFONT", Path.home() / ".venvs/musipam/soundfonts/MS Basic.sf3"))
SOUNDFONT_SHA256 = "5ea2375e8bd7d8e71def1036978c1621e85b66934169b6a2744b27b9b3c2d99c"

# ---------------------------------------------------------------- MuseScore 4 + Muse Sounds
MSCORE = Path(os.environ.get("MUSIPAM_MSCORE", "/Applications/MuseScore 4.app/Contents/MacOS/mscore"))
MUSE_INSTRUMENTS = Path(os.environ.get(
    "MUSIPAM_MUSE_INSTRUMENTS", Path.home() / "Library/Application Support/Muse Hub/Downloads/Instruments"))
MUSESAMPLER = Path(os.environ.get(
    "MUSIPAM_MUSESAMPLER", Path.home() / "Library/Application Support/MuseSampler/lib/libMuseSamplerCoreLib.dylib"))
MUSE_SOUNDS = json.loads((HERE / "muse_sounds.json").read_text())
MUSE_REFERENCE = HERE / "muse_reference.musicxml"  # one bar per instrument: clarinet, violin, piano, harp

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


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


# ---------------------------------------------------------------- FluidSynth
def check_soundfont() -> str:
    if not SOUNDFONT.exists():
        raise FileNotFoundError(f"soundfont missing: {SOUNDFONT} (copy MS Basic.sf3 from the MuseScore 4 app bundle)")
    digest = _sha256(SOUNDFONT)
    if digest != SOUNDFONT_SHA256 and "MUSIPAM_SOUNDFONT" not in os.environ:
        raise ValueError(f"{SOUNDFONT} has hash {digest[:12]}..., not the pinned {SOUNDFONT_SHA256[:12]}...; "
                         "audio would differ from the recorded stimuli. Set MUSIPAM_SOUNDFONT to use it deliberately.")
    return digest


def fluidsynth(mid: Path, wav: Path) -> None:
    # dynamic sample loading: ~4.6x faster with the compressed .sf3, bit-identical output
    cmd = ["fluidsynth", "-ni", "-q", "-F", str(wav), "-r", str(SR), "-g", "0.5",
           "-o", "audio.file.format=float", "-o", "synth.dynamic-sample-loading=1",
           str(SOUNDFONT), str(mid)]
    subprocess.run(cmd, check=True, capture_output=True)


# ---------------------------------------------------------------- Muse Sounds
def muse_fingerprint() -> dict:
    """What the Muse Sounds route would render with: versions and library file fingerprints."""
    if not MSCORE.exists():
        raise FileNotFoundError(f"MuseScore 4 not found at {MSCORE}. Install it and the Muse Sounds instruments "
                                "through Muse Hub, set MUSIPAM_MSCORE, or build with --renderer fluidsynth.")
    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "version.txt"
        _mscore(["--long-version"], log, 120)
        out = log.read_text()
    version = [line.strip() for line in out.splitlines() if "; Version " in line]
    fp = {"musescore": version[-1] if version else out.strip(), "musesampler_version": None,
          "musesampler_sha256": _sha256(MUSESAMPLER) if MUSESAMPLER.exists() else None, "instruments": {}}
    try:  # the version string needs no initialization of the sampler
        lib = ctypes.CDLL(str(MUSESAMPLER))
        lib.ms_get_version_string.restype = ctypes.c_char_p
        fp["musesampler_version"] = lib.ms_get_version_string().decode()
    except (OSError, AttributeError):
        pass
    for name, inst in MUSE_SOUNDS["instruments"].items():
        stem = MUSE_INSTRUMENTS / inst["files"]
        spx, sts = Path(f"{stem}.spx"), stem.parent / "SFZ" / f"{stem.name}.sts"
        fp["instruments"][name] = {"label": inst["label"], "muse_uid": inst["muse_uid"],
                                   "spx_sha256": _sha256(spx) if spx.exists() else None,
                                   "sts_bytes": sts.stat().st_size if sts.exists() else None}
    return fp


def check_muse(workdir: Path) -> dict:
    """Refuse to render unless the Muse Sounds route matches the pinned one (see the module docstring)."""
    fp = muse_fingerprint()
    pin = MUSE_SOUNDS["pinned"]
    diffs = [f"{k}: {fp[k]} (pinned {pin[k]})" for k in ("musescore", "musesampler_sha256") if fp[k] != pin[k]]
    for name, inst in MUSE_SOUNDS["instruments"].items():
        got = fp["instruments"][name]
        if got["spx_sha256"] is None:
            raise FileNotFoundError(f"Muse Sounds instrument missing: {inst['label']} (install it through Muse Hub)")
        diffs += [f"{name} {k}: {got[k]} (pinned {inst['pinned'][k]})"
                  for k in ("spx_sha256", "sts_bytes") if got[k] != inst["pinned"][k]]
    workdir.mkdir(parents=True, exist_ok=True)
    ref = workdir / "muse_reference.wav"
    muse_render([(MUSE_REFERENCE, ["clarinet", "violin", "piano", "harp"], ref)], workdir)
    fp["reference_wav_sha256"] = _sha256(ref)
    if fp["reference_wav_sha256"] != pin["reference_wav_sha256"]:
        diffs.append(f"reference render {fp['reference_wav_sha256'][:12]}... (pinned {pin['reference_wav_sha256'][:12]}...)")
    x = _load(ref).mean(1)
    bar = int(round(4 * 60 / 100 * SR))  # 4/4 at 100 bpm
    for i, name in enumerate(["clarinet", "violin", "piano", "harp"]):
        if np.sqrt(np.mean(x[i * bar:(i + 1) * bar] ** 2)) < 1e-4:
            raise RuntimeError(f"Muse Sounds reference render: the {name} bar is silent")
    if diffs and not ALLOW_CHANGE:
        raise ValueError("The Muse Sounds renderer differs from the pinned one, so the audio would differ from the "
                         "recorded stimuli:\n  " + "\n  ".join(diffs) + "\nSet MUSIPAM_ALLOW_RENDERER_CHANGE=1 to render "
                         "with it deliberately, then update 'pinned' in musipam_stim/muse_sounds.json.")
    fp["differs_from_pinned"] = diffs
    return fp


def _mscore(args: list[str], log: Path, timeout: float) -> None:
    """Run MuseScore's command line with its output in a log file.

    Not a pipe: MuseScore starts a crash handler that inherits the output handles and can
    outlive MuseScore, and a pipe held open by it would stall the build.
    """
    with open(log, "a") as f:
        subprocess.run([str(MSCORE), *args], stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                       timeout=timeout)


def _mscore_job(jobs: list[dict], job_file: Path) -> None:
    """Run a MuseScore batch job; retry any file the batch did not produce on its own."""
    for j in jobs:
        Path(j["out"]).unlink(missing_ok=True)
    job_file.write_text(json.dumps(jobs, indent=1))
    log = job_file.with_suffix(".log")
    timeout = 600 + 60 * len(jobs)  # the first launch after a Muse Hub update can spend minutes initializing
    _mscore(["-j", str(job_file)], log, timeout)
    for j in jobs:
        if not Path(j["out"]).exists():
            _mscore(["-o", j["out"], j["in"]], log, 600)
            if not Path(j["out"]).exists():
                raise RuntimeError(f"MuseScore could not convert {j['in']} -> {j['out']} (log: {log})")


def _assign_sounds(raw: Path, instruments: str | list[str], out: Path) -> None:
    """Copy a MuseScore file, giving its parts the Muse Sounds instruments (one name for all parts, or one per part)."""
    with zipfile.ZipFile(raw) as z:
        mscx = next(n for n in z.namelist() if n.endswith(".mscx"))
        parts = re.findall(r'<Part id="(\d+)">.*?<Instrument id="([^"]+)"', z.read(mscx).decode(), flags=re.S)
        names = [instruments] * len(parts) if isinstance(instruments, str) else list(instruments)
        if not parts or len(names) != len(parts):
            raise ValueError(f"{raw}: {len(parts)} parts for instruments {names}")
        a = json.loads(z.read("audiosettings.json"))
        a["tracks"] = [{**copy.deepcopy(MUSE_SOUNDS["instruments"][nm]["track"]), "partId": pid, "instrumentId": iid}
                       for (pid, iid), nm in zip(parts, names)]
        a["aux"], a["master"] = copy.deepcopy(MUSE_SOUNDS["aux"]), copy.deepcopy(MUSE_SOUNDS["master"])
        a["activeSoundProfile"] = "MuseSounds"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zo:
            for item in z.infolist():
                data = json.dumps(a, indent=1).encode() if item.filename == "audiosettings.json" else z.read(item.filename)
                zo.writestr(item, data)


def muse_render(stems: list[tuple[Path, str | list[str], Path]], workdir: Path) -> None:
    """Render [(musicxml, instrument(s), wav)] with Muse Sounds."""
    workdir.mkdir(parents=True, exist_ok=True)
    raw = [workdir / f"{x.stem}_raw.mscz" for x, _, _ in stems]
    _mscore_job([{"in": str(x), "out": str(r)} for (x, _, _), r in zip(stems, raw)], workdir / "convert.json")
    scores = []
    for (x, inst, _), r in zip(stems, raw):
        scores.append(workdir / f"{x.stem}.mscz")
        _assign_sounds(r, inst, scores[-1])
    _mscore_job([{"in": str(m), "out": str(w)} for m, (_, _, w) in zip(scores, stems)], workdir / "render.json")


# ---------------------------------------------------------------- mixing, checks
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


def onset_offset(wav: Path, onsets_s: list[float]) -> tuple[float, int]:
    """Median offset (s) of a stem's note onsets from the score's, and how many onsets were measured.

    For each onset in the score, the audio's onset is the spectral-flux peak between 30 ms before
    and 120 ms after it (1-ms frames). A renderer that shifts, drops or stretches notes moves the median.
    """
    x = _load(wav).mean(1)
    n, hop, pad = 1024, SR // 1000, 1024 + SR // 10
    x = np.concatenate([np.zeros(pad), x, np.zeros(n)])
    win = np.hanning(n)
    offs = []
    for e in onsets_s:
        centres = np.arange(e - 0.031, e + 0.12, hop / SR)
        starts = np.round(centres * SR).astype(int) + pad - n // 2
        if starts[0] < 0 or starts[-1] + n > len(x):
            continue
        spec = np.log1p(1000 * np.abs(np.fft.rfft(np.stack([x[s:s + n] for s in starts]) * win, axis=1)))
        flux = np.maximum(np.diff(spec, axis=0), 0).sum(1)
        offs.append(centres[1:][int(np.argmax(flux))] - e)
    return (float(np.median(offs)) if offs else float("nan")), len(offs)
