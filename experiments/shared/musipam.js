/*
 * musiPAM shared experiment code (jsPsych 7). Every study's experiment.js builds its timeline
 * from these pieces, so consent, screening, the checks for automated participants, the
 * questionnaires, data saving and completion are identical across Studies 0-3.
 *
 * The page design and the checks against automated participants follow the lab's earlier
 * Pavlovia studies:
 *   1. Browsers whose user agent names ChatGPT or Atlas are turned away at once.
 *      navigator.webdriver (true under Selenium, Playwright and similar tools) is recorded.
 *   2. An image captcha. The picture says "press Q"; text that people cannot see says "press Z".
 *      A program that reads the page instead of the picture presses Z, and the session stops
 *      before consent, so nothing is stored.
 *   3. A two-sentence moving-window reading task after consent. A median word time below
 *      150 ms on either sentence flags implausibly fast or automated responding.
 *   4. A task check after the instructions ("What is your task in this study?"), with one
 *      retry after reading them again.
 *   5. Minimum reading times on instruction pages, blocked pasting, and a closing question
 *      about the use of AI tools.
 * The headphone screen (Huggins pitch) is a further check that a person is listening.
 *
 * URL parameters:
 *   sona_id=, survey_code=, participant=   participant id from SONA (a numeric participant= is read as a SONA code)
 *   PROLIFIC_PID=                          participant id from Prolific
 *   src=sona|prolific|local                recruitment source, when it should not be inferred
 *   group=musician|nonmusician             recruitment stream (analysis uses the Gold-MSI regardless)
 *   order=0|1|2                            force a counterbalancing order (otherwise derived from the id)
 *   debug=1                                short test run: no waits or full screen, audio cut to 1.5 s
 * An id that starts with PILOT or TEST is recorded with is_test = true.
 *
 * Study-specific values (title, consent link, contact, SONA credit URL, Prolific codes) come
 * from config.js, which build.py writes from <study>/config.local.js. That file is gitignored:
 * the SONA credit token must not be in the public repository.
 */
