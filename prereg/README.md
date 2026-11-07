# musiPAM preregistrations (drafts)

Each file follows the field structure of the **OSF Preregistration** template (Study Information → Design Plan → Sampling Plan → Variables → Analysis Plan → Other), so each section pastes directly into the OSF form.

| File | Study | Status |
|---|---|---|
| [S0_norming.md](S0_norming.md) | 0 · Stimulus norming | draft |
| [S1a_perceived_derivation.md](S1a_perceived_derivation.md) | 1a · Perceived derivation | draft |
| [S1b_motif_similarity.md](S1b_motif_similarity.md) | 1b · Motif similarity | draft |
| [S1c_relation_similarity.md](S1c_relation_similarity.md) | 1c · Relation similarity | draft |
| [S2_theme_variation_mapping.md](S2_theme_variation_mapping.md) | 2 · Theme ↔ variation mapping | draft |
| [S3_cross_theme_mapping.md](S3_cross_theme_mapping.md) | 3 · Cross-theme mapping | draft |

## Rules for finalizing a draft

1. **Freeze the stimuli.** Tag a release of the stimulus set in the GitHub repository; Zenodo mints a DOI. The preregistration cites that DOI and the commit hash. No stimulus changes after registration.
2. **Freeze the model predictions.** Every similarity value used in a confirmatory model test is computed from the frozen release and saved as a CSV with its SHA-256 hash in the registration (`predictions/`). The models are then predicting data that doesn't exist yet.
3. **Set N by simulation.** Replace the provisional N with a simulation-based power analysis (`simr` or `mixedpower`) using Study 0 / pilot variance estimates. Keep the simulation script with the registration.
4. **Resolve every DECISION.** None may remain at registration.
5. **Register on OSF immediately before data collection.** Deviations are reported in the paper as deviations.

## Shared methods (identical in every study unless stated)

- **Platform.** jsPsych on Pavlovia. Each study is its own Pavlovia project, which is its own GitLab repository on gitlab.pavlovia.org. That gives every study its own data folder, piloting/running status, session credits and SONA link, and lets its code be frozen at its registration while later studies are still in development. All six projects are built from one shared codebase in this repository (`experiments/`: consent, headphone screen, Gold-MSI, audio player, data saving), so the shared parts are identical across studies.
- **Headphone screen.** Huggins-pitch test (Milne et al., 2021), 6 trials, pass ≥ 5. Participants who fail end the session and are not counted toward N.
- **Musical background.** Gold-MSI Musical Training subscale (7 items; Müllensiefen et al., 2014), plus years of formal training and current weekly practice.
- **Common exclusions.**
  - failed catch trials (study-specific thresholds);
  - answering "no" to "Did you complete this study seriously? (Your answer will not affect your credit.)";
  - completion time under 50% of the median;
  - a repeat participation (only the first session is kept);
  - audio playback failures on more than 10% of trials.

  Excluded participants are replaced until the target N is reached.
- **Analysis software.** R ≥ 4.4 (`lme4`, `ordinal`, `emmeans`, `simr`). Model similarities are computed in Python by the `stimgen` generator at the frozen commit; PAM uses the Lu lab implementation.
- **Random effects.** The maximal structure justified by the design (Barr et al., 2013). If a model fails to converge, drop the random-effect correlations, then remove the random slope with the smallest variance, one at a time, until it converges.
- **Inference.** α = .05, two-sided, with Holm correction within each study's family of confirmatory tests.
