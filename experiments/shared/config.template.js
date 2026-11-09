/*
 * Study-specific settings. Copy this file to <study>/config.local.js (e.g. study0/config.local.js),
 * fill in the values from that study's SONA and Prolific pages, and rebuild. config.local.js
 * is gitignored: the SONA credit token lets anyone grant credit, so it must stay out of the
 * public repository. It belongs only in the deployed copy (the study's private Pavlovia project).
 *
 * While a value still has its placeholder (EXPERIMENT_ID, CREDIT_TOKEN, COMPLETION_CODE,
 * SCREENOUT_CODE), the experiment never redirects there: it shows a final page instead.
 */
window.MUSIPAM_CONFIG = {
  // SONA: Study Information page -> "Website" -> the client-side completion URL. Keep the
  // trailing "survey_code=": the experiment appends the participant's code.
  sonaCreditUrl: "https://ucla.sona-systems.com/webstudy_credit.aspx?experiment_id=EXPERIMENT_ID&credit_token=CREDIT_TOKEN&survey_code=",
  // Prolific: the study's completion codes (one for finishers, one for headphone-screen failures).
  prolificCompletionUrl: "https://app.prolific.com/submissions/complete?cc=COMPLETION_CODE",
  prolificScreenoutUrl: "https://app.prolific.com/submissions/complete?cc=SCREENOUT_CODE",
  // Shown on the consent page. Use the address in the IRB-approved consent form.
  contactEmail: "[contact email from the IRB-approved consent]",
};
