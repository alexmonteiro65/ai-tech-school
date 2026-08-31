/* Persistent guide widget: Alex Monteiro's "AM" monogram, present on every
   page, cycling short static tips. Not a chatbot — no input, no live AI
   call, just rotating text (see CLAUDE.md section 1 on why Rita never
   became a live chat character, and why this stays the same shape). */
(function () {
  "use strict";

  var TIPS = {
    en: [
      "New here? The Beginner path takes about 35 minutes, start to finish.",
      "You can switch languages anytime — your choice is saved automatically.",
      "Every lesson ends with a badge you can look back on from the path page.",
      "Stuck on a quiz? There's no minimum score — it's there to teach, not to gate you.",
      "MCP is the standard that lets Claude connect to real tools like GitHub.",
      "An agent is just a loop: observe, think, act, repeat — with guardrails you set.",
      "This whole site is plain HTML, CSS, and JavaScript. No frameworks, no tracking."
    ],
    pt: [
      "Chegou agora? A trilha Iniciante leva cerca de 35 minutos, do início ao fim.",
      "Você pode trocar de idioma quando quiser — sua escolha é salva automaticamente.",
      "Cada aula termina com um selo que você pode rever na página da trilha.",
      "Travou em um quiz? Não existe nota mínima — ele serve para ensinar, não para barrar você.",
      "MCP é o padrão que permite ao Claude se conectar a ferramentas reais, como o GitHub.",
      "Um agente é só um ciclo: observar, pensar, agir, repetir — com limites que você define.",
      "Este site inteiro é HTML, CSS e JavaScript puros. Sem frameworks, sem rastreamento."
    ],
    es: [
      "¿Recién llegas? La ruta Principiante toma unos 35 minutos, de principio a fin.",
      "Puedes cambiar de idioma cuando quieras — tu elección se guarda automáticamente.",
      "Cada lección termina con una insignia que puedes revisar desde la página de la ruta.",
      "¿Trabado en un quiz? No hay puntaje mínimo — está para enseñar, no para bloquearte.",
      "MCP es el estándar que permite a Claude conectarse a herramientas reales, como GitHub.",
      "Un agente es solo un ciclo: observar, pensar, actuar, repetir — con límites que tú defines.",
      "Todo este sitio es HTML, CSS y JavaScript puros. Sin frameworks, sin rastreo."
    ]
  };

  var LABELS = {
    en: { eyebrow: "Tip from Alex", close: "Close" },
    pt: { eyebrow: "Dica do Alex", close: "Fechar" },
    es: { eyebrow: "Consejo de Alex", close: "Cerrar" }
  };

  function currentLang() {
    if (window.ATS && window.ATS.i18n && typeof window.ATS.i18n.getLanguage === "function") {
      return window.ATS.i18n.getLanguage();
    }
    return "en";
  }

  function buildWidget() {
    var wrap = document.createElement("div");
    wrap.className = "guide-widget";
    wrap.innerHTML =
      '<div class="guide-panel" data-guide-panel hidden>' +
        '<button type="button" class="guide-close" data-guide-close aria-label="Close">&times;</button>' +
        '<p class="guide-eyebrow" data-guide-eyebrow>Tip from Alex</p>' +
        '<p class="guide-tip" data-guide-tip></p>' +
      "</div>" +
      '<button type="button" class="guide-bubble" data-guide-toggle aria-label="Tip from Alex">AM</button>';
    document.body.appendChild(wrap);
    return wrap;
  }

  function init() {
    var widget = buildWidget();
    var toggleBtn = widget.querySelector("[data-guide-toggle]");
    var closeBtn = widget.querySelector("[data-guide-close]");
    var panel = widget.querySelector("[data-guide-panel]");
    var tipEl = widget.querySelector("[data-guide-tip]");
    var eyebrowEl = widget.querySelector("[data-guide-eyebrow]");

    var tipIndex = Math.floor(Math.random() * TIPS.en.length);

    function renderTip() {
      var lang = currentLang();
      var tips = TIPS[lang] || TIPS.en;
      var labels = LABELS[lang] || LABELS.en;
      eyebrowEl.textContent = labels.eyebrow;
      closeBtn.setAttribute("aria-label", labels.close);
      tipEl.textContent = tips[tipIndex % tips.length];
    }

    toggleBtn.addEventListener("click", function () {
      var isHidden = panel.hidden;
      panel.hidden = !isHidden;
      if (isHidden) renderTip();
    });

    closeBtn.addEventListener("click", function () {
      panel.hidden = true;
    });

    var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!prefersReducedMotion) {
      setInterval(function () {
        tipIndex += 1;
        if (!panel.hidden) renderTip();
      }, 9000);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