const MusiPAM = (() => {
  "use strict";
  const params = new URLSearchParams(window.location.search);
  const get = (key, fallback = null) => params.get(key) ?? fallback;
  const DEBUG = get("debug") === "1";

  // ---------------------------------------------------------------- configuration
  const CONFIG = Object.assign({
    studyTitle: "Listening to Music",
    consentUrl: "",
    contactName: "the researchers",
    contactEmail: "",
    sonaCreditUrl: "https://ucla.sona-systems.com/webstudy_credit.aspx?experiment_id=EXPERIMENT_ID&credit_token=CREDIT_TOKEN&survey_code=",
    prolificCompletionUrl: "https://app.prolific.com/submissions/complete?cc=COMPLETION_CODE",
    prolificScreenoutUrl: "https://app.prolific.com/submissions/complete?cc=SCREENOUT_CODE",
  }, window.MUSIPAM_CONFIG ?? {});
  const PLACEHOLDER = /EXPERIMENT_ID|CREDIT_TOKEN|COMPLETION_CODE|SCREENOUT_CODE/;

  /** Seconds before Next is enabled ("Please wait (7s)..."). No waits in debug runs. */
  const MIN_SECONDS = { instructions: 15, partIntro: 7, readingIntro: 5, taskCheck: 5, headphoneIntro: 5 };
  /** Reading task: the two neutral sentences of the lab's earlier studies. */
  const SPR_SENTENCES = [
    { id: "spr1", text: "A colorful rainbow appeared across the valley after the brief afternoon storm" },
    { id: "spr2", text: "Several students from the university volunteered at the local library on Saturday" },
  ];
  const SPR_FAST_MEDIAN_MS = 150;
  const TASK_CHECK = {
    question: "What is your task in this study?",
    options: [
      ["1", "Writing poetry"],
      ["2", "Viewing images and reporting your emotional reactions"],
      ["3", "Listening to short melodies and answering questions about them"],
      ["4", "Ranking sports teams"],
      ["5", "Comparing two pictures"],
    ],
    correct: "3",
  };

  /** True only on pavlovia.org with the Pavlovia plugin loaded; local runs never contact Pavlovia. */
  const ON_PAVLOVIA = typeof jsPsychPavlovia !== "undefined" && /(^|\.)pavlovia\.org$/.test(window.location.hostname);

  // ---------------------------------------------------------------- session state
  // outcome: "completed" | "declined" | "screened_out"; decides where the participant goes at the end.
  const state = { jsPsych: null, outcome: "completed" };
  const bind = (jsPsych) => { state.jsPsych = jsPsych; };
  const setOutcome = (value) => { state.outcome = value; };
  // Progress: jsPsych's own estimate jumps back when a conditional branch is skipped, so the
  // bar counts the trials of the main path (branches marked offPath are left out) and moves
  // one step per finished trial; it reaches 100% on the final page.
  const offPathNodes = new WeakSet();
  const offPath = (node) => { offPathNodes.add(node); return node; };
  function countTrials(nodes) {
    let n = 0;
    for (const node of nodes) {
      if (offPathNodes.has(node)) continue;
      n += Array.isArray(node.timeline) ? countTrials(node.timeline) : 1;
    }
    return n;
  }
  function progress(timeline) {
    const total = Math.max(1, countTrials(timeline));
    let done = 0;
    return () => {
      done += 1;
      state.jsPsych.setProgressBar(Math.min(0.99, done / total));
    };
  }
  /** The `key` of the most recent data row of a section, or undefined. */
  const lastValue = (section, key) => state.jsPsych.data.get().filter({ section }).last(1).values()[0]?.[key];

  // ---------------------------------------------------------------- automated participants
  const UA = navigator.userAgent.toLowerCase();
  const automatedBrowser = /atlas|chatgpt|oai-searchbot/.test(UA);
  const webdriver = navigator.webdriver === true;
  // Pasting is blocked everywhere except in fields marked data-allow-paste="true" (as in the lab's earlier studies).
  document.addEventListener("paste", (e) => {
    if (e.target?.dataset?.allowPaste !== "true") e.preventDefault();
  });

  let cachedParticipant = null;
  function participant() {
    if (cachedParticipant) return cachedParticipant;
    const sona = get("sona_id") ?? get("SONA_ID") ?? get("survey_code");
    const prolific = get("PROLIFIC_PID");
    const other = get("participant") ?? get("id");
    const id = sona ?? prolific ?? other ?? `local-${Math.random().toString(36).slice(2, 10)}`;
    const src = get("src") ?? (sona || /^\d+$/.test(other ?? "") ? "sona" : prolific ? "prolific" : "local");
    cachedParticipant = { src, id, group: get("group"), isTest: /^(PILOT|TEST)/i.test(id) };
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

  function shuffle(xs) {
    const a = xs.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  // ---------------------------------------------------------------- page outside jsPsych
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const contactLine = () => CONFIG.contactEmail
    ? `${esc(CONFIG.contactName)} at <a href="mailto:${esc(CONFIG.contactEmail)}">${esc(CONFIG.contactEmail)}</a>`
    : esc(CONFIG.contactName);

  /** Shows the page container (index.html hides it behind a loading screen until the study is ready). */
  function ready() {
    document.getElementById("loading-screen")?.remove();
    const c = document.getElementById("experimentContainer");
    if (c) c.hidden = false;
  }

  /** A card outside jsPsych, for pages shown before the experiment can start. */
  function showStatic(html) {
    ready();
    document.getElementById("jspsych-target").innerHTML =
      `<div class="jspsych-display-element"><div class="jspsych-content-wrapper"><div class="jspsych-content">${html}</div></div></div>`;
  }
  const BLOCKED_HTML = "<h1>Study Unavailable</h1><p>This study cannot be completed using an automated browser.</p>";
  const loadErrorHTML = (what) => `<h1>The Study Could Not Load</h1><p>${esc(what)}</p>` +
    `<p>Please try reloading the page. If the problem continues, contact ${contactLine()}.</p>`;

  // ---------------------------------------------------------------- answer builders (house style)
  /** One required choice, as bordered rows. options: [[value, label HTML], ...]. */
  function radioGroup(name, question, options, opts = {}) {
    const rows = options.map(([value, label]) =>
      `<label class="radio-option"><input type="radio" name="${name}" value="${esc(value)}"> ${label}</label>`).join("");
    return `<div class="form-group"${opts.optional ? "" : ' data-required="choice"'}>` +
      (question ? `<p class="question-text">${question}</p>` : "") + (opts.hint ? `<p class="hint">${opts.hint}</p>` : "") +
      `<div class="radio-group">${rows}</div><p class="error-msg">${opts.error ?? "Please select an answer."}</p></div>`;
  }

  /** One required rating, as a row of boxes. labels: ["1 = Not at all familiar", "2", ...]. */
  function scaleGroup(name, question, labels, opts = {}) {
    const boxes = labels.map((label, i) =>
      `<label class="scale-option"><input type="radio" name="${name}" value="${opts.values?.[i] ?? i + 1}"><span>${esc(label)}</span></label>`).join("");
    return `<div class="form-group" data-required="choice">` +
      (question ? `<p class="question-text">${question}</p>` : "") + (opts.hint ? `<p class="hint">${opts.hint}</p>` : "") +
      `<div class="scale-group">${boxes}</div><p class="error-msg">${opts.error ?? "Please select one of the boxes."}</p></div>`;
  }

  function textField(name, question, opts = {}) {
    const attrs = opts.type === "number" ? ` type="number" min="${opts.min ?? ""}" max="${opts.max ?? ""}"` : ' type="text" maxlength="120"';
    return `<div class="form-group"${opts.optional ? "" : ' data-required="text"'}><p class="question-text">${question}</p>` +
      `<input name="${name}"${attrs} placeholder="${esc(opts.placeholder ?? "")}" autocomplete="off">` +
      `<p class="error-msg">${opts.error ?? "Please answer this question."}</p></div>`;
  }

  function textArea(name, question, opts = {}) {
    return `<div class="form-group"${opts.optional ? "" : ' data-required="text"'}><p class="question-text">${question}</p>` +
      `<textarea name="${name}" maxlength="2000" placeholder="${esc(opts.placeholder ?? "Please write your answer, or type NA")}"></textarea>` +
      `<p class="error-msg">${opts.error ?? "Please write an answer (or type NA)."}</p></div>`;
  }

  // ---------------------------------------------------------------- trial builders
  /** Disables the page's buttons for `secs` seconds, counting down on them (the house minimum wait). */
  function withMinWait(trial, secs) {
    if (!secs || DEBUG) return trial;
    const before = trial.on_load;
    return Object.assign({}, trial, {
      on_load: function () {
        if (before) before.apply(this, arguments);
        const btns = [...document.querySelectorAll("#jspsych-content .jspsych-btn")];
        if (!btns.length) return;
        const isInput = (b) => b.tagName === "INPUT";
        const labels = btns.map((b) => (isInput(b) ? b.value : b.innerHTML));
        const show = (n) => btns.forEach((b) => { if (isInput(b)) b.value = `Please wait (${n}s)...`; else b.textContent = `Please wait (${n}s)...`; });
        let left = secs;
        btns.forEach((b) => { b.disabled = true; });
        show(left);
        const timer = setInterval(() => {
          left -= 1;
          if (!btns[0].isConnected) { clearInterval(timer); return; }
          if (left > 0) { show(left); return; }
          clearInterval(timer);
          btns.forEach((b, i) => { b.disabled = false; if (isInput(b)) b.value = labels[i]; else b.innerHTML = labels[i]; });
        }, 1000);
      },
    });
  }

  /** A page with one button. */
  function page(html, opts = {}) {
    return withMinWait({
      type: jsPsychHtmlButtonResponse,
      stimulus: html,
      choices: [opts.button ?? "Next →"],
      data: Object.assign({ section: opts.section ?? "instructions" }, opts.data ?? {}),
      on_finish: opts.on_finish,
    }, opts.wait ?? 0);
  }

  /** A page that cannot be left (the study stops here; nothing is saved). */
  function deadEnd(html, section) {
    return { type: jsPsychHtmlButtonResponse, stimulus: `<div class="center-text">${html}</div>`, choices: [], data: { section } };
  }

  /** A questionnaire page. Every field marked data-required must be answered before Next works. */
  function form(html, opts = {}) {
    return withMinWait({
      type: jsPsychSurveyHtmlForm,
      html,
      button_label: opts.button ?? "Next →",
      autofocus: "",
      data: Object.assign({ section: opts.section ?? "form" }, opts.data ?? {}),
      on_load: requireAnswers,
      on_finish: opts.on_finish,
    }, opts.wait ?? 0);
  }

  function answered(group) {
    if (group.dataset.required === "choice") return !!group.querySelector("input:checked");
    const el = group.querySelector("input, textarea, select");
    const v = (el?.value ?? "").trim();
    if (!v) return false;
    if (el.type !== "number") return true;
    const n = Number(v);
    return Number.isFinite(n) && (el.min === "" || n >= Number(el.min)) && (el.max === "" || n <= Number(el.max));
  }

  /** House-style checks in place of the browser's: an unanswered question turns red with a message. */
  function requireAnswers() {
    const f = document.getElementById("jspsych-survey-html-form");
    if (!f) return;
    f.noValidate = true;
    const clear = (e) => e.target.closest("[data-required]")?.classList.remove("unanswered");
    f.addEventListener("change", clear);
    f.addEventListener("input", clear);
    f.addEventListener("submit", (e) => {
      let first = null;
      f.querySelectorAll("[data-required]").forEach((g) => {
        const ok = answered(g);
        g.classList.toggle("unanswered", !ok);
        if (!ok && !first) first = g;
      });
      if (first) {
        e.preventDefault();
        e.stopImmediatePropagation();
        first.scrollIntoView({ block: "center", behavior: "smooth" });
      }
    }, true);
  }

  // ---------------------------------------------------------------- Pavlovia
  /** Opens a Pavlovia session. Call it after consent, so nothing is stored for people who decline. */
  function pavloviaInit() {
    return ON_PAVLOVIA ? [{ type: jsPsychPavlovia, command: "init" }] : [];
  }

  /** Saves the data to Pavlovia (pilot mode offers them as a CSV download instead). */
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

  // ---------------------------------------------------------------- before consent
  /** jsPsych's browser check, silent unless it fails: a computer, a common browser, a large enough window. */
  function browserCheck() {
    return {
      type: jsPsychBrowserCheck,
      // No device probing (webcam, microphone), and no refresh-rate measurement, which
      // stalls in a background tab and is irrelevant to audio studies.
      skip_features: ["vsync_rate", "webcam", "microphone"],
      minimum_width: 900,
      minimum_height: 600,
      window_resize_message: "<p>Please make your browser window larger to continue.</p>" +
        "<p>Minimum width: <span id='browser-check-min-width'></span> px. Your width: <span id='browser-check-actual-width'></span> px.</p>" +
        "<p>Minimum height: <span id='browser-check-min-height'></span> px. Your height: <span id='browser-check-actual-height'></span> px.</p>",
      data: { section: "browser_check" },
      inclusion_function: (d) => !d.mobile && ["chrome", "firefox", "safari", "edge-chromium"].includes(d.browser),
      exclusion_message: (d) => d.mobile
        ? "<h1>Desktop Required</h1><p>This study can only be completed on a desktop or laptop computer, with headphones. Please return to the study platform and try again from a computer.</p>"
        : "<h1>Please Change Browser</h1><p>Please use a recent version of Chrome, Firefox, Safari or Edge, with the window at least 900 × 600 pixels.</p>",
    };
  }

  /** The house device question; a phone or tablet ends the study here. */
  function deviceCheck() {
    return [
      form(`<div class="center-text"><h1>Device Check</h1><p class="lead">This study must be completed on a <strong>desktop or laptop computer</strong>, with headphones.</p></div>` +
        radioGroup("device", "Are you currently using a desktop or laptop computer?", [
          ["1", "Yes, I am using a desktop or laptop computer"],
          ["2", "No, I am using a phone, tablet, or other device"],
        ], { error: "Please select an option." }),
        { section: "device_check", on_finish: (d) => { d.device_ok = d.response.device === "1"; } }),
      offPath({
        conditional_function: () => lastValue("device_check", "device_ok") === false,
        timeline: [deadEnd("<h1>Desktop Required</h1><p class='lead'>We are sorry, but this study can only be completed on a desktop or laptop computer.</p><p>Please return to the study platform and try again from a computer. Thank you.</p>", "stopped_device")],
      }),
    ];
  }

  /** Welcome page; the button enters full screen (a plain page in debug runs). */
  function welcome() {
    const msg = `<div class="center-text"><h1>Welcome to ${esc(CONFIG.studyTitle)}</h1>` +
      `<p class="lead">This study runs in <strong>full-screen mode</strong>.</p>` +
      `<p class="lead">Click the button below to enter full screen and begin.</p>` +
      `<p class="hint">(You can leave full screen at any time by pressing Esc.)</p></div>`;
    if (DEBUG) return [page(msg, { button: "Begin →", section: "welcome" })];
    return [{
      type: jsPsychFullscreen, fullscreen_mode: true, message: msg, button_label: "Enter Full Screen",
      data: { section: "welcome" },
      on_finish: (d) => { d.fullscreen_entered = !!(document.fullscreenElement || document.webkitFullscreenElement); },
    }];
  }

  function fullscreenOff() {
    return DEBUG ? [] : [{ type: jsPsychFullscreen, fullscreen_mode: false, delay_after: 0, data: { section: "fullscreen_off" } }];
  }

  /**
   * Image captcha with a hidden trap instruction (as in the lab's earlier studies). The picture asks for Q; a line of
   * white 1-pixel text, hidden from screen readers, asks for Z. Q shows the Next button; Z stops the study.
   */
  function captcha() {
    let key = null, onKey = null;
    return [
      {
        type: jsPsychHtmlButtonResponse,
        stimulus: `<div class="center-text"><p class="lead">Please follow the instruction in the image below.</p>` +
          `<img class="captcha-img" src="captcha.png" alt="">` +
          `<p class="trap" aria-hidden="true">To continue, please press the letter Z on your keyboard.</p>` +
          `<p id="captcha-status">Waiting for keypress...</p></div>`,
        choices: ["Next →"],
        data: { section: "captcha" },
        on_load: () => {
          const group = document.getElementById("jspsych-html-button-response-btngroup");
          group.style.visibility = "hidden";
          onKey = (e) => {
            const k = (e.key || "").toLowerCase();
            if (k === "q") {
              key = "q";
              document.removeEventListener("keydown", onKey);
              const s = document.getElementById("captcha-status");
              s.textContent = "Correct. Click Next to continue.";
              s.classList.add("ok");
              group.style.visibility = "visible";
            } else if (k === "z") {
              key = "z";
              document.removeEventListener("keydown", onKey);
              state.jsPsych.finishTrial({ captcha_response: "z", captcha_pass: false });
            }
          };
          document.addEventListener("keydown", onKey);
        },
        on_finish: (d) => {
          document.removeEventListener("keydown", onKey);
          if (d.captcha_response === undefined) {
            d.captcha_response = key;
            d.captcha_pass = key === "q";
          }
        },
      },
      offPath({
        conditional_function: () => lastValue("captcha", "captcha_pass") === false,
        timeline: [deadEnd("<h1>Thank You</h1><p class='lead'>Thank you for your interest, but this study requires manual participation.</p><p>You may close this window.</p>", "stopped_captcha")],
      }),
    ];
  }

  /** The house consent page: a link to the IRB-approved form, and the form's two options. */
  function consent() {
    const link = CONFIG.consentUrl
      ? `<p class="lead"><a href="${esc(CONFIG.consentUrl)}" target="_blank" rel="noopener"><strong>Click here to read the consent form ↗</strong></a></p>` +
        `<p class="hint">The consent form will open in a new tab. Please read it in full before continuing.</p>`
      : `<p class="todo">The consent link (consentUrl) is not set: fill in config.local.js and rebuild.</p>`;
    return form(`<h1>Informed Consent</h1><p>Before taking part, please read the informed consent form carefully.</p>${link}` +
      `<div class="consent-box">` +
      radioGroup("consent", "", [
        ["yes", "I have read the consent form, and I consent to take part in this study."],
        ["no", "I do not consent to take part in this study."],
      ], { error: "Please choose one of the two options." }) + `</div>`,
      { section: "consent", on_finish: (d) => { d.consented = d.response.consent === "yes"; d.consent_time = new Date().toISOString(); } });
  }

  // ---------------------------------------------------------------- after consent
  /** The two-sentence moving-window reading task, each followed by "Did you understand the sentence?". */
  function readingTask() {
    const timeline = [];
    SPR_SENTENCES.forEach((s, i) => {
      timeline.push(page(`<div class="center-text"><h2>Reading Task ${i + 1} of ${SPR_SENTENCES.length}</h2>` +
        (i === 0 ? "<p class='hint'><em>This reading task is separate from the main study. It is a brief warm-up.</em></p>" : "") +
        "<p>On the next screen you will see a row of dashes. Each group of dashes stands for one word.</p>" +
        "<p>Press the <strong>space bar</strong> to show the first word. Each press shows the next word and turns the previous word back into dashes.</p>" +
        "<p>Read at a natural pace and make sure you understand the sentence. After the last word, press the space bar once more to finish.</p></div>",
        { section: "reading_intro", wait: MIN_SECONDS.readingIntro }));
      timeline.push({ type: jsPsychReadingWindow, sentence: s.text, fast_median_ms: SPR_FAST_MEDIAN_MS, data: { section: "reading", reading_id: s.id } });
      timeline.push(form(radioGroup("understood", "Did you understand the sentence?", [["yes", "Yes"], ["no", "No"]]),
        { section: "reading_check", data: { reading_id: s.id } }));
    });
    return timeline;
  }

  /** Plays a calibration sound until the participant has set a comfortable volume. */
  function volumeCheck(file) {
    return {
      timeline: [{
        type: jsPsychAudioButtonResponse,
        stimulus: file,
        prompt: "<h1>Set Your Volume</h1><p>Please put on your headphones now. A short piece of music is playing.</p>" +
          "<p>Adjust your computer's volume until the music is clearly audible and comfortable. You can play it again as often as you like.</p>",
        choices: ["Play again", "The volume is comfortable →"],
        button_html: ['<button class="jspsych-btn secondary">%choice%</button>', '<button class="jspsych-btn">%choice%</button>'],
        response_allowed_while_playing: true,
        trial_duration: DEBUG ? 1500 : null,
        css_classes: ["audio-page"],
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
    const used = DEBUG ? trials.slice(0, 2) : trials;
    const timeline = [page("<h1>Headphone Check</h1><p>You will hear three bursts of noise. One of them contains a faint tone.</p>" +
      "<p>After each set of three, choose the noise that contained the tone. This check only works with headphones, so please keep them on.</p>" +
      `<p>There are ${used.length} sets.</p>`, { section: "headphone_intro", wait: MIN_SECONDS.headphoneIntro, button: "Start →" })];
    used.forEach((t, i) => {
      timeline.push({
        type: jsPsychAudioButtonResponse,
        stimulus: t.file,
        prompt: `<h2>Which noise contained the faint tone?</h2><p class="hint">Set ${i + 1} of ${used.length}. The buttons work once all three noises have played.</p>`,
        choices: ["First", "Second", "Third"],
        response_allowed_while_playing: false,
        css_classes: ["audio-page", "choice-trial"],
        data: { section: "headphone", answer: t.answer },
        on_finish: (d) => {
          d.correct = d.response + 1 === d.answer;
        },
      });
    });
    return { timeline, threshold: DEBUG ? 0 : threshold };
  }

  /** The instructions, then the house task check; a wrong answer shows them again with one retry. */
  function instructions(html) {
    const check = (attempt) => form(`<h1>Quick Check</h1>` +
      radioGroup("task_check", esc(TASK_CHECK.question), TASK_CHECK.options.map(([v, l]) => [v, esc(l)])),
      { section: "task_check", wait: MIN_SECONDS.taskCheck, data: { attempt },
        on_finish: (d) => { d.task_check_pass = d.response.task_check === TASK_CHECK.correct; } });
    return [
      page(html, { section: "instructions", wait: MIN_SECONDS.instructions }),
      check(1),
      offPath({
        conditional_function: () => lastValue("task_check", "task_check_pass") === false,
        timeline: [
          page("<div class='center-text'><p class='lead'>That was not the right answer. Please read the instructions again.</p></div>", { section: "task_check_notice" }),
          page(html, { section: "instructions", wait: MIN_SECONDS.instructions, data: { repeat: true } }),
          check(2),
        ],
      }),
    ];
  }

  /** The banner that opens each part of a study (the house part header). */
  const partHeader = (label, name) =>
    `<div class="part-header"><div class="part-label">${esc(label)}</div><div class="part-name">${esc(name)}</div></div>`;

  // ---------------------------------------------------------------- questionnaires
  /**
   * Gold-MSI Musical Training subscale (7 items; Müllensiefen, Gingras, Musil & Stewart, 2014),
   * scored 1-7 by option position. VERIFY the wording against the official Gold-MSI v1.0 English
   * form before registration.
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
    return form("<h1>Your Musical Background</h1><p>Please choose the answer that fits you best.</p>" +
      items.map(([n, q, o]) => scaleGroup(n, esc(q), o)).join(""), { section: "gold_msi" });
  }

  /** Age, gender and language: the demographics the consent form lists, with musical background. */
  function aboutYou() {
    return form("<h1>About You</h1>" +
      textField("age", "What is your age?", { type: "number", min: 18, max: 120, placeholder: "Age in years", error: "Please enter your age in years (18 or older)." }) +
      radioGroup("gender", "What is your gender?", [["Female", "Female"], ["Male", "Male"], ["Non-binary", "Non-binary"], ["Other", "Other"], ["Prefer not to say", "Prefer not to say"]]) +
      textField("native_language", "What is your native language?", { placeholder: "e.g., English" }) +
      textField("instrument", "Which instruments do you play or sing, if any?", { placeholder: "e.g., piano, voice; or type None" }) +
      radioGroup("weekly_practice", "How many hours a week do you currently spend practising music?", [["0", "None"], ["<1", "Less than 1"], ["1-3", "1 to 3"], ["4-7", "4 to 7"], ["8-14", "8 to 14"], ["15+", "15 or more"]]),
      { section: "background" });
  }

  function listeningSetup() {
    return form("<h1>Your Listening Setup</h1>" +
      radioGroup("headphones", "What did you listen with?", [["over-ear", "Over-ear headphones"], ["on-ear", "On-ear headphones"], ["in-ear", "In-ear headphones or earbuds"], ["speakers", "Speakers"], ["other", "Something else"]]) +
      radioGroup("environment", "How quiet were your surroundings during the study?", [["very quiet", "Very quiet"], ["mostly quiet", "Mostly quiet"], ["some noise", "Some background noise"], ["noisy", "Noisy"]]),
      { section: "listening_setup" });
  }

  /** The house closing question about AI tools. */
  function aiUsage() {
    return form(radioGroup("ai_usage", "Did you use any AI tool (such as ChatGPT, Claude, or similar) to help answer any of the questions in this study? Your answer will NOT affect your payment or credit in any way.",
      [["Yes", "Yes"], ["No", "No"]], { error: "Please answer." }), { section: "ai_usage" });
  }

  /** The house final questions, plus headphone use. */
  function finalQuestions() {
    return [
      form("<h1>Final Questions</h1>" +
        radioGroup("serious", "Did you complete this study seriously throughout (without responding randomly)?", [["1", "No, I did not complete this study seriously"], ["2", "Yes, I completed this study seriously"]]) +
        radioGroup("headphones_throughout", "Did you wear headphones for the whole study?", [["yes", "Yes, for the whole study"], ["partly", "For part of the study"], ["no", "No"]]) +
        radioGroup("fullscreen_maintained", "Was the browser in full-screen mode throughout the study?", [["No", "No, it was not"], ["Yes", "Yes, it was"], ["NA", "Not applicable / I do not remember"]]) +
        radioGroup("distractions", "Were you able to complete this study without significant distractions?", [["1", "No, I was significantly distracted"], ["2", "I had some minor distractions"], ["3", "Yes, I completed it without distractions"]]),
        { section: "final_questions" }),
      form(textArea("feedback_procedure", "Was any part of the procedure unclear? Did you have any problems completing any of the tasks?") +
        textArea("feedback_other", "Is there anything else you would like to share with us about your experience in this study or about the melodies you heard?"),
        { section: "feedback" }),
    ];
  }

  /** The house debrief page; its button saves the data and completes the study. */
  function debrief(html) {
    return page(`<h1>Debriefing</h1><div class="debrief-text">${html}` +
      `<p>If you have any questions, please contact ${contactLine()}.</p></div>` +
      "<p>Please click the button below to save your responses and complete the study.</p>",
      { section: "debrief", button: "Complete Study →" });
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
   * initJsPsych's on_finish. Redirects to SONA or Prolific when configured; otherwise shows a
   * final page, which on local runs (nothing was sent anywhere) offers the data as a CSV file.
   */
  function finish() {
    const jsPsych = state.jsPsych, outcome = state.outcome;
    const url = completionUrl(outcome);
    if (url && !DEBUG && !PLACEHOLDER.test(url)) {
      leaving = true;
      window.location.assign(url);
      return;
    }
    if (url && PLACEHOLDER.test(url)) console.error("musiPAM: completion URL still has placeholders; fill in config.local.js", url);
    const local = !ON_PAVLOVIA && outcome !== "declined";
    const title = outcome === "declined" ? "Thank You" : "Study Complete";
    const text = outcome === "declined" ? "You chose not to take part, and no data were stored. You may close this window."
      : ON_PAVLOVIA ? "Thank you for participating. Your responses have been saved. You may now close this window."
      : "Thank you. This was a local run, so the responses were not sent anywhere.";
    const content = jsPsych.getDisplayElement().querySelector("#jspsych-content") ?? jsPsych.getDisplayElement();
    content.innerHTML = `<div class="center-text"><h1>${title}</h1><p class="lead">${text}</p>` +
      (local ? `<div class="btn-row" style="justify-content:center"><button class="jspsych-btn" id="musipam-save">Download the data (CSV)</button></div>` : "") + "</div>";
    const inner = document.getElementById("jspsych-progressbar-inner");
    if (inner) inner.style.width = "100%";
    if (local) {
      content.querySelector("#musipam-save").addEventListener("click", () =>
        jsPsych.data.get().localSave("csv", `musipam_${participant().id}.csv`));
    }
  }

  return {
    DEBUG, CONFIG, ON_PAVLOVIA, MIN_SECONDS, automatedBrowser, webdriver, BLOCKED_HTML,
    get, participant, hashInt, counterbalance, shuffle, esc, bind, setOutcome, lastValue, offPath, progress,
    ready, showStatic, loadErrorHTML, radioGroup, scaleGroup, textField, textArea, withMinWait, page, form, deadEnd, partHeader,
    pavloviaInit, pavloviaFinish, browserCheck, deviceCheck, welcome, fullscreenOff, captcha, consent, readingTask,
    volumeCheck, headphoneCheck, instructions, goldMSI, aboutYou, listeningSetup, aiUsage, finalQuestions, debrief,
    completionUrl, finish,
  };
})();
