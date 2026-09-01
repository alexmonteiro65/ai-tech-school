/* Shared audio-narration engine, used by per-lesson audio sections.

   Pattern: same as js/video.js but simpler — no avatar, just a real human
   voice narrating the lesson script, hosted right in this repo (a 3-5
   minute MP3 is small enough that there's no reason to reach for
   YouTube/Vimeo the way the video pipeline does). Renders a plain HTML5
   <audio> player. Leave a language's url empty and a "coming soon"
   placeholder renders instead, so the page never breaks waiting on the
   recording. See CLAUDE.md section 2 for why this project doesn't call a
   generative voice API directly — the audio is recorded/produced outside
   this codebase (the founder's own voice, or a free tool the user runs
   himself) and only the finished, hosted file is referenced here. */
window.ATS = window.ATS || {};

(function (ATS) {
  "use strict";

  var DEFAULT_PLACEHOLDER_TEXT = {
    en: "The narrated audio for this lesson is in production — check back soon.",
    pt: "O áudio narrado desta aula está em produção — volte em breve.",
    es: "El audio narrado de esta lección está en producción — vuelve pronto."
  };

  var DEFAULT_LISTEN_LABEL = {
    en: "Listen to this lesson",
    pt: "Ouça esta aula",
    es: "Escucha esta lección"
  };

  /* config: {
       urls: { en, pt, es },   // path to an MP3 in this repo, empty = no audio yet
       duration: "~4 min",     // optional label
       label: { en, pt, es },  // optional override for the player's heading
       placeholderText: { en, pt, es }
     } */
  function create(containerSelector, config, lang) {
    var container = document.querySelector(containerSelector);
    if (!container) return;

    config = config || {};
    var urls = config.urls || {};
    var url = urls[lang] || urls.en;

    if (!url) {
      var placeholderMap = config.placeholderText || DEFAULT_PLACEHOLDER_TEXT;
      var text = placeholderMap[lang] || placeholderMap.en;
      container.innerHTML =
        '<div class="video-placeholder">' +
        '<svg class="icon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 18V5l12-2v13M9 18a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm12-2a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>' +
        "<p>" + text + "</p></div>";
      return;
    }

    var label = (config.label && (config.label[lang] || config.label.en)) || (DEFAULT_LISTEN_LABEL[lang] || DEFAULT_LISTEN_LABEL.en);
    var durationHtml = config.duration ? '<span class="ats-audio-duration">' + config.duration + "</span>" : "";

    container.innerHTML =
      '<div class="ats-audio-player">' +
      '<div class="ats-audio-player-label"><span>' + label + "</span>" + durationHtml + "</div>" +
      '<audio controls preload="none" style="width:100%;">' +
      '<source src="' + url + '" type="audio/mpeg">' +
      "</audio>" +
      "</div>";
  }

  ATS.audio = { create: create };
})(window.ATS);
