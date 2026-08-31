/* Shared language-switching engine. Each page defines its own translation
   dictionary (static strings via data-i18n / data-i18n-html /
   data-i18n-placeholder attributes, plus any dynamically-rendered exercise
   or quiz data) and calls ATS.i18n.init(dict, onLanguageChange).
   See CLAUDE.md section 8. */
window.ATS = window.ATS || {};

(function (ATS) {
  "use strict";

  var STORAGE_KEY = "ats_lang_v1";
  var SUPPORTED = ["en", "pt", "es"];
  var DEFAULT_LANG = "en";
  var HTML_LANG = { en: "en", pt: "pt-BR", es: "es" };

  function readLanguage() {
    try {
      var stored = window.localStorage.getItem(STORAGE_KEY);
      if (stored && SUPPORTED.indexOf(stored) !== -1) return stored;
    } catch (e) {
      /* storage unavailable — fall back to default */
    }
    return DEFAULT_LANG;
  }

  function writeLanguage(lang) {
    try {
      window.localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {
      /* storage unavailable — language just won't persist this session */
    }
  }

  var currentDict = null;
  var currentLang = DEFAULT_LANG;
  var changeCallbacks = [];

  function applyStaticText(lang) {
    if (!currentDict) return;
    var strings = currentDict[lang] || currentDict[DEFAULT_LANG];

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (strings[key] !== undefined) {
        el.textContent = strings[key];
      }
    });

    document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-html");
      if (strings[key] !== undefined) {
        el.innerHTML = strings[key];
      }
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-placeholder");
      if (strings[key] !== undefined) {
        el.setAttribute("placeholder", strings[key]);
      }
    });
  }

  function highlightSwitcher(lang) {
    document.querySelectorAll("[data-lang-btn]").forEach(function (btn) {
      var isActive = btn.getAttribute("data-lang-btn") === lang;
      btn.classList.toggle("is-active", isActive);
      btn.setAttribute("aria-pressed", String(isActive));
    });
    document.documentElement.setAttribute("lang", HTML_LANG[lang] || "en");
  }

  function applyLanguage(lang) {
    currentLang = lang;
    applyStaticText(lang);
    highlightSwitcher(lang);
    changeCallbacks.forEach(function (cb) {
      cb(lang);
    });
  }

  function setLanguage(lang) {
    if (SUPPORTED.indexOf(lang) === -1) return;
    writeLanguage(lang);
    applyLanguage(lang);
  }

  function getLanguage() {
    return currentLang;
  }

  /* dict: { en: {key: text}, pt: {...}, es: {...} } — for data-i18n* elements.
     onLanguageChange(lang): optional, called on init and every switch — used
     by lesson pages to rebuild JS-rendered exercises/quizzes in the new
     language. */
  function init(dict, onLanguageChange) {
    currentDict = dict;
    if (typeof onLanguageChange === "function") {
      changeCallbacks.push(onLanguageChange);
    }

    document.querySelectorAll("[data-lang-btn]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        setLanguage(btn.getAttribute("data-lang-btn"));
      });
    });

    applyLanguage(readLanguage());
  }

  ATS.i18n = {
    init: init,
    setLanguage: setLanguage,
    getLanguage: getLanguage,
    SUPPORTED: SUPPORTED
  };
})(window.ATS);
