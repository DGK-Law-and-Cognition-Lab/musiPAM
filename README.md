# musiPAM

**Probabilistic analogical mapping for music.** musiPAM tests whether the mapping algorithm that explains verbal analogy (PAM; Lu, Ichien & Holyoak, 2022, *Psychological Review*) and visual analogy (visiPAM; Webb et al., 2023, *Nature Communications*) also explains how listeners map one passage of music onto another.

Each musical analog is a graph:

- **nodes** are two-bar motifs;
- **edges** are the relations between them: order, transposition, contour, rhythm, harmonic function and restatement.

This repository holds the stimulus set and the code that generates it, the motif graphs, the design checks, the study plan, and the preregistration drafts.

David G. Kamper · Department of Psychology, UCLA · [ORCID 0000-0003-0362-759X](https://orcid.org/0000-0003-0362-759X)

## Contents

```
docs/STUDY_PLAN.md        every study, one by one, and why 16 themes
docs/STIMULUS_SPEC.md     themes, transformation grid, rendering, validation, provenance
docs/RELATION_MODEL.md    plan for a learned relation model ("music BART")
relations/                the learned relation model ("music BART"): pair generator, model, tests
pam/                      PAM (Lu, Ichien & Holyoak, 2022) on the stimuli: Python port validated against the lab's MATLAB code
prereg/                   OSF-format preregistration drafts (Studies 0, 1a, 1b, 1c, 2, 3)
experiments/              jsPsych 7 code for the human studies, one Pavlovia project per study (Study 0 so far)
stimgen/                  the generator: themes, transformations, arrangement, rendering, graphs, checks
stimuli/T1 … T16/         per stimulus: score (.musicxml), .mid, .mp3, motif graph (.graph.json)
stimuli/manifest.csv      one row per stimulus, including the SHA-256 of its WAV master
stimuli/anchors/          well-known public-domain melodies for Study 0 (familiarity anchors, practice melody)
stimuli/note_events.csv   every melody note with its motif label
stimuli/reports/          validation report and design checks (symbolic and MERT)
```

The current set has **16 themes × 11 conditions = 176 stimuli**: four relational skeletons (sentence, period, rounded, sequence chain), each realized by four themes, with eight designed cross-mapping pairs (see `docs/STIMULUS_SPEC.md`).

## Rebuild the stimuli

WAV masters are not stored in git. The build is deterministic and regenerates them byte for byte; `manifest.csv` records each file's hash so any rebuild can be checked.

The audio is rendered with **Muse Sounds** through MuseScore Studio's command line: a clarinet (Berlin Woodwinds, Orchestral Tools) over a concert grand (Vienna Symphonic Library), and in the timbre variation a violin (Berlin Strings First Chairs) and a harp (Vienna Harp). Melody and accompaniment are rendered as separate stems, mixed with the melody 6 LU above the accompaniment, and normalized to −20 LUFS.

```bash
python3 -m venv ~/.venvs/musipam && ~/.venvs/musipam/bin/pip install -r stimgen/requirements.txt
cd stimgen && ~/.venvs/musipam/bin/python build.py
```

The build requires ffmpeg, MuseScore Studio 4.7.6 and the four Muse Sounds instruments above, all free through [Muse Hub](https://www.musehub.com). Before rendering, it checks MuseScore, the MuseSampler engine and the instrument libraries against the fingerprints in `stimgen/musipam_stim/muse_sounds.json`, and renders a reference score that must match a pinned hash, so an update cannot silently change the audio. Without Muse Sounds, `build.py --renderer fluidsynth` renders with FluidSynth and MuseScore's MS Basic soundfont (`Contents/Resources/sound/MS Basic.sf3`, placed at `~/.venvs/musipam/soundfonts/`). That route uses free software only, but its audio differs from the released files.

All musical content lives in `stimgen/musipam_stim/themes.py`. The build fails if an edit breaks a designed relation, makes a transformation inexact, or renders notes away from where the score puts them.

**Learned embeddings.** `stimgen/embed.py` embeds every motif with the pretrained music transformer [MERT-v1-95M](https://huggingface.co/m-a-p/MERT-v1-95M), at a pinned revision. The embedding arrays are not stored here because MERT is licensed CC BY-NC 4.0; run the script to regenerate them. It needs `stimgen/requirements-models.txt`.

## Run the experiments

`experiments/README.md` covers building a study, testing it locally, and deploying it to Pavlovia.

## Provenance

The themes were drafted with AI assistance (Anthropic Claude) to a written specification, and are being reviewed and revised by the first author. Every note is explicit in `themes.py`, and every transformation is deterministic code. No generative audio model is involved.

## License

- **Code** (`stimgen/`, `relations/`, `experiments/`): MIT. See [LICENSE](LICENSE).
- **Stimuli, documentation, reports and preregistrations** (`stimuli/`, `docs/`, `prereg/`, `relations/reports/`): CC BY 4.0. See [LICENSE-CC-BY-4.0.md](LICENSE-CC-BY-4.0.md). The relation model's training data come from folk-tune collections bundled with music21 and are not redistributed; `relations/build_corpus.py` regenerates them.
- **Third-party credits** (the sample libraries, the soundfont, MERT, the experiment libraries, PAM): see [NOTICE.md](NOTICE.md).

## Citation

See [CITATION.cff](CITATION.cff). Releases are archived on Zenodo with a DOI.
