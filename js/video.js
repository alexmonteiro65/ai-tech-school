/* Shared video-embed config, used by the dedicated video page and by each
   level hub's course-intro video slot. One place to fill in once the real
   videos exist — see CLAUDE.md section 1 and video/ai-universe-script.md.

   VIDEO_EMBED_URLS values must be a standard *player embed* URL (e.g. a
   YouTube "https://www.youtube.com/embed/<id>" link, or a Vimeo
   "https://player.vimeo.com/video/<id>" link) — not a normal watch-page
   URL. Leave a language empty and a "coming soon" placeholder renders
   instead, so the site never breaks waiting on video production. */
window.ATS = window.ATS || {};

(function (ATS) {
  "use strict";

  var VIDEO_EMBED_URLS = {
    en: "",
    pt: "",
    es: ""
  };

  var PLACEHOLDER_TEXT = {
    en: "The AI Universe video is in production — check back soon.",
    pt: "O vídeo O Universo da IA está em produção — volte em breve.",
    es: "El video El Universo de la IA está en producción — vuelve pronto."
  };

  function hasVideo(lang) {
    return !!VIDEO_EMBED_URLS[lang];
  }

  function renderInto(containerSelector, lang) {
    var container = document.querySelector(containerSelector);
    if (!container) return;

    var url = VIDEO_EMBED_URLS[lang] || VIDEO_EMBED_URLS.en;

    if (url) {
      container.innerHTML =
        '<div class="video-embed"><iframe src="' + url + '" title="The AI Universe" ' +
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" ' +
        'allowfullscreen loading="lazy"></iframe></div>';
    } else {
      var text = PLACEHOLDER_TEXT[lang] || PLACEHOLDER_TEXT.en;
      container.innerHTML =
        '<div class="video-placeholder">' +
        '<svg class="icon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 7 16 12 9 17Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/></svg>' +
        "<p>" + text + "</p></div>";
    }
  }

  ATS.video = {
    renderInto: renderInto,
    hasVideo: hasVideo
  };
})(window.ATS);
