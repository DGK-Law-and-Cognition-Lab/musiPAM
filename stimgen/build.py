"""Build the musiPAM v2 stimulus set end to end.

    ~/.venvs/musipam/bin/python build.py [--out ../stimuli] [--scratch DIR] [--no-audio]

Writes, per stimulus: MusicXML (open in MuseScore), full MIDI, WAV master,
MP3, and the motif graph (JSON). Then the manifest, a note-event table, the
validation report, and the design check.
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
from musipam_stim.arrange import INSTRUMENTS, build_score
from musipam_stim.graphs import graph_json, stim_graph
from musipam_stim.render import (LEAD_IN_S, TAIL_S, check_soundfont,
                                 fluidsynth, mix_master)
from musipam_stim.themes import (CROSS_MAPPINGS, THEMES, analog_pairs,
                                 theme_stim)
from musipam_stim.transforms import CELL, DESCRIPTION, TRANSFORMS, flat_notes
from musipam_stim.validate import (check_audio, check_designed_relations,
                                   check_stim)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent / "stimuli"))
    ap.add_argument("--scratch", default=None)
    ap.add_argument("--no-audio", action="store_true")
    args = ap.parse_args()
    out = Path(args.out)
    scratch = Path(args.scratch or tempfile.mkdtemp(prefix="musipam_"))
    scratch.mkdir(parents=True, exist_ok=True)
    (out / "reports").mkdir(parents=True, exist_ok=True)
    if not args.no_audio:
        print(f"soundfont sha256 {check_soundfont()[:16]}... ok", flush=True)

    idents = {tid: theme_stim(tid) for tid in THEMES}
    checks = check_designed_relations(idents)
    graphs, manifest, events = {}, [], []

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
            if not args.no_audio:
                mel_mid, acc_mid = scratch / f"{sid}_mel.mid", scratch / f"{sid}_acc.mid"
                build_score(s, parts=("melody",), annotate=False).write("midi", fp=str(mel_mid))
                build_score(s, parts=("accomp",), annotate=False).write("midi", fp=str(acc_mid))
                mel_wav, acc_wav = scratch / f"{sid}_mel.wav", scratch / f"{sid}_acc.wav"
                fluidsynth(mel_mid, mel_wav)
                fluidsynth(acc_mid, acc_wav)
                wav, mp3 = tdir / f"{sid}.wav", tdir / f"{sid}.mp3"
                st = mix_master(mel_wav, acc_wav, music_s, wav, mp3)
                checks += check_audio(sid, st, LEAD_IN_S + music_s + TAIL_S)
                row.update({"wav": f"{tid}/{sid}.wav", "mp3": f"{tid}/{sid}.mp3",
                            "duration_s": round(st.duration_s, 3), "lufs": round(st.lufs, 2),
                            "peak_dbfs": round(st.peak_dbfs, 2), "wav_sha256": sha256(wav)})
            manifest.append(row)

            t = 0.0
            for seg_pos, seg in enumerate(s.segments):
                for n in seg.notes:
                    events.append({"stim_id": sid, "part": "melody", "motif": seg.label, "motif_pos": seg_pos,
                                   "onset_ql": t, "dur_ql": n.dur,
                                   "onset_s": round(t * 60.0 / s.bpm + LEAD_IN_S, 4),
                                   "dur_s": round(n.dur * 60.0 / s.bpm, 4),
                                   "pitch": n.p.nameWithOctave, "midi": n.p.midi, "ornamental": n.kind or ""})
                    t += n.dur
            print(f"  built {sid}", flush=True)

    _write_csv(out / "manifest.csv", manifest)
    _write_csv(out / "note_events.csv", events)
    _design_check(graphs, out / "reports")
    _validation_report(checks, out / "reports" / "validation_report.md")
    errors = [c for c in checks if not c.ok and c.severity == "error"]
    print(f"{len(manifest)} stimuli, {len(checks)} checks, {len(errors)} errors")
    for c in errors:
        print(f"  FAIL {c.stim_id} {c.name}: {c.detail}")
    return 1 if errors else 0


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
