/* Shared video-embed engine, used by the dedicated video page, each level
   hub's course-intro video slot, and per-lesson video sections.

   Pattern: the actual file stays hosted for free on YouTube/Vimeo
   (unlisted, not "public search" listed) — that's what keeps this a static
   site with zero hosting/bandwidth cost — but the LEARNER never leaves
   ai-tech-school.github.io. A branded poster card opens a full in-page
   overlay player (ATS dark theme, ATS chrome, close button, Escape to
   close). No redirect, no new tab, no youtube.com address bar. See
   CLAUDE.md section 1/2 for why this project never calls a paid
   video-generation API directly — the video is produced externally and
   only its finished, hosted URL is configured here.

   VIDEO_EMBED_URLS / any config passed to ATS.video.create must be a
   standard *player embed* URL:
     YouTube: https://www.youtube-nocookie.com/embed/<id>
     Vimeo:   https://player.vimeo.com/video/<id>
   not a normal watch-page URL. Leave a language empty and a "coming soon"
   placeholder renders instead, so the site never breaks waiting on video
   production. */
window.ATS = window.ATS || {};

(function (ATS) {
  "use strict";

  var DEFAULT_PLACEHOLDER_TEXT = {
    en: "This video is in production — check back soon.",
    pt: "Este vídeo está em produção — volte em breve.",
    es: "Este video está en producción — vuelve pronto."
  };

  var DEFAULT_WATCH_LABEL = { en: "Watch video", pt: "Assistir vídeo", es: "Ver video" };

  var overlayEl = null;
  var overlayIframe = null;
  var lastFocusedEl = null;

  function ensureOverlay() {
    if (overlayEl) return overlayEl;

    overlayEl = document.createElement("div");
    overlayEl.className = "ats-video-overlay";
    overlayEl.setAttribute("role", "dialog");
    overlayEl.setAttribute("aria-modal", "true");
    overlayEl.hidden = true;
    overlayEl.innerHTML =
      '<div class="ats-video-overlay-backdrop" data-video-close></div>' +
      '<div class="ats-video-overlay-panel">' +
      '<button type="button" class="ats-video-overlay-close" data-video-close aria-label="Close video">' +
      '<svg class="icon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>' +
      "</button>" +
      '<div class="ats-video-overlay-frame-wrap">' +
      '<iframe class="ats-video-overlay-iframe" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>' +
      "</div>" +
      "</div>";
    document.body.appendChild(overlayEl);
    overlayIframe = overlayEl.querySelector(".ats-video-overlay-iframe");

    overlayEl.addEventListener("click", function (e) {
      if (e.target && e.target.hasAttribute("data-video-close")) closeOverlay();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && overlayEl && !overlayEl.hidden) closeOverlay();
    });

    return overlayEl;
  }

  function openOverlay(url, title) {
    ensureOverlay();
    lastFocusedEl = document.activeElement;
    overlayEl.querySelector(".ats-video-overlay-frame-wrap").setAttribute("aria-label", title || "Video");
    overlayIframe.src = url + (url.indexOf("?") > -1 ? "&" : "?") + "autoplay=1&rel=0";
    overlayEl.hidden = false;
    document.body.classList.add("ats-video-open");
    overlayEl.querySelector(".ats-video-overlay-close").focus();
  }

  function closeOverlay() {
    if (!overlayEl) return;
    overlayEl.hidden = true;
    overlayIframe.src = "about:blank";
    document.body.classList.remove("ats-video-open");
    if (lastFocusedEl && typeof lastFocusedEl.focus === "function") lastFocusedEl.focus();
  }

  /* Renders a poster card that launches the overlay player on click.
     config: {
       urls: { en, pt, es },        // player-embed URLs, empty = no video yet
       poster: "path/to/image.jpg", // optional; falls back to a gradient tile
       duration: "~3 min",          // optional label on the poster
       title: { en, pt, es },       // optional accessible title / overlay label
       placeholderText: { en, pt, es } // optional override for "coming soon" copy
     } */
  function create(containerSelector, config, lang) {
    var container = document.querySelector(containerSelector);
    if (!container) return;

    config = config || {};
    var urls = config.urls || {};
    var url = urls[lang] || urls.en;
    var title = (config.title && (config.title[lang] || config.title.en)) || "Video";

    if (!url) {
      var placeholderMap = config.placeholderText || DEFAULT_PLACEHOLDER_TEXT;
      var text = placeholderMap[lang] || placeholderMap.en;
      container.innerHTML =
        '<div class="video-placeholder">' +
        '<svg class="icon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 7 16 12 9 17Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/></svg>' +
        "<p>" + text + "</p></div>";
      return;
    }

    var watchLabel = DEFAULT_WATCH_LABEL[lang] || DEFAULT_WATCH_LABEL.en;
    var posterStyle = config.poster
      ? 'style="background-image:url(' + config.poster + ')"'
      : "";
    var durationHtml = config.duration
      ? '<span class="ats-video-poster-duration">' + config.duration + "</span>"
      : "";

    container.innerHTML =
      '<button type="button" class="ats-video-poster" ' + posterStyle + ' aria-label="' + watchLabel + ': ' + title + '">' +
      '<span class="ats-video-poster-play" aria-hidden="true">' +
      '<svg class="icon" viewBox="0 0 24 24" fill="none"><path d="M9 7 16 12 9 17Z" fill="currentColor"/></svg>' +
      "</span>" +
      '<span class="ats-video-poster-label">' + watchLabel + "</span>" +
      durationHtml +
      "</button>";

    container.querySelector(".ats-video-poster").addEventListener("click", function () {
      openOverlay(url, title);
    });
  }

  /* Backward-compatible helper for the existing "AI Universe" video page,
     which calls ATS.video.renderInto("#video-container", lang) directly. */
  var AI_UNIVERSE_CONFIG = {
    urls: { en: "video/ai-universe-en.mp4", pt: "video/ai-universe-pt.mp4", es: "video/ai-universe-es.mp4" },
    title: { en: "The AI Universe", pt: "O Universo da IA", es: "El Universo de la IA" },
    duration: "~2 min"
  };

  function renderInto(containerSelector, lang) {
    create(containerSelector, AI_UNIVERSE_CONFIG, lang);
  }

  function hasVideo(lang, config) {
    var urls = (config && config.urls) || AI_UNIVERSE_CONFIG.urls;
    return !!(urls[lang] || urls.en);
  }

  ATS.video = {
    create: create,
    renderInto: renderInto,
    hasVideo: hasVideo,
    AI_UNIVERSE_CONFIG: AI_UNIVERSE_CONFIG
  };
})(window.ATS);
