/*
 * musiPAM shared experiment code (jsPsych 7). Every study's experiment.js builds its
 * timeline from these pieces, so consent, screening, questionnaires, data saving and
 * completion are identical across Studies 0-3.
 *
 * URL parameters:
 *   src=sona|prolific|local     recruitment source (inferred from the id parameter if absent)
 *   sona_id=..., PROLIFIC_PID=... participant id from the recruitment platform
 *   group=musician|nonmusician  recruitment stream (analysis uses the Gold-MSI regardless)
 *   order=0|1|2                 force a counterbalancing order (otherwise derived from the id)
 *   debug=1                     short run for testing: 2 items per block, audio cut to 1.5 s
 *
 * Study-specific values (SONA credit URL, Prolific codes, contact email) come from
 * config.js, which build.py writes from <study>/config.local.js. That file is gitignored:
 * the SONA credit token must not be in the public repository.
 */
const MusiPAM = (() => {
  "use strict";
  const params = new URLSearchParams(window.location.search);
  const get = (key, fallback = null) => params.get(key) ?? fallback;
  const DEBUG = get("debug") === "1";

  // ---------------------------------------------------------------- configuration
  const CONFIG = Object.assign({
    sonaCreditUrl: "https://ucla.sona-systems.com/webstudy_credit.aspx?experiment_id=EXPERIMENT_ID&credit_token=CREDIT_TOKEN&survey_code=",
    prolificCompletionUrl: "https://app.prolific.com/submissions/complete?cc=COMPLETION_CODE",
    prolificScreenoutUrl: "https://app.prolific.com/submissions/complete?cc=SCREENOUT_CODE",
    contactEmail: "[contact email from the IRB-approved consent]",
  }, window.MUSIPAM_CONFIG ?? {});
  const PLACEHOLDER = /EXPERIMENT_ID|CREDIT_TOKEN|COMPLETION_CODE|SCREENOUT_CODE/;

  /** True only on pavlovia.org with the Pavlovia plugin loaded; local runs never contact Pavlovia. */
  const ON_PAVLOVIA = typeof jsPsychPavlovia !== "undefined" && /(^|\.)pavlovia\.org$/.test(window.location.hostname);

  let cachedParticipant = null;
  function participant() {
    if (cachedParticipant) return cachedParticipant;
    const sona = get("sona_id") ?? get("SONA_ID");
    const prolific = get("PROLIFIC_PID");
    const src = get("src") ?? (sona ? "sona" : prolific ? "prolific" : "local");
    const id = sona ?? prolific ?? get("id") ?? `local-${Math.random().toString(36).slice(2, 10)}`;
    cachedParticipant = { src, id, group: get("group") };
    return cachedParticipant;
  }

  /** FNV-1a hash, for deterministic counterbalancing from a participant id. */
  function hashInt(s) {
    let h = 2166136261;
    for (const c of String(s)) {
      h ^= c.charCodeAt(0);
      h = Math.imul(h, 16777619);
    }
    return h >>> 0;
  }

  function counterbalance(id, n) {
    const forced = get("order");
    if (forced !== null && /^\d+$/.test(forced)) return Number(forced) % n;
    return hashInt(id) % n;
  }

  // ---------------------------------------------------------------- small HTML builders
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

  /** A required 1-7 rating row with labelled ends, for survey-html-form. */
  function scale7(name, question, low, high) {
    const opts = [1, 2, 3, 4, 5, 6, 7]
      .map((v) => `<label class="pt"><input type="radio" name="${name}" value="${v}" required><span>${v}</span></label>`)
      .join("");
    return `<fieldset class="q"><legend>${question}</legend><div class="scale7">${opts}</div>` +
      `<div class="ends"><span>1 = ${esc(low)}</span><span>7 = ${esc(high)}</span></div></fieldset>`;
  }

  /** A required single-choice question, for survey-html-form. */
  function choice(name, question, options) {
    const opts = options
      .map(([value, label]) => `<label class="opt"><input type="radio" name="${name}" value="${esc(value)}" required> ${esc(label)}</label>`)
      .join("");
    return `<fieldset class="q"><legend>${question}</legend><div class="opts">${opts}</div></fieldset>`;
  }

  function select(name, question, options) {
    const opts = options.map((o) => `<option value="${esc(o)}">${esc(o)}</option>`).join("");
    return `<label class="sel"><span>${question}</span><select name="${name}" required><option value="" selected disabled>Choose…</option>${opts}</select></label>`;
  }

  // ---------------------------------------------------------------- Pavlovia
  /** Opens a Pavlovia session. Call it after consent, so nothing is stored for people who decline. */
  function pavloviaInit() {
    return ON_PAVLOVIA ? [{ type: jsPsychPavlovia, command: "init" }] : [];
  }

  /**
   * Saves the data to Pavlovia (in pilot mode Pavlovia offers them as a CSV download instead).
   * Off Pavlovia nothing is sent anywhere; the final page offers the data as a CSV.
   */
  function pavloviaFinish() {
    return ON_PAVLOVIA ? [{ type: jsPsychPavlovia, command: "finish", participantId: participant().id }] : [];
  }

  // The Pavlovia plugin (2022.1.1) asks "Leave site?" on unload and never removes that
  // listener, which would stall the redirect to SONA or Prolific. This capturing listener
  // runs before it and, once the data are saved, stops it.
  let leaving = false;
  window.addEventListener("beforeunload", (e) => {
    if (leaving) e.stopImmediatePropagation();
  }, true);

  // ---------------------------------------------------------------- standard sections
  function browserCheck() {
    return {
      type: jsPsychBrowserCheck,
      // No device probing (webcam, microphone), and no refresh-rate measurement, which
      // stalls in a background tab and is irrelevant to audio studies.
      skip_features: ["vsync_rate", "webcam", "microphone"],
      minimum_width: 900,
      minimum_height: 600,
      data: { section: "browser_check" },
      inclusion_function: (d) => !d.mobile && ["chrome", "firefox", "safari", "edge-chromium"].includes(d.browser),
      exclusion_message: (d) => d.mobile
        ? "<p>This study needs a computer with headphones. Please return on a laptop or desktop computer.</p>"
        : "<p>Please use a recent version of Chrome, Firefox, Safari or Edge, and make the window at least 900 × 600 pixels.</p>",
    };
  }

  function consent(studyTitle) {
    return {
      type: jsPsychHtmlButtonResponse,
      stimulus:
        `<div class="page"><h1>${esc(studyTitle)}</h1>` +
        `<p class="todo">[IRB-APPROVED CONSENT TEXT GOES HERE. Replace this paragraph with the approved information sheet before any data collection.]</p>` +
        `<p>You will listen to short pieces of music over headphones and answer questions about them. ` +
        `Please work in a quiet place, wear headphones, and keep this window in focus until the end.</p>` +
        `<p>Questions: ${esc(CONFIG.contactEmail)}</p></div>`,
      choices: ["I agree to take part", "I do not agree"],
      data: { section: "consent" },
      on_finish: (d) => {
        d.consented = d.response === 0;
      },
    };
  }

  function fullscreen(on) {
    if (DEBUG) return [];
    return [{ type: jsPsychFullscreen, fullscreen_mode: on, message: on ? "<p>The study runs in full screen.</p>" : "", button_label: "Continue" }];
  }

  /** Plays a calibration sound until the participant has set a comfortable volume. */
  function volumeCheck(file) {
    return {
      timeline: [{
        type: jsPsychAudioButtonResponse,
        stimulus: file,
        prompt: "<div class='page'><h2>Set your volume</h2><p>Put on your headphones. Adjust your computer's volume until this music is clearly audible and comfortable. You can replay it.</p></div>",
        choices: ["Play again", "The volume is comfortable"],
        response_allowed_while_playing: true,
        trial_duration: DEBUG ? 1500 : null,
        data: { section: "volume" },
      }],
      loop_function: (data) => !DEBUG && data.values()[0].response === 0,
    };
  }

  /**
   * Headphone screen with Huggins-pitch stimuli (Milne et al., 2021): three noise bursts per
   * trial, one of which carries a faint tone that is audible only over headphones. Returns
   * { timeline, threshold }: pass = at least `threshold` correct of `trials.length`.
   */
  function headphoneCheck(trials, threshold = 5) {
    const timeline = [{
      type: jsPsychHtmlButtonResponse,
      stimulus: "<div class='page'><h2>Headphone check</h2><p>You will hear three bursts of noise. One of them contains a faint tone. " +
        "After each set, choose the burst with the tone. This check only works with headphones.</p></div>",
      choices: ["Start"],
      data: { section: "headphone_intro" },
    }];
    const used = DEBUG ? trials.slice(0, 2) : trials;
    used.forEach((t, i) => {
      timeline.push({
        type: jsPsychAudioButtonResponse,
        stimulus: t.file,
        prompt: `<p>Which noise contained the faint tone? (${i + 1} of ${used.length})</p>`,
        choices: ["First", "Second", "Third"],
        response_allowed_while_playing: false,
        data: { section: "headphone", answer: t.answer },
        on_finish: (d) => {
          d.correct = d.response + 1 === d.answer;
        },
      });
    });
    return { timeline, threshold: DEBUG ? 0 : threshold };
  }

  /**
   * Gold-MSI Musical Training subscale (7 items; Müllensiefen, Gingras, Musil & Stewart, 2014).
   * VERIFY the wording against the official Gold-MSI v1.0 English form before registration.
   */
  function goldMSI() {
    const agree = ["Completely disagree", "Strongly disagree", "Disagree", "Neither agree nor disagree", "Agree", "Strongly agree", "Completely agree"];
    const items = [
      ["gmsi_14", "I have never been complimented for my talents as a musical performer.", agree],
      ["gmsi_27", "I would not consider myself a musician.", agree],
      ["gmsi_32", "I engaged in regular, daily practice of a musical instrument (including voice) for ___ years.", ["0", "1", "2", "3", "4–5", "6–9", "10 or more"]],
      ["gmsi_33", "At the peak of my interest, I practised ___ hours per day on my primary instrument.", ["0", "0.5", "1", "1.5", "2", "3–4", "5 or more"]],
      ["gmsi_35", "I have had formal training in music theory for ___ years.", ["0", "0.5", "1", "2", "3", "4–6", "7 or more"]],
      ["gmsi_36", "I have had ___ years of formal training on a musical instrument (including voice) during my lifetime.", ["0", "0.5", "1", "2", "3–5", "6–9", "10 or more"]],
      ["gmsi_37", "I can play ___ musical instruments.", ["0", "1", "2", "3", "4", "5", "6 or more"]],
    ];
    return {
      type: jsPsychSurveyHtmlForm,
      preamble: "<div class='page'><h2>Your musical background</h2></div>",
      html: `<div class="page form">${items.map(([n, q, o]) => select(n, q, o)).join("")}</div>`,
      button_label: "Continue",
      data: { section: "gold_msi" },
    };
  }

  function background() {
    return {
      type: jsPsychSurveyHtmlForm,
      preamble: "<div class='page'><h2>About you</h2></div>",
      html: "<div class='page form'>" +
        select("age_band", "Age", ["18–20", "21–24", "25–29", "30–39", "40–49", "50 or older", "Prefer not to say"]) +
        `<label class="sel"><span>Main instrument(s), if any</span><input type="text" name="instrument" maxlength="80"></label>` +
        select("weekly_practice", "Hours of music practice in a typical week now", ["0", "Less than 1", "1–3", "4–7", "8–14", "15 or more"]) +
        select("headphones", "What are you listening with?", ["Over-ear headphones", "On-ear headphones", "In-ear headphones or earbuds", "Speakers", "Other"]) +
        select("environment", "How quiet are your surroundings right now?", ["Very quiet", "Mostly quiet", "Some background noise", "Noisy"]) +
        "</div>",
      button_label: "Continue",
      data: { section: "background" },
    };
  }

  function seriousness() {
    return {
      type: jsPsychSurveyHtmlForm,
      html: "<div class='page form'>" +
        choice("serious", "Did you complete this study seriously? <span class='note'>(Your answer will not affect your credit.)</span>", [["yes", "Yes"], ["no", "No"]]) +
        `<label class="sel"><span>Any comments? (optional)</span><textarea name="comments" rows="3" maxlength="1000"></textarea></label>` +
        "</div>",
      button_label: "Finish",
      data: { section: "seriousness" },
    };
  }

  function debrief(text) {
    return {
      type: jsPsychHtmlButtonResponse,
      stimulus: `<div class="page"><h2>Thank you</h2>${text}<p class="todo">[IRB-APPROVED DEBRIEF TEXT GOES HERE.]</p></div>`,
      choices: ["Submit and finish"],
      data: { section: "debrief" },
    };
  }

  // ---------------------------------------------------------------- the end of a session
  /** Where to send the participant once the data are saved; null = stay on a final page. */
  function completionUrl(outcome) {
    const p = participant();
    if (outcome === "declined") return null;
    if (p.src === "sona") return CONFIG.sonaCreditUrl + encodeURIComponent(p.id);
    if (p.src === "prolific") return outcome === "screened_out" ? CONFIG.prolificScreenoutUrl : CONFIG.prolificCompletionUrl;
    return null;
  }

  /**
   * Called from initJsPsych's on_finish. outcome: "completed" | "screened_out" | "declined".
   * Redirects to SONA or Prolific when configured; otherwise shows a final page, which on
   * local runs (nothing was sent anywhere) offers the data as a CSV file.
   */
  function finish(jsPsych, outcome) {
    const url = completionUrl(outcome);
    if (url && !DEBUG && !PLACEHOLDER.test(url)) {
      leaving = true;
      window.location.assign(url);
      return;
    }
    if (url && PLACEHOLDER.test(url)) console.error("musiPAM: completion URL still has placeholders; fill in config.local.js", url);
    const local = !ON_PAVLOVIA && outcome !== "declined";
    const text = outcome === "declined" ? "You chose not to take part, and no data were stored. You can close this window."
      : ON_PAVLOVIA ? "Your responses have been saved. You can close this window."
      : "This was a local run, so the responses were not sent anywhere.";
    const el = jsPsych.getDisplayElement();
    el.innerHTML = `<div class="page"><h2>Finished</h2><p>${text}</p>` +
      (local ? `<p><button class="jspsych-btn" id="musipam-save">Download the data (CSV)</button></p>` : "") + "</div>";
    if (local) {
      el.querySelector("#musipam-save").addEventListener("click", () =>
        jsPsych.data.get().localSave("csv", `musipam_${participant().id}.csv`));
    }
  }

  function shuffle(xs) {
    const a = xs.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  return {
    DEBUG, CONFIG, ON_PAVLOVIA, get, participant, hashInt, counterbalance, esc, scale7, choice, select,
    pavloviaInit, pavloviaFinish, browserCheck, consent, fullscreen, volumeCheck, headphoneCheck,
    goldMSI, background, seriousness, debrief, completionUrl, finish, shuffle,
  };
})();
