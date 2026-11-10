/*
 * Study-specific settings. Copy this file to <study>/config.local.js (e.g. study0/config.local.js),
 * fill in the values, and rebuild. config.local.js is gitignored: the SONA credit token lets
 * anyone grant credit, so it must stay out of the public repository. It belongs only in the
 * deployed copy, in the study's private Pavlovia project.
 *
 * While a value still has its placeholder (EXPERIMENT_ID, CREDIT_TOKEN, COMPLETION_CODE,
 * SCREENOUT_CODE), the experiment never redirects there: it shows a final page instead.
 */
window.MUSIPAM_CONFIG = {
  // Shown on the welcome page. Use the title of the SONA listing, so participants know they
  // are in the right study.
  studyTitle: "Listening to Music",
  // The IRB-approved consent form (a UCLA Box share link); the consent page links to it.
  consentUrl: "",
  // Named on the debrief and error pages; use the contact in the consent form.
  contactName: "the researchers",
  contactEmail: "",
  // SONA: Study Information page -> "Website" -> the client-side completion URL. Keep the
  // trailing "survey_code=": the experiment appends the participant's code.
  sonaCreditUrl: "https://ucla.sona-systems.com/webstudy_credit.aspx?experiment_id=EXPERIMENT_ID&credit_token=CREDIT_TOKEN&survey_code=",
  // Prolific: the study's completion codes (one for finishers, one for headphone-screen failures).
  prolificCompletionUrl: "https://app.prolific.com/submissions/complete?cc=COMPLETION_CODE",
  prolificScreenoutUrl: "https://app.prolific.com/submissions/complete?cc=SCREENOUT_CODE",
};
