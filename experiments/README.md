# musiPAM experiments

jsPsych 7 code for the human studies. Each study runs as its own Pavlovia project, and all of them are built from the shared code here. Consent, the checks for automated participants, the headphone screen, the questionnaires, data saving and the end-of-session redirect are therefore identical across studies.

The page design and the checks for automated participants follow the lab's earlier Pavlovia studies: a white card on a light page in Georgia type, a thin progress bar, "Next →" buttons at the bottom right, answers as bordered rows or numbered boxes, and the same captcha, reading task, task check, minimum page times and AI-use question.

| Path | What it is |
|---|---|
| `shared/musipam.js` | Shared pieces: participant ids, counterbalancing, page and form builders, the checks for automated participants, consent, volume check, headphone screen, questionnaires, debrief, Pavlovia saving, redirect. |
| `shared/musipam.css` | The page design (the lab's house style), applied to jsPsych's pages. |
| `shared/plugin-audio-tap.js` | jsPsych plugin: plays a melody and records every space-bar press, timed on the audio clock. |
| `shared/plugin-reading-window.js` | jsPsych plugin: the moving-window reading task. |
| `shared/captcha.png` | The captcha image ("press Q"), shared with the lab's earlier studies. |
| `shared/make_headphone_stimuli.py` | The six Huggins-pitch trials (Milne et al., 2021) and the volume-calibration sound. |
| `shared/config.template.js` | Template for a study's private settings (see below). |
| `shared/libs.json` | jsPsych 7.3.4, its plugins and the Pavlovia plugin, pinned by URL and SHA-256. |
| `study0/` | Study 0 (stimulus norming): `index.html`, `experiment.js`, and the gitignored `config.local.js`. Design: `../prereg/S0_norming.md`. |
| `build.py` | Assembles `dist/<study>/`, the folder that goes to Pavlovia. |
| `serve.py` | Serves a built study on this computer for testing. |

## A Study 0 session

1. The sounds load. A browser check (silent unless it fails) and the device question ("desktop or laptop?") come first.
2. Welcome page; its button enters full screen.
3. Image captcha (see below).
4. Consent: a link to the IRB-approved form on UCLA Box, and the form's two options. Declining ends the session; nothing is stored.
5. The Pavlovia session opens. Two reading-task sentences, each followed by "Did you understand the sentence?".
6. Volume, then the headphone screen (6 Huggins-pitch trials; at least 5 correct to continue).
7. Instructions, then the task check ("What is your task in this study?"). A wrong answer shows the instructions again, with one retry.
8. The three parts (familiarity, naturalness, musical ideas), in the participant's counterbalanced order. Each opens with a banner ("Part 1 of 3") and a practice melody; the two rating parts each contain one attention check.
9. Musical background (Gold-MSI Musical Training), About you (age, gender, native language, instruments, practice), listening setup, the AI-use question, final questions (seriousness, headphones, full screen, distractions), feedback, debrief.
10. The data are saved, then SONA grants credit or Prolific gets its code.

The consent form lists the demographics it covers: age, gender, language and musical background. The questionnaires ask nothing beyond that.

## Checks for automated participants

The same checks as the lab's earlier studies, plus the headphone screen:

| Check | What happens | Recorded as |
|---|---|---|
| Automated browser | A user agent naming ChatGPT, Atlas or OAI-SearchBot sees "Study Unavailable" and cannot start. | (no data) |
| Webdriver flag | `navigator.webdriver` (true under Selenium, Playwright and similar) is recorded on every row. | `webdriver` |
| Image captcha | The picture says "press Q". White 1-pixel text, hidden from screen readers, says "press Z". Q shows the Next button; Z ends the session before consent, so nothing is stored. | `captcha_response`, `captcha_pass` (section `captcha`, local only) |
| Reading task | Two sentences, read word by word with the space bar. A median word time below 150 ms on either sentence flags implausibly fast or automated reading. | section `reading`: `rts`, `median_rt`, `fast`, `repeat_presses`; section `reading_check`: `understood` |
| Task check | "What is your task in this study?" after the instructions; one retry after reading them again. | section `task_check`: `attempt`, `task_check_pass` |
| Minimum page times | Next stays disabled, counting down, for 15 s on the instructions, 7 s on each part's introduction, 5 s on the reading-task and headphone introductions and on the task check. | |
| Pasting | Blocked in every text field. | |
| AI use | "Did you use any AI tool (such as ChatGPT, Claude, or similar) to help answer any of the questions in this study?" | section `ai_usage` |
| Headphone screen | Huggins pitch is audible only over headphones. | section `headphone`: `correct` |

## Build

```bash
~/.venvs/musipam/bin/python build.py study0
```

This writes `dist/study0/`:

- the code, the stylesheet and `captcha.png`;
- `config.js`, from `study0/config.local.js`;
- `lib/`, the pinned libraries, served from the study's own folder so a slow CDN cannot stall a session;
- `audio/`, the 16 identity themes, 4 anchor melodies and the practice melody;
- `hp/`, the headphone-screen WAVs;
- `stimuli.json`, the item list with each theme's designed motif boundaries and barlines.

`stimuli.json` also records the stimulus-set version, a hash of the two manifests, and every data row carries it. The anchors and the practice melody come from `../stimgen/build_anchors.py`.

## Test on this computer

```bash
~/.venvs/musipam/bin/python serve.py study0
```

Then open <http://localhost:8765/?debug=1&participant=PILOT_DK1>.

- `debug=1` makes a short run: one theme and one anchor per part, audio cut to 1.5 s, no full screen, no minimum waits, and a headphone screen that always passes.
- On the captcha page press Q. Pressing Z (the hidden instruction) ends the session.
- In a debug run, `jsPsych.data.get()` in the browser console shows the data.
- The final page of any local run offers the data as a CSV.
- Nothing is sent anywhere unless the page runs on pavlovia.org.

| URL parameter | Effect |
|---|---|
| `sona_id=…`, `survey_code=…`, or a numeric `participant=…` | SONA participant id; the session ends with the SONA credit redirect. |
| `PROLIFIC_PID=…` | Prolific participant id; the session ends with the Prolific code. |
| `participant=PILOT_…` or `TEST_…` | A test id: recorded with `is_test = true`, and no redirect. |
| `group=musician` | Recruitment stream, recorded in every row. |
| `order=0\|1\|2` | Forces a part order. Otherwise the order comes from a hash of the participant id. |
| `debug=1` | The short test run described above. |

## Deploy to Pavlovia

Each study gets its own Pavlovia project (a GitLab repository on gitlab.pavlovia.org). That gives each study its own data folder, piloting/running switch and recruitment link. A registered study's code also stays frozen while later studies change.

Pavlovia charges for each completed session unless an institutional licence covers it. UCLA's licence covers the musiPAM studies (confirmed by D. Kamper, 2026-11-09), so no credits need to be bought or assigned.

1. Create the project, e.g. `musipam/study-0-norming`, and keep it **private**: the deployed `config.js` holds the SONA credit token. The existing `musipam/study-1` can be renamed or kept for Study 1.
2. Clone it, copy the contents of `dist/study0/` into it, then commit and push. Do not commit a `config.json` of your own: Pavlovia writes the correct one, and a committed one overrides it.
3. On the Pavlovia dashboard, set the project to **Piloting**. Pilot runs offer the data as a CSV download instead of saving it. Test the whole session, including the redirect.
4. Set it to **Running** for data collection. Decide whether to turn on "save incomplete results". Data are stored only after consent: the Pavlovia session opens on the page after the consent page.

**Recruitment links.**

- SONA: `https://run.pavlovia.org/musipam/study-0-norming/?sona_id=%SURVEY_CODE%`
- Prolific: `https://run.pavlovia.org/musipam/study-0-norming/?PROLIFIC_PID={{%PROLIFIC_PID%}}&group=musician`

**Private settings.** `study0/config.local.js` (gitignored; template in `shared/config.template.js`) holds:

- `studyTitle`, shown on the welcome page: use the SONA listing's title;
- `consentUrl`, the IRB-approved consent form ("CONSENT FORM_MusiPAM.pdf" on UCLA Box; filled in);
- `contactName` and `contactEmail`, the contact in the consent form (filled in);
- `sonaCreditUrl`, from the SONA listing (it contains the credit token);
- `prolificCompletionUrl` and `prolificScreenoutUrl`, if Prolific is used.

Rebuild after editing it. It must never enter the public repository. While a placeholder remains in a redirect URL, the experiment never redirects there.

At the end of a session:

| Outcome | Data saved | Where the participant goes |
|---|---|---|
| Completed | yes | SONA: credit granted. Prolific: completion code. |
| Failed the headphone screen | yes | SONA: credit granted. Prolific: screen-out code. |
| Declined consent | no | A closing page. |
| Captcha trap (Z) or not on a computer | no | A closing page; the session cannot continue. |

## Before any data collection

- [x] IRB-approved consent form linked (`consentUrl`), with its contact.
- [ ] The debrief text (`DEBRIEF` in `study0/experiment.js`) checked against what the IRB approved.
- [ ] `studyTitle` matched to the SONA listing; `sonaCreditUrl` (and the Prolific codes, if used) filled in; one complete pilot run per recruitment source, through the redirect.
- [ ] Gold-MSI item wording checked against the official v1.0 English form (`goldMSI()`).
- [ ] The preregistration's open DECISIONs resolved, including the part order, the anchor list and the exclusions for the automated-participant checks (`../prereg/S0_norming.md`).

## Data

One CSV per session, one row per trial. Columns used in the analysis:

- **Every row:** `study`, `stimulus_set`, `participant_id`, `source`, `group`, `is_test`, `block_order`, `debug`, `webdriver`.
- **Ratings:** `section` (familiarity / naturalness / segmentation / …), `phase` (intro / listen / rate / tap / practice / attention_check), `item`, `kind` (theme / anchor / practice), `theme`. Ratings are in `response` (JSON): `recognized`, `familiarity`, `naturalness`, `liking`.
- **Segmentation:** `taps`, in seconds from audio onset. Compare them with the item's `boundaries` and `barlines` in `stimuli.json`.
- **Checks:** `audio_failed` (listening and tapping trials), `check_passed` (attention checks), `correct` (headphone screen), the reading task (`fast`, `median_rt`), the task check (`task_check_pass` by `attempt`), `ai_usage`, and the final questions (`serious`, `headphones_throughout`, `fullscreen_maintained`, `distractions`).
- **Questionnaires:** sections `gold_msi` (items `gmsi_14` … `gmsi_37`, values 1-7 by option position), `background` (`age`, `gender`, `native_language`, `instrument`, `weekly_practice`), `listening_setup`, `feedback`.
- **Consent:** `consented`, `consent_time` (section `consent`).

## Licenses

The code here is MIT, like `stimgen/`. The audio files are the musiPAM stimuli (CC BY 4.0). `captcha.png` is shared with the lab's earlier studies. The libraries the build downloads, jsPsych and the Pavlovia plugin, are MIT-licensed by their authors and are not stored in this repository.
