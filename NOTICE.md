# Third-party notices

## Soundfont used to render the audio

The audio in `stimuli/` is rendered with **MS Basic.sf3**, which ships with MuseScore 4 and is MuseScore_General v0.2. It is shared under the MIT license. Its credits, which must accompany derivative works:

- FluidR3 (original version) by Frank Wen. Copyright (c) 2000–02.
- Mono conversion (FluidR3Mono) by Michael Cowgill. Copyright (c) 2014–17.
- Adaptation for MuseScore_General.sf2 by S. Christian Collins. Copyright (c) 2018–19.
- Temple Blocks instrument provided by Ethan Winer. Copyright (c) 2002.
- Drumline Cymbals provided by Michael Schorsch. Copyright (c) 2016.

The soundfont itself is not redistributed here. The build verifies its SHA-256 hash: `5ea2375e8bd7d8e71def1036978c1621e85b66934169b6a2744b27b9b3c2d99c`.

## MERT

The motif embeddings are computed with **MERT-v1-95M** (Li et al., 2024; https://huggingface.co/m-a-p/MERT-v1-95M, revision `12af15fef9d0ac838c3f475bfbbf26d2060dd4f5`). The model is licensed CC BY-NC 4.0. Its weights and the raw embedding arrays are not redistributed here; `stimgen/embed.py` regenerates the arrays from the pinned model.

## Software

The stimuli are built with music21, NumPy, SciPy, pyloudnorm, soundfile, FluidSynth and ffmpeg, each under its own license.

## Experiment libraries

The experiments in `experiments/` run on jsPsych 7.3.4 (de Leeuw, 2015; https://www.jspsych.org) and its plugins, and save data with the Pavlovia jsPsych plugin (version 2022.1.1, Ilixa Ltd.). Both are MIT-licensed. Neither is stored here: `experiments/build.py` downloads the versions pinned in `experiments/shared/libs.json` and checks their SHA-256 hashes.

## Anchor melodies

`stimuli/anchors/` holds arrangements of public-domain melodies: "Ode to Joy" (Beethoven), "Frère Jacques" and "Greensleeves" (traditional), "Amazing Grace" (the hymn tune "New Britain"), and "Twinkle, Twinkle, Little Star" ("Ah! vous dirai-je, maman"). The arrangements come from the same pipeline as the themes and are CC BY 4.0, like the rest of `stimuli/`.

## PAM

`pam/pam.py` is a Python port of `TestMapping_PAMfunc.m` from the PAM code of Hongjing Lu, Nicholas Ichien and Keith J. Holyoak, included with the authors' permission. It reproduces the MATLAB original to machine precision (`pam/validate.py`). If you use it, cite:

Lu, H., Ichien, N., & Holyoak, K. J. (2022). Probabilistic analogical mapping with semantic relation networks. *Psychological Review, 129*(5), 1078–1103. https://doi.org/10.1037/rev0000358

