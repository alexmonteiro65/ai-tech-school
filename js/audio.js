/* Shared audio-narration engine, used by per-lesson audio sections.

   Pattern: same as js/video.js but simpler — no avatar, just a narrated
   voice reading the lesson script, hosted right in this repo (a 2-4
   minute MP3 is small enough that there's no reason to reach for
   YouTube/Vimeo the way the video pipeline does). Renders a plain HTML5
   <audio> player. Leave a language's url empty and a "coming soon"
   placeholder renders instead, so the page never breaks waiting on the
   recording.

   Where the MP3s come from: Piper, a free, open-source, offline neural
   TTS engine (MIT-licensed, no account, no API key — this is NOT the
   "no paid/generative third-party API" case in CLAUDE.md section 2,
   which is about billed, key-authenticated APIs like Runway/HeyGen).
   scripts/generate_narration.py reads the scripts in video/*-script.md
   and synthesizes them with Piper inside
   .github/workflows/generate-narration.yml — the same GitHub-Actions-as-
   backend pattern as the AI News and Instagram pipelines, needed only
   because the Piper voice models themselves are fetched from Hugging
   Face, which this project's own dev sandbox can't reach but Actions
   runners can. See claude/change-plan-sept1.md section 4 for the voice
   choices. Nothing here calls a generative API from the live site or a
   visitor's browser — only the finished, hosted MP3 is referenced.

   (Fixed 2026-09-02: scripts/generate_narration.py writes each lesson's
   MP3 path as "audio/lessons/<lesson>-<lang>.mp3" — correct only when
   resolved from the site root. Every lesson page patched with that path
   lives two folders deep, at levels/<path>/lesson-N.html, so the browser
   was resolving it as levels/<path>/audio/lessons/... and 404ing — the
   narration never played on any lesson page. resolveMediaUrl() below
   fixes this the same way js/video.js does, by resolving a site-root-
   relative path against wherever this script itself was actually loaded
   from, so the already-patched pages needed no changes at all.) */
window.ATS = window.ATS || {};

(function (ATS) {
  "use strict";

  /* This script is loaded from a different relative depth depending on
     the page ("js/audio.js" at the site root, "../../js/audio.js" from
     levels/<path>/...) — find our own <script> tag and reuse whatever
     prefix it was loaded with, so a single site-root-relative MP3 path
     resolves correctly no matter how deep the calling page lives. */
  function computeSitePrefix(scriptFileName) {
    var scripts = document.getElementsByTagName("script");
    for (var i = 0; i < scripts.length; i++) {
      var src = scripts[i].getAttribute("src");
      if (!src) continue;
      var clean = src.split("?")[0].split("#")[0];
      if (clean.slice(-scriptFileName.length) === scriptFileName) {
        return clean.slice(0, clean.length - scriptFileName.length);
      }
    }
    return "";
  }

  var SITE_PREFIX = computeSitePrefix("js/audio.js");

  function resolveMediaUrl(path) {
    if (!path) return path;
    if (/^([a-z][a-z0-9+.-]*:)?\/\//i.test(path) || path.charAt(0) === "/") return path;
    return SITE_PREFIX + path;
  }

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
    var url = resolveMediaUrl(urls[lang] || urls.en);

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
