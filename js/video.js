/* Shared video engine, used by the dedicated video page and each level
   hub's course-intro video slot.

   Pattern: videos are self-hosted plain MP4 files served from this site's
   own `video/` folder — NOT YouTube/Vimeo embeds. A YouTube/Vimeo iframe
   shows that platform's own logo and a "watch on YouTube/Vimeo" link
   inside the embedded player chrome, which a visitor can click to leave
   the site — exactly what this project does not want. A native <video>
   element has no such link: nothing in it can take a visitor off this
   page. A branded poster card opens a full in-page overlay player (ATS
   dark theme, ATS chrome, close button, Escape to close) playing that
   real <video>.

   (Fixed 2026-09-02: this file used to still be the pre-refactor
   YouTube/Vimeo <iframe> embed version, loading the self-hosted MP4
   inside an <iframe> with a "?autoplay=1&rel=0" suffix meant for a
   platform embed URL — the CSS for the real <video>-based overlay had
   already shipped, but this script hadn't caught up, so the iframe
   rendered at the browser's unstyled default size: a tiny, low-quality
   video box floating inside the correctly-sized dark modal. Also fixed
   here: the overlay's close button only closed when the click landed
   exactly on the <button>, not on the ✕ icon drawn inside it — which is
   most of the button's visible area — so most real clicks on "close"
   did nothing.)

   VIDEO_EMBED_URLS / any config passed to ATS.video.create must be a
   path to a self-hosted video file, relative to the SITE ROOT (e.g.
   "video/ai-universe-en.mp4"), never adjusted for how deep the calling
   page lives — resolveMediaUrl() below corrects it automatically no
   matter whether the page using it is at the site root or nested under
   levels/<path>/. Leave a language empty and a "coming soon" placeholder
   renders instead, so the site never breaks waiting on video production.
   See CLAUDE.md section 1/2 for why this project never calls a paid
   video-generation API directly — videos are produced externally (or by
   the automated pipeline) and only the finished file is referenced
   here. */
window.ATS = window.ATS || {};

(function (ATS) {
  "use strict";

  var DEFAULT_PLACEHOLDER_TEXT = {
    en: "This video is in production — check back soon.",
    pt: "Este vídeo está em produção — volte em breve.",
    es: "Este video está en producción — vuelve pronto."
  };

  var DEFAULT_WATCH_LABEL = { en: "Watch video", pt: "Assistir vídeo", es: "Ver video" };

  /* This script is loaded from a different relative depth depending on
     the page ("js/video.js" at the site root, "../../js/video.js" from
     levels/<path>/...) — find our own <script> tag and reuse whatever
     prefix it was loaded with, so a single site-root-relative media path
     resolves correctly from any page, instead of only working for
     pages that happen to sit at the site root. */
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

  var SITE_PREFIX = computeSitePrefix("js/video.js");

  function resolveMediaUrl(path) {
    if (!path) return path;
    // Already absolute (protocol, protocol-relative, or root-relative) —
    // leave it alone.
    if (/^([a-z][a-z0-9+.-]*:)?\/\//i.test(path) || path.charAt(0) === "/") return path;
    return SITE_PREFIX + path;
  }

  var overlayEl = null;
  var overlayVideo = null;
  var lastFocusedEl = null;

  function isCloseTarget(target) {
    return !!(target && target.closest && target.closest("[data-video-close]"));
  }

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
      '<video class="ats-video-overlay-video" controls playsinline preload="metadata"></video>' +
      "</div>" +
      "</div>";
    document.body.appendChild(overlayEl);
    overlayVideo = overlayEl.querySelector(".ats-video-overlay-video");

    // Use closest(), not hasAttribute() on the exact click target — the
    // close button's visible ✕ is an inner <svg>/<path>, and a click that
    // lands on the glyph (most of the button's area) would otherwise be
    // silently ignored because only the <button> itself carries
    // data-video-close.
    overlayEl.addEventListener("click", function (e) {
      if (isCloseTarget(e.target)) closeOverlay();
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
    overlayVideo.src = url;
    overlayEl.hidden = false;
    document.body.classList.add("ats-video-open");
    overlayVideo.play().catch(function () {
      /* Autoplay can be blocked by the browser; controls are visible so
         the learner can just press play themselves. */
    });
    overlayEl.querySelector(".ats-video-overlay-close").focus();
  }

  function closeOverlay() {
    if (!overlayEl) return;
    overlayEl.hidden = true;
    overlayVideo.pause();
    overlayVideo.removeAttribute("src");
    overlayVideo.load();
    document.body.classList.remove("ats-video-open");
    if (lastFocusedEl && typeof lastFocusedEl.focus === "function") lastFocusedEl.focus();
  }

  /* Renders a poster card that launches the overlay player on click.
     config: {
       urls: { en, pt, es },        // site-root-relative video paths, empty = no video yet
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
    var url = resolveMediaUrl(urls[lang] || urls.en);
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
    var posterUrl = config.poster ? resolveMediaUrl(config.poster) : null;
    var posterStyle = posterUrl ? 'style="background-image:url(' + posterUrl + ')"' : "";
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

  /* Backward-compatible helper for the existing "AI Universe" video page
     and every level hub's course-intro slot, which call
     ATS.video.renderInto("#video-container", lang) directly. Paths here
     are site-root-relative like everything else — resolveMediaUrl() (via
     create()) is what makes the same config work correctly whether the
     calling page is at the site root or nested under levels/<path>/. */
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
