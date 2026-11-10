/*
 * musiPAM Study 0: stimulus norming. Familiarity, naturalness and segmentation of every
 * theme and of four well-known anchor melodies, in three parts whose order is
 * counterbalanced (Latin square). Design and analysis: prereg/S0_norming.md.
 *
 * Flow (page design and the checks for automated participants follow the lab's earlier studies;
 * see shared/musipam.js):
 *   load sounds > browser check > device check > welcome + full screen > image captcha >
 *   consent (declining ends the study; nothing is stored) > [Pavlovia session opens] >
 *   reading task (2 sentences) > volume > headphone screen (failing ends the study) >
 *   instructions > task check (one retry) > the three parts > musical background >
 *   about you > listening setup > AI use > final questions > feedback > debrief > save > redirect
 */
(async function main() {
  "use strict";
  if (MusiPAM.automatedBrowser) {
    MusiPAM.showStatic(MusiPAM.BLOCKED_HTML);
    return;
  }
  let S;
  try {
    S = await (await fetch("stimuli.json", { cache: "no-store" })).json();
  } catch (e) {
    MusiPAM.showStatic(MusiPAM.loadErrorHTML("The study's files could not be loaded."));
    return;
  }
  const P = MusiPAM.participant();
  const DEBUG = MusiPAM.DEBUG;
  const AUDIO_MS = DEBUG ? 1500 : null;
  const SAFETY_S = 5; // a listening trial whose audio never ends is stopped this long after it should have

  // Part orders: the preregistered Latin square. (See the DECISION in prereg/S0_norming.md
  // on running familiarity first, before any melody has been heard in the session.)
  const ORDERS = [
    ["familiarity", "naturalness", "segmentation"],
    ["naturalness", "segmentation", "familiarity"],
    ["segmentation", "familiarity", "naturalness"],
  ];
  const orderIndex = MusiPAM.counterbalance(P.id, ORDERS.length);
  const order = ORDERS[orderIndex];

  let tick = () => {}; // set once the timeline exists (MusiPAM.progress)
  const jsPsych = initJsPsych({
    display_element: "jspsych-target",
    show_progress_bar: true,
    auto_update_progress_bar: false,
    message_progress_bar: "",
    on_trial_finish: () => tick(),
    on_finish: () => MusiPAM.finish(),
  });
  MusiPAM.bind(jsPsych);
  jsPsych.data.addProperties({
    study: "S0", stimulus_set: S.version, participant_id: P.id, source: P.src, group: P.group, is_test: P.isTest,
    block_order: order.join(">"), order_index: orderIndex, debug: DEBUG, webdriver: MusiPAM.webdriver,
  });
  if (DEBUG) window.jsPsych = jsPsych; // debug runs only: inspect the data from the console

  // A debug run uses one theme and one anchor.
  const items = DEBUG
    ? [S.items.find((x) => x.kind === "theme"), S.items.find((x) => x.kind === "anchor")].filter(Boolean)
    : S.items;
  const practice = S.practice;
  const N = items.length;
  const info = (it) => (it ? { item: it.id, kind: it.kind, theme: it.theme ?? null } : { item: null });
  const counter = (k) => `<p class="item-head">Melody ${k} of ${N}</p>`;

  // ------------------------------------------------------------------ trial builders
  const listen = (it, section, note, head = "") => {
    let t0 = 0;
    return {
      type: jsPsychAudioKeyboardResponse,
      stimulus: it.file,
      prompt: `${head}<p class="listening"><span class="icon"></span>${note ?? "Listen to the whole melody."}</p>`,
      choices: "NO_KEYS",
      trial_ends_after_audio: true,
      trial_duration: AUDIO_MS ?? Math.round((it.duration + SAFETY_S) * 1000),
      data: { section, phase: "listen", ...info(it) },
      on_start: () => {
        t0 = performance.now();
      },
      on_finish: (d) => {
        d.listen_s = Math.round(performance.now() - t0) / 1000;
        d.audio_failed = !DEBUG && d.listen_s >= it.duration + SAFETY_S - 0.5; // ended by the safety stop
      },
    };
  };

  const FAM_LABELS = ["1 = Not at all familiar", "2", "3", "4 = Moderately familiar", "5", "6", "7 = Extremely familiar"];
  const NAT_LABELS = ["1 = Not at all natural", "2", "3", "4 = Somewhat natural", "5", "6", "7 = Completely natural"];
  const LIKE_LABELS = ["1 = Not at all", "2", "3", "4 = Somewhat", "5", "6", "7 = Very much"];
  const NAT_HINT = "Does it sound like a real piece of music that someone could have composed, or does something about it sound odd, random or out of place?";

  // "Before today": in two of the three part orders, familiarity comes after parts in which
  // every melody has already been heard.
  const famQs = () =>
    MusiPAM.radioGroup("recognized", "Had you heard this melody before today?", [["yes", "Yes"], ["no", "No"], ["unsure", "Not sure"]]) +
    MusiPAM.scaleGroup("familiarity", "Before today, how familiar was this melody to you?", FAM_LABELS);

  const natQs = () =>
    MusiPAM.scaleGroup("naturalness", "How natural does this melody sound as music?", NAT_LABELS, { hint: NAT_HINT }) +
    MusiPAM.scaleGroup("liking", "How much do you like it?", LIKE_LABELS);

  const rate = (it, section, html, extra = {}) =>
    MusiPAM.form(html, { section, data: { phase: "rate", ...info(it), ...extra } });

  const tap = (it, section, phase = "tap", head = "") => ({
    type: jsPsychAudioTap,
    stimulus: it.file,
    prompt: `${head}<p class="listening"><span class="icon"></span>Press <kbd>Space</kbd> each time a new musical idea begins.</p>`,
    max_duration: AUDIO_MS,
    safety_s: SAFETY_S,
    data: { section, phase, ...info(it) },
  });

  const setOutcome = (value) => ({ type: jsPsychCallFunction, func: () => MusiPAM.setOutcome(value), data: { section: "outcome", outcome: value } });

  /**
   * An instructed-response attention check halfway through a rating part. It replays the
   * practice melody, so no rated melody is heard an extra time before it is rated.
   */
  function attentionCheck(section) {
    const html = section === "familiarity"
      ? "<p class='question-text'>Attention check: for this melody, please select “Not sure” and 2.</p>" + famQs()
      : "<p class='question-text'>Attention check: for this melody, please select 6 for both questions.</p>" + natQs();
    const check = Object.assign(rate(practice, section, html, { phase: "attention_check" }), {
      on_finish: (d) => {
        const r = d.response;
        d.check_passed = section === "familiarity"
          ? r.recognized === "unsure" && r.familiarity === "2"
          : r.naturalness === "6" && r.liking === "6";
      },
    });
    return practice ? [listen(practice, section), check] : [check];
  }

  const withCheck = (trials, section) => {
    const half = 2 * Math.floor(trials.length / 4); // between two melodies (each is listen + rate)
    return [...trials.slice(0, half), ...attentionCheck(section), ...trials.slice(half)];
  };

  // ------------------------------------------------------------------ the three parts
  const PART = { familiarity: "Familiarity", naturalness: "Naturalness", segmentation: "Musical Ideas" };
  const intro = (b, html) => MusiPAM.page(MusiPAM.partHeader(`Part ${order.indexOf(b) + 1} of ${order.length}`, PART[b]) + html,
    { section: b, data: { phase: "intro" }, wait: MusiPAM.MIN_SECONDS.partIntro });
  const again = (b) => (order.indexOf(b) > 0 ? " They are the same melodies as before, in a new order." : "");
  const practiceNote = "<p>First, a practice melody.</p>";

  const BLOCKS = {
    familiarity: () => [
      intro("familiarity", `<p>You will hear ${N} short melodies, one at a time.${again("familiarity")} After each one, you will answer two questions: whether you had heard it <strong>before today</strong>, and how familiar it was to you before today.</p>` +
        "<p>Some of the melodies are well known; others may be new to you. Do not count hearing a melody earlier in this study.</p>" +
        "<p>Please listen to each melody to the end. There are no right or wrong answers.</p>" + (practice ? practiceNote : "")),
      ...(practice ? [listen(practice, "familiarity", "Practice: listen to the whole melody."), rate(practice, "familiarity", "<p class='item-head'>Practice</p>" + famQs(), { phase: "practice" })] : []),
      ...withCheck(MusiPAM.shuffle(items).flatMap((it, k) => [listen(it, "familiarity", undefined, counter(k + 1)), rate(it, "familiarity", counter(k + 1) + famQs())]), "familiarity"),
    ],
    naturalness: () => [
      intro("naturalness", `<p>You will hear ${N} short melodies, one at a time.${again("naturalness")} After each one, you will answer two questions.</p>` +
        `<div class="instruction-box"><p><strong>How natural does it sound as music?</strong> ${NAT_HINT} Please judge the music itself, its notes and rhythms, not the sound quality of the recording. A 1 means it sounds odd or random; a 7 means it sounds completely like real music.</p>` +
        "<p style='margin:12px 0 0'><strong>How much do you like it?</strong> This is a separate question: a melody can sound natural without being one you like, and the other way round.</p></div>" +
        "<p>There are no right or wrong answers. Please use the whole scale.</p>" + (practice ? practiceNote : "")),
      ...(practice ? [listen(practice, "naturalness", "Practice: listen to the whole melody."), rate(practice, "naturalness", "<p class='item-head'>Practice</p>" + natQs(), { phase: "practice" })] : []),
      ...withCheck(MusiPAM.shuffle(items).flatMap((it, k) => [listen(it, "naturalness", undefined, counter(k + 1)), rate(it, "naturalness", counter(k + 1) + natQs())]), "naturalness"),
    ],
    segmentation: () => [
      intro("segmentation", `<p>You will hear each of ${N} short melodies twice.${again("segmentation")} The first time, just listen. The second time, press the <kbd>Space</kbd> bar each time you hear a new musical idea begin.</p>` +
        "<p>There are no right or wrong answers; press whenever it feels right to you.</p>" + (practice ? practiceNote : "")),
      ...(practice ? [listen(practice, "segmentation", "Practice: first, just listen."), tap(practice, "segmentation", "practice"),
        MusiPAM.page("<p class='lead'>Good. In the rest of this part, do the same: listen once, then press <kbd>Space</kbd> at each new musical idea on the second listening.</p>", { section: "segmentation", data: { phase: "practice_done" } })] : []),
      ...MusiPAM.shuffle(items).flatMap((it, k) => [listen(it, "segmentation", "First, just listen.", counter(k + 1)), tap(it, "segmentation", "tap", counter(k + 1))]),
    ],
  };

  // ------------------------------------------------------------------ assemble
  const hp = MusiPAM.headphoneCheck(S.headphone);
  const passedHeadphones = () =>
    jsPsych.data.get().filter({ section: "headphone" }).select("correct").sum() >= hp.threshold;
  const consented = () => MusiPAM.lastValue("consent", "consented") === true;

  // Session length: four hearings of every melody (one each to rate familiarity and
  // naturalness, two to segment), about 10 s per rating page, about 11 min of set-up,
  // checks and questions.
  const music = items.reduce((a, x) => a + x.duration, 0) + (practice ? practice.duration : 0);
  const minutes = Math.max(5, Math.round((4 * music + 20 * N + 660) / 60 / 5) * 5);

  const PART_TEXT = {
    familiarity: "Whether you had heard each melody before today, and how familiar it was to you.",
    naturalness: "How natural each melody sounds as music, and how much you like it.",
    segmentation: "You hear each melody twice and press the space bar each time a new musical idea begins.",
  };
  const overview = "<h1>Study Instructions</h1>" +
    `<p>In this study, you will listen to <strong>${N} short melodies</strong> over headphones, in three parts. Each part asks a different question about the same melodies:</p>` +
    `<div class="instruction-box">${order.map((b, i) => `<p${i ? " style='margin-top:12px'" : ""}><strong>Part ${i + 1}: ${PART[b]}.</strong> ${PART_TEXT[b]}</p>`).join("")}</div>` +
    "<p>Each part starts with a practice melody. There are no right or wrong answers.</p>" +
    "<p>A few questions will ask you to select a specific answer. Please read every question carefully.</p>" +
    "<p>At the end, you will answer a few questions about yourself and your musical background.</p>" +
    `<p>The study should take approximately <strong>${DEBUG ? "a few" : minutes} minutes</strong>.</p>`;

  const DEBRIEF = "<p>Thank you for taking part. This study asks how people hear short melodies: whether they know them, whether they sound like natural music, and where they hear one musical idea end and the next begin.</p>" +
    "<p style='margin-top:12px'>Four of the melodies are well known, such as “Ode to Joy”; the others were composed for this research. Your answers help us choose melodies for later studies of how people compare one piece of music with another.</p>" +
    "<p style='margin-top:12px'>The reading task, the headphone check and the attention checks help us make sure that answers come from attentive people listening over headphones. No deception was involved in this study.</p>";

  const audio = [...items.map((x) => x.file), ...(practice ? [practice.file] : []), ...S.headphone.map((x) => x.file), S.calibration];
  const timeline = [
    {
      type: jsPsychPreload, audio, data: { section: "preload" },
      message: "<div class='center-text'><div class='spinner' style='margin:0 auto 16px'></div><p>Loading the sounds...</p></div>",
      error_message: "<h1>The Sounds Did Not Load</h1><p>Please check your internet connection and reload this page.</p>",
      show_detailed_errors: DEBUG,
    },
    MusiPAM.browserCheck(),
    ...MusiPAM.deviceCheck(),
    ...MusiPAM.welcome(),
    ...MusiPAM.captcha(),
    MusiPAM.consent(),
    MusiPAM.offPath({ conditional_function: () => !consented(), timeline: [setOutcome("declined")] }),
    {
      conditional_function: consented,
      timeline: [
        ...MusiPAM.pavloviaInit(),
        ...MusiPAM.readingTask(),
        MusiPAM.volumeCheck(S.calibration),
        ...hp.timeline,
        MusiPAM.offPath({
          conditional_function: () => !passedHeadphones(),
          timeline: [
            setOutcome("screened_out"),
            MusiPAM.page("<h1>Thank You</h1><p class='lead'>This study needs headphones, and the check did not detect them, so the study ends here.</p><p>Thank you for your time.</p>",
              { section: "screened_out", button: "Finish →" }),
            ...MusiPAM.fullscreenOff(),
            ...MusiPAM.pavloviaFinish(),
          ],
        }),
        {
          conditional_function: passedHeadphones,
          timeline: [
            ...MusiPAM.instructions(overview),
            ...order.flatMap((b) => BLOCKS[b]()),
            MusiPAM.page("<div class='center-text'><p class='lead'>You have now completed the listening parts of the study. Please answer a few questions about yourself.</p></div>", { section: "questionnaire_intro" }),
            MusiPAM.goldMSI(),
            MusiPAM.aboutYou(),
            MusiPAM.listeningSetup(),
            MusiPAM.aiUsage(),
            ...MusiPAM.finalQuestions(),
            MusiPAM.debrief(DEBRIEF),
            ...MusiPAM.fullscreenOff(),
            ...MusiPAM.pavloviaFinish(),
          ],
        },
      ],
    },
  ];
  tick = MusiPAM.progress(timeline);
  MusiPAM.ready();
  jsPsych.run(timeline);
})();
