/*
 * jsPsych 7 plugin "audio-tap": play an audio file and record every press of the
 * response key, timed from audio onset on the audio clock (WebAudio currentTime,
 * or HTMLAudioElement.currentTime when WebAudio is off). Used for the segmentation
 * task of musiPAM Study 0: "press the space bar each time a new musical idea begins".
 *
 * Data: taps (array of seconds from audio onset), n_taps, audio_duration, and ended_by:
 * "audio" (normal), "max_duration", or a playback failure: "timeout" (the audio never
 * finished, e.g. a suspended audio context) or "error" (it could not be played).
 */
var jsPsychAudioTap = (function (jspsych) {
  "use strict";

  const info = {
    name: "audio-tap",
    parameters: {
      /** The audio file to play. */
      stimulus: { type: jspsych.ParameterType.AUDIO, default: undefined },
      /** HTML shown while the audio plays. */
      prompt: { type: jspsych.ParameterType.HTML_STRING, default: null },
      /** Keys that count as a tap. */
      keys: { type: jspsych.ParameterType.KEYS, default: [" "] },
      /** Stop after this many ms even if the audio is longer (debugging). */
      max_duration: { type: jspsych.ParameterType.INT, default: null },
      /** End the trial this many seconds after the audio should have finished, if it has not. */
      safety_s: { type: jspsych.ParameterType.FLOAT, default: 5 },
      /** Flash a dot on every tap, so the participant sees the press registered. */
      show_flash: { type: jspsych.ParameterType.BOOL, default: true },
    },
  };

  class AudioTapPlugin {
    constructor(jsPsych) {
      this.jsPsych = jsPsych;
    }

    trial(display_element, trial) {
      const ctx = this.jsPsych.pluginAPI.audioContext();
      const taps = [];
      let source = null;
      let audio = null;
      let t0 = null;
      let duration = null;
      let listener = null;
      let timer = null;
      let ended = false;

      display_element.innerHTML =
        `<div class="tap-wrap">${trial.prompt ?? ""}` +
        `<div class="tap-dot" id="tap-dot" aria-hidden="true"></div>` +
        `<p class="tap-count" id="tap-count" aria-live="polite">Presses: 0</p></div>`;

      const now = () => (ctx !== null ? ctx.currentTime - t0 : audio.currentTime);

      const onKey = () => {
        if (ended) return;
        taps.push(Math.round(now() * 1000) / 1000);
        const count = display_element.querySelector("#tap-count");
        if (count) count.textContent = `Presses: ${taps.length}`;
        if (trial.show_flash) {
          const dot = display_element.querySelector("#tap-dot");
          if (dot) {
            dot.classList.add("on");
            setTimeout(() => dot.classList.remove("on"), 120);
          }
        }
      };

      const finish = (how) => {
        if (ended) return;
        ended = true;
        if (listener !== null) this.jsPsych.pluginAPI.cancelKeyboardResponse(listener);
        if (timer !== null) clearTimeout(timer);
        try {
          if (source !== null) source.stop();
          if (audio !== null) audio.pause();
        } catch (e) {
          /* already stopped */
        }
        display_element.innerHTML = "";
        this.jsPsych.finishTrial({
          stimulus: trial.stimulus,
          taps: taps,
          n_taps: taps.length,
          audio_duration: duration,
          ended_by: how,
          audio_failed: how === "timeout" || how === "error",
        });
      };

      this.jsPsych.pluginAPI
        .getAudioBuffer(trial.stimulus)
        .then((buffer) => {
          if (ctx !== null) {
            source = ctx.createBufferSource();
            source.buffer = buffer;
            source.connect(ctx.destination);
            duration = buffer.duration;
            source.onended = () => finish("audio");
            t0 = ctx.currentTime;
            source.start(t0);
          } else {
            audio = buffer;
            audio.currentTime = 0;
            duration = audio.duration;
            audio.addEventListener("ended", () => finish("audio"));
            audio.play();
          }
          listener = this.jsPsych.pluginAPI.getKeyboardResponse({
            callback_function: onKey,
            valid_responses: trial.keys,
            rt_method: "performance",
            persist: true,
            allow_held_key: false,
          });
          timer = trial.max_duration !== null
            ? setTimeout(() => finish("max_duration"), trial.max_duration)
            : setTimeout(() => finish("timeout"), (duration + trial.safety_s) * 1000);
        })
        .catch((err) => {
          console.error("audio-tap: could not play", trial.stimulus, err);
          finish("error");
        });
    }
  }
  AudioTapPlugin.info = info;

  return AudioTapPlugin;
})(jsPsychModule);
