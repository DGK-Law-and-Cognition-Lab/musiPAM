# musiPAM experiments

jsPsych 7 code for the human studies. Each study runs as its own Pavlovia project, and all of them are built from the shared code here. Consent, the headphone screen, the Gold-MSI, data saving and the end-of-session redirect are therefore identical across studies.

| Path | What it is |
|---|---|
| `shared/musipam.js` | Shared pieces: participant ids, counterbalancing, consent, browser check, volume check, headphone screen, Gold-MSI, background questions, debrief, Pavlovia saving, redirect. |
| `shared/plugin-audio-tap.js` | jsPsych plugin: plays a melody and records every space-bar press, timed on the audio clock. |
| `shared/make_headphone_stimuli.py` | The six Huggins-pitch trials (Milne et al., 2021) and the volume-calibration sound. |
| `shared/config.template.js` | Template for a study's private settings (see below). |
| `shared/libs.json` | jsPsych 7.3.4, its plugins and the Pavlovia plugin, pinned by URL and SHA-256. |
| `study0/` | Study 0 (stimulus norming): `index.html`, `experiment.js`. Design: `../prereg/S0_norming.md`. |
| `build.py` | Assembles `dist/<study>/`, the folder that goes to Pavlovia. |
| `serve.py` | Serves a built study on this computer for testing. |

## Build

```bash
~/.venvs/musipam/bin/python build.py study0
```

This writes `dist/study0/`:

- the code;
- `lib/`, the pinned libraries, served from the study's own folder so a slow CDN cannot stall a session;
- `audio/`, the 16 identity themes, 4 anchor melodies and the practice melody;
- `hp/`, the headphone-screen WAVs;
- `stimuli.json`, the item list with each theme's designed motif boundaries and barlines.

`stimuli.json` also records the stimulus-set version, a hash of the two manifests, and every data row carries it. The anchors and the practice melody come from `../stimgen/build_anchors.py`.

## Test on this computer

```bash
~/.venvs/musipam/bin/python serve.py study0
```

Then open <http://localhost:8765/?debug=1>.

- `debug=1` makes a short run: one theme and one anchor per block, audio cut to 1.5 s, no full screen, and a headphone screen that always passes.
- In a debug run, `jsPsych.data.get()` in the browser console shows the data.
- The final page of any local run offers the data as a CSV.
- Nothing is sent anywhere unless the page runs on pavlovia.org.

| URL parameter | Effect |
|---|---|
| `sona_id=…` / `PROLIFIC_PID=…` | Participant id; also sets the source and the redirect at the end. |
| `group=musician` | Recruitment stream, recorded in every row. |
| `order=0\|1\|2` | Forces a block order. Otherwise the order comes from a hash of the participant id. |
| `debug=1` | The short test run described above. |

## Deploy to Pavlovia

Each study gets its own Pavlovia project (a GitLab repository on gitlab.pavlovia.org). That gives each study its own data folder, piloting/running switch and recruitment link. A registered study's code also stays frozen while later studies change.

1. Create the project, e.g. `musipam/study-0-norming`. The existing `musipam/study-1` can be renamed or kept for Study 1.
2. Clone it, copy the contents of `dist/study0/` into it, then commit and push.
3. On the Pavlovia dashboard, set the project to **Piloting**. Pilot runs offer the data as a CSV download instead of saving it. Test the whole session, including the redirect.
4. Set it to **Running** for data collection. Decide whether to turn on "save incomplete results". Data are stored only after consent: the Pavlovia session opens on the page after the consent page.

**Recruitment links.**

- SONA: `https://run.pavlovia.org/musipam/study-0-norming/?sona_id=%SURVEY_CODE%`
- Prolific: `https://run.pavlovia.org/musipam/study-0-norming/?PROLIFIC_PID={{%PROLIFIC_PID%}}&group=musician`

**Private settings.** Copy `shared/config.template.js` to `study0/config.local.js` and fill in:

- the SONA credit URL (it contains the credit token);
- the Prolific completion and screen-out codes;
- the contact email.

Then rebuild. `config.local.js` is gitignored and must never enter the public repository. While a placeholder remains, the experiment never redirects.

At the end of a session:

| Outcome | Data saved | Where the participant goes |
|---|---|---|
| Completed | yes | SONA: credit granted. Prolific: completion code. |
| Failed the headphone screen | yes | SONA: credit granted. Prolific: screen-out code. |
| Declined consent | no | A closing page. |

## Before any data collection

- [ ] IRB-approved consent and debrief text (the `[IRB-…]` boxes in `shared/musipam.js`) and the contact email.
- [ ] Gold-MSI item wording checked against the official v1.0 English form (`goldMSI()`).
- [ ] `config.local.js` filled in; one complete pilot run per recruitment source, through the redirect.
- [ ] The preregistration's open DECISIONs resolved, including the block order and the anchor list (`../prereg/S0_norming.md`).

## Data

One CSV per session, one row per trial. Columns used in the analysis:

- **Every row:** `study`, `stimulus_set`, `participant_id`, `source`, `group`, `block_order`, `debug`.
- **Ratings:** `section` (familiarity / naturalness / segmentation / …), `phase` (listen / rate / tap / practice / attention_check), `item`, `kind` (theme / anchor / practice), `theme`. Ratings are in `response` (JSON).
- **Segmentation:** `taps`, in seconds from audio onset. Compare them with the item's `boundaries` and `barlines` in `stimuli.json`.
- **Exclusions:** `audio_failed` (listening and tapping trials), `check_passed` (attention checks), `correct` (headphone screen), the `seriousness` response, and `time_elapsed`.

## Licenses

The code here is MIT, like `stimgen/`. The audio files are the musiPAM stimuli (CC BY 4.0). The libraries the build downloads, jsPsych and the Pavlovia plugin, are MIT-licensed by their authors and are not stored in this repository.
