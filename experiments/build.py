"""Build a deployable experiment folder: shared code + one study + its stimuli.

    ~/.venvs/musipam/bin/python build.py study0            # -> dist/study0/

The output folder is what goes into the study's Pavlovia project (a GitLab repository):
copy it over the repository's contents and push. Every study is built from the same
shared code, so consent, screening and questionnaires stay identical across studies.

Stimuli come from the musiPAM stimulus set: ../stimuli/manifest.csv (the themes) and
../stimuli/anchors/manifest.csv (well-known anchor melodies and the practice melody;
built by stimgen/build_anchors.py). Study settings (SONA credit URL, Prolific codes,
contact email) come from <study>/config.local.js, which is gitignored; without it the
build uses shared/config.template.js and the experiment never redirects.

jsPsych, its plugins and the Pavlovia plugin (all MIT-licensed) are served from the
experiment's own lib/ folder rather than a CDN, so a slow or failing CDN cannot stall a
session. shared/libs.json pins each file's URL and SHA-256; build.py downloads missing
files into vendor/ (a gitignored cache) and refuses any file whose hash differs.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
import urllib.request
from pathlib import Path

sys.dont_write_bytecode = True  # keep __pycache__ out of Google Drive

HERE = Path(__file__).resolve().parent
V2 = HERE.parent
STIM = V2 / "stimuli"
VENDOR = HERE / "vendor"
sys.path.insert(0, str(HERE / "shared"))
from make_headphone_stimuli import make as make_headphone  # noqa: E402

LEAD_IN_S = 0.1  # stimgen/musipam_stim/render.py: silence before the music


def vendor_libs(dst: Path) -> int:
    """Copy the pinned jsPsych files into dst, downloading any that are not cached yet."""
    VENDOR.mkdir(exist_ok=True)
    dst.mkdir(parents=True, exist_ok=True)
    libs = json.loads((HERE / "shared" / "libs.json").read_text())
    for lib in libs:
        cached = VENDOR / lib["file"]
        if not cached.exists():
            req = urllib.request.Request(lib["url"], headers={"User-Agent": "musipam-build"})
            cached.write_bytes(urllib.request.urlopen(req, timeout=60).read())
        digest = hashlib.sha256(cached.read_bytes()).hexdigest()
        if digest != lib["sha256"]:
            raise SystemExit(f"{lib['file']}: SHA-256 {digest[:12]}... is not the pinned {lib['sha256'][:12]}...; "
                             f"delete {cached} and rebuild, or update shared/libs.json deliberately")
        shutil.copy(cached, dst / lib["file"])
    return len(libs)


def theme_items() -> list[dict]:
    items = []
    for r in csv.DictReader(open(STIM / "manifest.csv")):
        if r["condition"] != "identity":
            continue
        num, den = (int(x) for x in r["meter"].split("/"))
        bar_s = num * 4.0 / den * 60.0 / float(r["bpm"])
        onsets = [float(x) for x in r["motif_onsets_s"].split()]
        items.append({
            "id": r["stim_id"], "kind": "theme", "theme": r["theme"], "source": STIM / r["mp3"],
            "duration": float(r["duration_s"]),
            "boundaries": onsets[1:],  # designed motif boundaries: the onsets of motifs 2-4 (bars 3, 5, 7)
            "barlines": [round(LEAD_IN_S + k * bar_s, 3) for k in range(int(r["bars"]))],
        })
    return items


def anchor_items() -> tuple[list[dict], dict | None]:
    path = STIM / "anchors" / "manifest.csv"
    if not path.exists():
        print("  note: no anchors yet (run stimgen/build_anchors.py); building without anchors or practice melody")
        return [], None
    anchors, practice = [], None
    for r in csv.DictReader(open(path)):
        it = {"id": r["id"], "kind": r["kind"], "theme": None, "title": r["title"], "source": path.parent / r["mp3"],
              "duration": float(r["duration_s"]), "boundaries": [float(x) for x in r["boundaries_s"].split()]}
        if r["kind"] == "practice":
            practice = it
        else:
            anchors.append(it)
    return anchors, practice


def stimulus_set_version() -> str:
    h = hashlib.sha256()
    for m in (STIM / "manifest.csv", STIM / "anchors" / "manifest.csv"):
        if m.exists():
            h.update(m.read_bytes())
    return "musiPAM-v2-" + h.hexdigest()[:10]


def build(study: str) -> Path:
    src = HERE / study
    if not (src / "experiment.js").exists():
        raise SystemExit(f"no study folder {src}")
    out = HERE / "dist" / study
    if out.exists():
        shutil.rmtree(out)
    (out / "audio").mkdir(parents=True)

    n_libs = vendor_libs(out / "lib")
    for f in (HERE / "shared").glob("*.js"):
        if f.name != "config.template.js":
            shutil.copy(f, out / f.name)
    shutil.copy(HERE / "shared" / "musipam.css", out / "musipam.css")
    for f in src.iterdir():
        if f.is_file() and f.name != "config.local.js" and not f.name.startswith("."):
            shutil.copy(f, out / f.name)
    config = src / "config.local.js"
    if config.exists():
        shutil.copy(config, out / "config.js")
    else:
        shutil.copy(HERE / "shared" / "config.template.js", out / "config.js")
        print(f"  note: no {study}/config.local.js; using placeholders (no SONA/Prolific redirect)")

    themes = theme_items()
    anchors, practice = anchor_items()

    def place(it: dict) -> dict:
        dst = out / "audio" / it["source"].name
        shutil.copy(it["source"], dst)
        return {k: v for k, v in it.items() if k != "source"} | {"file": f"audio/{dst.name}"}

    headphone, calibration = make_headphone(out / "hp")
    stimuli = {"version": stimulus_set_version(), "items": [place(it) for it in themes + anchors],
               "practice": place(practice) if practice else None,
               "headphone": headphone, "calibration": calibration}
    (out / "stimuli.json").write_text(json.dumps(stimuli, indent=1, ensure_ascii=False))
    size = sum(f.stat().st_size for f in out.rglob("*") if f.is_file()) / 1e6
    print(f"{study}: {len(themes)} themes, {len(anchors)} anchors, practice: {'yes' if practice else 'no'}; "
          f"{n_libs} pinned libraries; stimulus set {stimuli['version']}; {size:.1f} MB -> {out}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("study", nargs="?", default="study0")
    build(ap.parse_args().study)
