"""Build the musiPAM v2 stimulus set end to end.

    ~/.venvs/musipam/bin/python build.py [--out ../stimuli] [--scratch DIR] [--no-audio]
                                         [--renderer muse|fluidsynth]

Writes, per stimulus: MusicXML (open in MuseScore), full MIDI, WAV master,
MP3, and the motif graph (JSON). Then the manifest, a note-event table, the
validation report, the renderer record and the design check. Audio comes from
Muse Sounds through MuseScore 4 by default; --renderer fluidsynth uses the
original free renderer (FluidSynth + MS Basic). See musipam_stim/render.py.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # keep __pycache__ out of Google Drive

import argparse
import csv
import hashlib
import json
import re
import tempfile
from pathlib import Path

from musipam_stim import designcheck as dc
from musipam_stim import render
from musipam_stim.arrange import INSTRUMENTS, build_score, realize_accompaniment
from musipam_stim.graphs import graph_json, stim_graph
from musipam_stim.render import LEAD_IN_S, TAIL_S
from musipam_stim.themes import (CROSS_MAPPINGS, THEMES, analog_pairs,
                                 theme_stim)
from musipam_stim.transforms import CELL, DESCRIPTION, TRANSFORMS, flat_notes
from musipam_stim.validate import (check_alignment, check_audio,
                                   check_designed_relations, check_stim)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent / "stimuli"))
    ap.add_argument("--scratch", default=None)
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--renderer", choices=("muse", "fluidsynth"), default="muse")
    args = ap.parse_args()
    out = Path(args.out)
    scratch = Path(args.scratch or tempfile.mkdtemp(prefix="musipam_"))
    scratch.mkdir(parents=True, exist_ok=True)
    (out / "reports").mkdir(parents=True, exist_ok=True)
    if not args.no_audio:
        info = renderer_info(args.renderer, scratch)
        (out / "reports" / "renderer.json").write_text(json.dumps(info, indent=1) + "\n")

    idents = {tid: theme_stim(tid) for tid in THEMES}
    checks = check_designed_relations(idents)
    graphs, manifest, events, pending = {}, [], [], []

    for tid, ident in idents.items():
        tdir = out / tid
        tdir.mkdir(parents=True, exist_ok=True)
        for cond, fn in TRANSFORMS.items():
            s = fn(ident)
            sid = s.stim_id
            checks += check_stim(s, ident)

            score = build_score(s)
            xml = tdir / f"{sid}.musicxml"
            score.write("musicxml", fp=str(xml))
            _drop_encoding_date(xml)
            score.write("midi", fp=str(tdir / f"{sid}.mid"))

            g = stim_graph(s)
            graphs[(tid, cond)] = g
            (tdir / f"{sid}.graph.json").write_text(json.dumps(graph_json(s, g), indent=1))

            music_s = s.total_ql * 60.0 / s.bpm
            row = {
                "stim_id": sid, "theme": tid, "theme_title": THEMES[tid].title, "condition": cond,
                "cell": CELL[cond], "description": DESCRIPTION[cond],
                "key": f"{s.k.tonic.name} {s.k.mode}", "meter": s.meter, "bpm": s.bpm,
                "bars": round(s.total_ql / s.bar_ql), "music_s": round(music_s, 3),
                "melody_instrument": INSTRUMENTS[s.melody_inst][1],
                "accomp_instrument": INSTRUMENTS[s.accomp_inst][1],
                "motif_order": " ".join(seg.label for seg in s.segments),
                "motif_onsets_s": " ".join(f"{n['onset_ql'] * 60.0 / s.bpm + LEAD_IN_S:.3f}" for n in g["nodes"]),
                "n_melody_notes": len(flat_notes(s)),
                "musicxml": f"{tid}/{sid}.musicxml", "midi": f"{tid}/{sid}.mid",
                "graph": f"{tid}/{sid}.graph.json",
            }
            manifest.append(row)
            pending.append((row, s, tdir))

            t = 0.0
            for seg_pos, seg in enumerate(s.segments):
                for n in seg.notes:
                    events.append({"stim_id": sid, "part": "melody", "motif": seg.label, "motif_pos": seg_pos,
                                   "onset_ql": t, "dur_ql": n.dur,
                                   "onset_s": round(t * 60.0 / s.bpm + LEAD_IN_S, 4),
                                   "dur_s": round(n.dur * 60.0 / s.bpm, 4),
                                   "pitch": n.p.nameWithOctave, "midi": n.p.midi, "ornamental": n.kind or ""})
                    t += n.dur
        print(f"  built {tid} (symbolic)", flush=True)

    if not args.no_audio:
        done = render_stims([(s, tdir) for _, s, tdir in pending], scratch, args.renderer)
        for row, s, _ in pending:
            r = done[s.stim_id]
            checks += r["checks"]
            row.update({k: v for k, v in r.items() if k != "checks"})
            row.update({"wav": f"{s.theme_id}/{s.stim_id}.wav", "mp3": f"{s.theme_id}/{s.stim_id}.mp3"})
            for k in ("wav", "mp3", "duration_s", "lufs", "peak_dbfs", "wav_sha256"):  # keep the old column order
                row[k] = row.pop(k)
    _write_csv(out / "manifest.csv", manifest)
    _write_csv(out / "note_events.csv", events)
    _design_check(graphs, out / "reports")
    _validation_report(checks, out / "reports" / "validation_report.md")
    errors = [c for c in checks if not c.ok and c.severity == "error"]
    print(f"{len(manifest)} stimuli, {len(checks)} checks, {len(errors)} errors")
    for c in errors:
        print(f"  FAIL {c.stim_id} {c.name}: {c.detail}")
    return 1 if errors else 0


def renderer_info(renderer: str, scratch: Path) -> dict:
    """Check the renderer against its pinned version and describe it (reports/renderer.json)."""
    mix = {"stems": "melody, accompaniment", "melody_over_accompaniment_LU": render.MELODY_OVER_ACCOMP_LU,
           "target_LUFS": render.TARGET_LUFS, "peak_ceiling_dBFS": render.PEAK_CEILING_DBFS,
           "lead_in_s": LEAD_IN_S, "tail_s": TAIL_S, "fade_s": render.FADE_S, "sample_rate": render.SR,
           "wav": "16-bit PCM", "mp3": "LAME 192 kb/s"}
    if renderer == "muse":
        fp = render.check_muse(scratch / "muse_check")
        print(f"renderer: Muse Sounds via {fp['musescore'].split(';')[1].strip()}, MuseSampler "
              f"{fp['musesampler_version']}; reference render matches the pinned hash"
              + ("" if not fp["differs_from_pinned"] else f" -- NOT PINNED: {fp['differs_from_pinned']}"), flush=True)
        return {"renderer": "muse", "label": SOUND_LABEL["muse"], **fp, "mix": mix,
                "instrument_settings": "stimgen/musipam_stim/muse_sounds.json"}
    digest = render.check_soundfont()
    print(f"renderer: FluidSynth + MS Basic (sha256 {digest[:16]}... ok)", flush=True)
    return {"renderer": "fluidsynth", "label": SOUND_LABEL["fluidsynth"], "soundfont_sha256": digest, "mix": mix}


SOUND_LABEL = {"muse": "Muse Sounds (MuseScore 4)", "fluidsynth": "FluidSynth + MS Basic"}


def sound(renderer: str, inst: str) -> str:
    return render.MUSE_SOUNDS["instruments"][inst]["label"] if renderer == "muse" else f"MS Basic {INSTRUMENTS[inst][1]}"


def stem_onsets(s) -> dict[str, list[float]]:
    """Score onsets (s from the music's start) of the melody's notes and of the accompaniment's."""
    to_s = 60.0 / s.bpm
    mel, t = [], 0.0
    for seg in s.segments:
        for n in seg.notes:
            if n.p is not None:
                mel.append(t * to_s)
            t += n.dur
    bass, upper = realize_accompaniment(s)
    return {"melody": mel, "accomp": sorted({round(e[0] * to_s, 6) for e in bass + upper})}


def render_stims(items: list, scratch: Path, renderer: str, batch: int = 22) -> dict:
    """Render [(Stim, out_dir)]: two stems each, then mix, master, MP3 and audio checks.

    Returns {stim_id: manifest fields + "checks"}. Muse Sounds stems render in batches
    (one MuseScore process per batch); FluidSynth renders one stem at a time.
    """
    import time
    stems = []
    for s, _ in items:
        for part, inst in (("melody", s.melody_inst), ("accomp", s.accomp_inst)):
            base = scratch / f"{s.stim_id}_{part[:3]}"
            sc = build_score(s, parts=(part,), annotate=False)
            src = Path(f"{base}.musicxml" if renderer == "muse" else f"{base}.mid")
            sc.write("musicxml" if renderer == "muse" else "midi", fp=str(src))
            stems.append((src, inst, Path(f"{base}.wav")))
    t0 = time.time()
    if renderer == "muse":
        for i in range(0, len(stems), batch):
            render.muse_render(stems[i:i + batch], scratch / "muse")
            print(f"  rendered {min(i + batch, len(stems))}/{len(stems)} stems ({time.time() - t0:.0f} s)", flush=True)
    else:
        for src, _, wav in stems:
            render.fluidsynth(src, wav)
    out = {}
    for s, odir in items:
        sid, music_s = s.stim_id, s.total_ql * 60.0 / s.bpm
        mel_wav, acc_wav = scratch / f"{sid}_mel.wav", scratch / f"{sid}_acc.wav"
        wav, mp3 = odir / f"{sid}.wav", odir / f"{sid}.mp3"
        st = render.mix_master(mel_wav, acc_wav, music_s, wav, mp3)
        checks = check_audio(sid, st, LEAD_IN_S + music_s + TAIL_S)
        on = stem_onsets(s)
        fields = {"renderer": SOUND_LABEL[renderer], "melody_sound": sound(renderer, s.melody_inst),
                  "accomp_sound": sound(renderer, s.accomp_inst)}
        for part, stem in (("melody", mel_wav), ("accomp", acc_wav)):
            off, n = render.onset_offset(stem, on[part])
            checks.append(check_alignment(sid, part, off, n, strict=renderer == "muse"))
            fields[f"{part}_onset_offset_ms"] = round(off * 1000)
        fields.update({"duration_s": round(st.duration_s, 3), "lufs": round(st.lufs, 2),
                       "peak_dbfs": round(st.peak_dbfs, 2), "wav_sha256": sha256(wav), "checks": checks})
        out[sid] = fields
    return out


def _drop_encoding_date(path: Path) -> None:
    """music21 stamps today's date into every MusicXML file; drop it so rebuilds are byte-identical."""
    path.write_text(re.sub(r"\s*<encoding-date>[^<]*</encoding-date>", "", path.read_text()))


def _write_csv(path: Path, rows: list[dict]) -> None:
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def _validation_report(checks, path: Path) -> None:
    lines = ["# Validation report", "",
             "Objective checks only. Musical quality, naturalness and unfamiliarity are *not* certified here; "
             "they require listener pilots.", ""]
    n_err = sum(1 for c in checks if not c.ok and c.severity == "error")
    lines += [f"**{len(checks)} checks, {n_err} errors.**", "",
              "| stimulus | check | result | detail |", "|---|---|---|---|"]
    for c in checks:
        res = "pass" if c.ok else ("**FAIL**" if c.severity == "error" else "note")
        lines.append(f"| {c.stim_id} | {c.name} | {res} | {c.detail} |")
    path.write_text("\n".join(lines) + "\n")


def _design_check(graphs: dict, rdir: Path) -> None:
    norm = dc.relation_norm(graphs.values())
    W = dc.W_LEVELS
    hdr = "| condition | grid cell | " + " | ".join(f"w={w:g}" for w in W) + " |"
    sep = "|---|---|" + "---|" * len(W)
    L = ["# Design check: object vs. relational matching", "",
         "Exact brute-force graph matching (24 permutations of 4 motifs) — a proxy, **not PAM**. "
         "Score = (1-w)·node similarity + w·relation similarity; w=0 is object-only, w=1 relation-only. "
         "Relation vectors are standardized per dimension over the whole stimulus set.", "",
         "Cell entries: **✓** = the theme's motifs map onto their own transformed selves "
         "(T2's identical a1/a2 count as one class); **✗** = they do not. "
         "The label is where the theme's first motif *a* landed.", ""]
    out_json = {}
    for code, code_name in (("rel", "key/tempo-relative node code"), ("abs", "absolute (piano-roll) node code")):
        L += [f"## Theme → variation, {code_name}", ""]
        for tid in THEMES:
            base = graphs[(tid, "identity")]
            L += [f"**{tid}**", "", hdr, sep]
            for cond in TRANSFORMS:
                if cond in ("identity", "timbre", "tempo"):
                    continue
                gB = graphs[(tid, cond)]
                r = dc.evaluate(base, gB, dc.truth_by_source(base, gB), code, norm)
                cells = " | ".join(("✓ " if r["rows"][w]["class_ok"] else "✗ ") + r["rows"][w]["a_maps_to"] for w in W)
                L.append(f"| {cond} | {CELL[cond]} | {cells} |")
                out_json[f"{code}|{tid}|{cond}"] = {str(w): {"perm": r["rows"][w]["perm"], "ok": r["rows"][w]["class_ok"]}
                                                    for w in W}
            L.append("")
    ident = {tid: graphs[(tid, "identity")] for tid in THEMES}
    L += ["## Cross-mappings (truth = relational roles)", "",
          "Each row is a designed look-alike pair. The label shows where the source motif whose shape the "
          "target copies landed in the target theme.", "", hdr.replace("condition", "pair"), sep]
    for src, si, dst, di in CROSS_MAPPINGS:
        for code in ("rel", "abs"):
            r = dc.evaluate(ident[src], ident[dst], (0, 1, 2, 3), code, norm)
            lb = r["labels_B"]
            cells = " | ".join(("✓ " if r["rows"][w]["class_ok"] else "✗ ") + lb[r["rows"][w]["perm"][si]] for w in W)
            L.append(f"| {src} → {dst} [{code}] | {r['labels_A'][si]} → ? (look-alike: {lb[di]}) | {cells} |")
            out_json[f"cross|{code}|{src}>{dst}"] = {str(w): {"perm": r["rows"][w]["perm"], "ok": r["rows"][w]["class_ok"]}
                                                     for w in W}

    analogs = set(analog_pairs())
    tids = list(THEMES)
    rows = []
    for i, a in enumerate(tids):
        for b in tids[i + 1:]:
            m = dc.match(ident[a], ident[b], "rel", norm)
            best_p = max(m["scores"], key=lambda p: m["scores"][p][1])
            rows.append({"a": a, "b": b, "analog": (a, b) in analogs, "skeleton": THEMES[a].skeleton,
                         "role": m["scores"][(0, 1, 2, 3)][1], "best": m["scores"][best_p][1],
                         "role_is_best": best_p == (0, 1, 2, 3)})
    out_json["relsim"] = rows
    an = [r for r in rows if r["analog"]]
    ct = [r for r in rows if not r["analog"]]
    auc = sum((x["role"] > y["role"]) + 0.5 * (x["role"] == y["role"]) for x in an for y in ct) / (len(an) * len(ct))
    mean = lambda xs: sum(xs) / len(xs)
    L += ["", "## Relational similarity between themes", "",
          "Mean standardized relation similarity (w = 1). *Role* aligns motifs by position; *best* is the maximum "
          "over all 24 alignments. Designed analogs (same skeleton) should be more similar than pairs with "
          "different skeletons, and best aligned by role.", "",
          f"- **Designed analogs ({len(an)} pairs):** mean role similarity {mean([r['role'] for r in an]):.2f}; "
          f"best alignment is the role alignment in {sum(r['role_is_best'] for r in an)}/{len(an)}.",
          f"- **Different skeletons ({len(ct)} pairs):** mean role similarity {mean([r['role'] for r in ct]):.2f} "
          f"(max {max(r['role'] for r in ct):.2f}).",
          f"- **Separation:** a random analog pair beats a random control pair {auc:.0%} of the time (AUC).", "",
          "| analog pair | skeleton | role | best | best is role |", "|---|---|---|---|---|"]
    for r in an:
        L.append(f"| {r['a']} → {r['b']} | {r['skeleton']} | {r['role']:.2f} | {r['best']:.2f} | "
                 f"{'yes' if r['role_is_best'] else 'no'} |")
    raw13 = dc.evaluate(ident["T1"], ident["T3"], (0, 1, 2, 3), "rel")["truth_edge"]
    raw12 = dc.evaluate(ident["T1"], ident["T2"], (0, 1, 2, 3), "rel")["truth_edge"]
    L += ["", f"Without standardization the relational similarity of the role mapping is {raw13:.2f} (T1→T3) vs "
              f"{raw12:.2f} (T1→T2): positional relations, identical for any two 4-motif passages, swamp the "
              "derivational ones. Standardization is therefore required, and the real PAM implementation will "
              "need an equivalent normalization of musical relation vectors."]
    (rdir / "design_check.md").write_text("\n".join(L) + "\n")
    (rdir / "design_check.json").write_text(json.dumps(out_json, indent=1))


if __name__ == "__main__":
    raise SystemExit(main())
