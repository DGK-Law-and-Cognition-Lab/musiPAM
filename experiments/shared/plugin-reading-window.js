/*
 * jsPsych plugin: moving-window self-paced reading (Just, Carpenter & Woolley, 1982), as in the
 * lab's earlier Pavlovia studies. Every word starts as dashes; each
 * press of the space bar shows the next word and turns the previous one back into dashes. The
 * time each word stays on screen is recorded. A held key does not advance the window; its
 * repeats are counted instead. After the last word, one more press ends the sentence and a
 * Next button appears.
 *
 * Data: sentence, n_words, rts (ms per word, ";"-separated), median_rt, mean_rt, min_rt,
 * repeat_presses, fast (median below fast_median_ms: implausibly fast or automated reading).
 */
var jsPsychReadingWindow = (function (jspsych) {
  "use strict";

  const info = {
    name: "reading-window",
    parameters: {
      sentence: { type: jspsych.ParameterType.STRING, default: undefined },
      fast_median_ms: { type: jspsych.ParameterType.INT, default: 150 },
      button_label: { type: jspsych.ParameterType.STRING, default: "Next →" },
    },
  };

  class ReadingWindowPlugin {
    constructor(jsPsych) {
      this.jsPsych = jsPsych;
    }

    trial(display_element, trial) {
      const words = trial.sentence.split(" ");
      const masks = words.map((w) => "–".repeat(w.length));
      display_element.innerHTML =
        `<div class="center-text"><div id="spr-display" class="spr-display">${masks.join("  ")}</div>` +
        `<p class="hint" id="spr-hint">Press the space bar to show the first word.</p></div>` +
        `<div class="btn-row"><button class="jspsych-btn" id="spr-next" style="visibility:hidden">${trial.button_label}</button></div>`;
      const display = display_element.querySelector("#spr-display");
      const hint = display_element.querySelector("#spr-hint");
      const next = display_element.querySelector("#spr-next");
      const rts = [];
      let idx = -1, last = null, repeats = 0, done = false;

      const onKey = (e) => {
        if (e.code !== "Space" && e.key !== " ") return;
        e.preventDefault();
        if (e.repeat) { repeats++; return; }
        if (done) return;
        const now = performance.now();
        if (last !== null) rts.push(Math.round(now - last));
        last = now;
        idx++;
        if (idx < words.length) {
          display.textContent = words.map((w, i) => (i === idx ? w : masks[i])).join("  ");
          hint.textContent = idx === words.length - 1 ? "Press the space bar once more to finish." : "";
          return;
        }
        done = true;
        document.removeEventListener("keydown", onKey);
        display.textContent = "✓ Done";
        display.classList.add("done");
        hint.textContent = "";
        next.style.visibility = "visible";
      };
      document.addEventListener("keydown", onKey);

      next.addEventListener("click", () => {
        if (!done) return;
        const sorted = [...rts].sort((a, b) => a - b);
        const m = Math.floor(sorted.length / 2);
        const median = sorted.length ? (sorted.length % 2 ? sorted[m] : Math.round((sorted[m - 1] + sorted[m]) / 2)) : null;
        const data = {
          sentence: trial.sentence,
          n_words: words.length,
          rts: rts.join(";"),
          median_rt: median,
          mean_rt: rts.length ? Math.round(rts.reduce((a, b) => a + b, 0) / rts.length) : null,
          min_rt: rts.length ? Math.min(...rts) : null,
          repeat_presses: repeats,
          fast: median !== null && median < trial.fast_median_ms,
        };
        display_element.innerHTML = "";
        this.jsPsych.finishTrial(data);
      });
    }
  }
  ReadingWindowPlugin.info = info;
  return ReadingWindowPlugin;
})(jsPsychModule);
