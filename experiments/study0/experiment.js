/*
 * musiPAM Study 0: stimulus norming. Familiarity, naturalness and segmentation of every
 * theme and of four well-known anchor melodies, in three blocks whose order is
 * counterbalanced (Latin square). Design and analysis: prereg/S0_norming.md.
 */
(async function main() {
  "use strict";
  const S = await (await fetch("stimuli.json", { cache: "no-store" })).json();
  const P = MusiPAM.participant();
  const DEBUG = MusiPAM.DEBUG;
  const AUDIO_MS = DEBUG ? 1500 : null;
  const SAFETY_S = 5; // a listening trial whose audio never ends is stopped this long after it should have

  // Block orders: the preregistered Latin square. (See the DECISION in prereg/S0_norming.md
  // on running familiarity first, before any melody has been heard in the session.)
  const ORDERS = [
    ["familiarity", "naturalness", "segmentation"],
    ["naturalness", "segmentation", "familiarity"],
    ["segmentation", "familiarity", "naturalness"],
  ];
  const orderIndex = MusiPAM.counterbalance(P.id, ORDERS.length);
  const order = ORDERS[orderIndex];
  let outcome = "completed"; // or "declined" / "screened_out"; decides where the participant goes at the end

  const jsPsych = initJsPsych({
    show_progress_bar: true,
    auto_update_progress_bar: true,
    message_progress_bar: "Progress",
    on_finish: () => MusiPAM.finish(jsPsych, outcome),
  });
  jsPsych.data.addProperties({
    study: "S0", stimulus_set: S.version, participant_id: P.id, source: P.src, group: P.group,
    block_order: order.join(">"), order_index: orderIndex, debug: DEBUG,
  });
  if (DEBUG) window.jsPsych = jsPsych; // debug runs only: inspect the data from the console


  // A debug run uses one theme and one anchor.
  const items = DEBUG
    ? [S.items.find((x) => x.kind === "theme"), S.items.find((x) => x.kind === "anchor")].filter(Boolean)
    : S.items;
  const practice = S.practice;
  const info = (it) => (it ? { item: it.id, kind: it.kind, theme: it.theme ?? null } : { item: null });

  // ------------------------------------------------------------------ trial builders
  const listen = (it, section, note) => {
    let t0 = 0;
    return {
      type: jsPsychAudioKeyboardResponse,
      stimulus: it.file,
      prompt: `<p class="listening"><span class="icon"></span>${note ?? "Listen to the whole melody."}</p>`,
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

  const form = (it, section, html, extra = {}) => ({
    type: jsPsychSurveyHtmlForm,
    html: `<div class="page form">${html}</div>`,
    button_label: "Next",
    data: { section, phase: "rate", ...info(it), ...extra },
  });

  // "before today": in two of the three block orders, familiarity comes after other blocks
  // in which every melody has already been heard.
  const famQs = () =>
    MusiPAM.choice("recognized", "Had you heard this melody before today?", [["yes", "Yes"], ["no", "No"], ["unsure", "Not sure"]]) +
    MusiPAM.scale7("familiarity", "Before today, how familiar was this melody to you?", "not at all familiar", "very familiar");

  const natQs = () =>
    MusiPAM.scale7("naturalness", "How natural does this sound as a piece of music?", "not at all natural", "completely natural") +
    MusiPAM.scale7("liking", "How much do you like it?", "not at all", "very much");

  const tap = (it, section, phase = "tap") => ({
    type: jsPsychAudioTap,
    stimulus: it.file,
    prompt: "<p class='listening'><span class='icon'></span>Press <kbd>Space</kbd> each time a new musical idea begins.</p>",
    max_duration: AUDIO_MS,
    safety_s: SAFETY_S,
    data: { section, phase, ...info(it) },
  });

  const page = (html, button = "Continue", section = "instructions") => ({
    type: jsPsychHtmlButtonResponse,
    stimulus: `<div class="page">${html}</div>`,
    choices: [button],
    data: { section },
  });

  const setOutcome = (value) => ({ type: jsPsychCallFunction, func: () => { outcome = value; }, data: { section: "outcome", outcome: value } });

  /**
   * An instructed-response attention check halfway through a rating block. It replays the
   * practice melody, so no rated melody is heard an extra time before it is rated.
   */
  function attentionCheck(section) {
    const html = section === "familiarity"
      ? "<p><strong>Attention check:</strong> for this melody, please answer “Not sure” and 2.</p>" + famQs()
      : "<p><strong>Attention check:</strong> for this melody, please answer 6 on both scales.</p>" + natQs();
    const rate = {
      ...form(practice, section, html, { phase: "attention_check" }),
      on_finish: (d) => {
        const r = d.response;
        d.check_passed = section === "familiarity"
          ? r.recognized === "unsure" && r.familiarity === "2"
          : r.naturalness === "6" && r.liking === "6";
      },
    };
    return practice ? [listen(practice, section), rate] : [rate];
  }

  const withCheck = (trials, section) => {
    const half = 2 * Math.floor(trials.length / 4); // between two melodies (each is listen + rate)
    return [...trials.slice(0, half), ...attentionCheck(section), ...trials.slice(half)];
  };

  // ------------------------------------------------------------------ the three blocks
  const BLOCKS = {
    familiarity: () => [
      page("<h2>Heard it before?</h2><p>After each melody, say whether you had heard it before today, and how familiar it was to you before today. Do not count hearing it earlier in this study.</p>"),
      ...(practice ? [listen(practice, "familiarity", "Practice: listen to the whole melody."), form(practice, "familiarity", famQs(), { phase: "practice" })] : []),
      ...withCheck(MusiPAM.shuffle(items).flatMap((it) => [listen(it, "familiarity"), form(it, "familiarity", famQs())]), "familiarity"),
    ],
    naturalness: () => [
      page("<h2>How natural does it sound?</h2><p>After each melody, rate how natural it sounds as a piece of music, and how much you like it. There are no right or wrong answers.</p>"),
      ...(practice ? [listen(practice, "naturalness", "Practice: listen to the whole melody."), form(practice, "naturalness", natQs(), { phase: "practice" })] : []),
      ...withCheck(MusiPAM.shuffle(items).flatMap((it) => [listen(it, "naturalness"), form(it, "naturalness", natQs())]), "naturalness"),
    ],
    segmentation: () => [
      page("<h2>Where do new ideas begin?</h2><p>You will hear each melody twice. The first time, just listen. The second time, press the <kbd>Space</kbd> bar each time you hear a new musical idea begin. There are no right or wrong answers; press whenever it feels right to you.</p>"),
      ...(practice ? [listen(practice, "segmentation", "Practice: first, just listen."), tap(practice, "segmentation", "practice"),
        page("<p>Good. In the rest of this part, do the same: listen once, then press <kbd>Space</kbd> at each new musical idea on the second listening.</p>")] : []),
      ...MusiPAM.shuffle(items).flatMap((it) => [listen(it, "segmentation", "First, just listen."), tap(it, "segmentation")]),
    ],
  };

  // ------------------------------------------------------------------ assemble
  const hp = MusiPAM.headphoneCheck(S.headphone);
  const passedHeadphones = () =>
    jsPsych.data.get().filter({ section: "headphone" }).select("correct").sum() >= hp.threshold;
  const consented = () => jsPsych.data.get().filter({ section: "consent" }).values()[0]?.consented === true;

  // Session length: four hearings of every melody (one each to rate familiarity and
  // naturalness, two to segment), about 10 s per rating page, about 8 min of set-up and questions.
  const music = items.reduce((a, x) => a + x.duration, 0) + (practice ? practice.duration : 0);
  const minutes = Math.max(5, Math.round((4 * music + 20 * items.length + 480) / 60 / 5) * 5);

  const audio = [...items.map((x) => x.file), ...(practice ? [practice.file] : []), ...S.headphone.map((x) => x.file), S.calibration];
  const timeline = [
    {
      type: jsPsychPreload, audio, message: "<p>Loading the sounds…</p>", data: { section: "preload" },
      error_message: "<div class='page'><h2>The sounds did not load</h2><p>Please check your internet connection and reload this page.</p></div>",
      show_detailed_errors: DEBUG,
    },
    MusiPAM.browserCheck(),
    MusiPAM.consent("Listening to music"),
    { conditional_function: () => !consented(), timeline: [setOutcome("declined")] },
    {
      conditional_function: consented,
      timeline: [
        ...MusiPAM.pavloviaInit(),
        ...MusiPAM.fullscreen(true),
        MusiPAM.volumeCheck(S.calibration),
        ...hp.timeline,
        {
          conditional_function: () => !passedHeadphones(),
          timeline: [
            setOutcome("screened_out"),
            page("<h2>Thank you</h2><p>This study needs headphones, and the check did not detect them, so the study ends here. Thank you for your time.</p>", "Finish", "screened_out"),
            ...MusiPAM.fullscreen(false),
            ...MusiPAM.pavloviaFinish(),
          ],
        },
        {
          conditional_function: passedHeadphones,
          timeline: [
            page(`<h2>Three parts</h2><p>You will hear the same set of melodies in three parts, each with a different question. The whole study takes about ${DEBUG ? "a minute" : `${minutes} minutes`}.</p>`),
            ...order.flatMap((b) => BLOCKS[b]()),
            MusiPAM.goldMSI(),
            MusiPAM.background(),
            MusiPAM.seriousness(),
            MusiPAM.debrief("<p>Some of the melodies you heard are well known; the others were composed for this research. Your answers show which of the new melodies sound natural and unfamiliar, and where listeners hear their musical ideas begin.</p>"),
            ...MusiPAM.fullscreen(false),
            ...MusiPAM.pavloviaFinish(),
          ],
        },
      ],
    },
  ];
  jsPsych.run(timeline);
})();
