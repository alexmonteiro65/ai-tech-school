/* Shared engine for lesson pages: progress tracking, quiz checking,
   and a few reusable exercise patterns (choice / order / match).
   Exposed as window.ATS so lesson pages can call it from their own
   inline scripts. See CLAUDE.md sections 4 and 5.

   Every builder takes an optional `labels` object for its small set of
   fixed UI strings (button text, feedback prefixes, result templates) so
   a lesson page can pass the current language's strings on every render.
   Omitting `labels` falls back to English — see the *_DEFAULT objects. */
window.ATS = (function () {
  "use strict";

  var STORAGE_KEY = "ats_progress_v1";

  function readStorage() {
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function writeStorage(data) {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      /* storage unavailable — progress simply won't persist this session */
    }
  }

  function getProgress() {
    return readStorage();
  }

  function isLessonComplete(lessonId) {
    return !!readStorage()[lessonId];
  }

  function countCompleted(prefix) {
    var data = readStorage();
    return Object.keys(data).filter(function (id) {
      return data[id] && id.indexOf(prefix) === 0;
    }).length;
  }

  function completeLesson(lessonId, badgeElId) {
    var data = readStorage();
    data[lessonId] = true;
    writeStorage(data);
    if (badgeElId) {
      var el = document.getElementById(badgeElId);
      if (el) {
        el.hidden = false;
        el.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    }
  }

  function withDefaults(labels, defaults) {
    var out = {};
    var key;
    for (key in defaults) {
      if (Object.prototype.hasOwnProperty.call(defaults, key)) {
        out[key] = (labels && labels[key] !== undefined) ? labels[key] : defaults[key];
      }
    }
    return out;
  }

  var QUIZ_DEFAULT = {
    correctPrefix: "Correct.",
    incorrectPrefix: "Not quite.",
    scoreTemplate: function (correct, total) { return "You got " + correct + " of " + total + " right"; },
    summarySubtext: "You can review any explanation above at any time."
  };

  /* ---- Quiz engine ----
     questions: [{ text, options: [string...], correctIndex, explain }]
     Renders into the container, gives instant feedback on click, and
     calls onComplete(correctCount, total) once every question is answered. */
  function initQuiz(containerSelector, questions, labels, onComplete) {
    var container = document.querySelector(containerSelector);
    if (!container) return;
    var L = withDefaults(labels, QUIZ_DEFAULT);

    var letters = ["A", "B", "C", "D"];
    var answeredCount = 0;
    var correctCount = 0;

    var summary = document.createElement("div");
    summary.className = "quiz-summary";
    var scoreP = document.createElement("p");
    scoreP.className = "score";
    var subP = document.createElement("p");
    subP.textContent = L.summarySubtext;
    summary.appendChild(scoreP);
    summary.appendChild(subP);

    questions.forEach(function (q, qIndex) {
      var qEl = document.createElement("div");
      qEl.className = "quiz-question";

      var head = document.createElement("div");
      head.className = "quiz-question-head";
      var numEl = document.createElement("span");
      numEl.className = "quiz-question-num";
      numEl.textContent = "Q" + (qIndex + 1);
      var textEl = document.createElement("p");
      textEl.className = "quiz-question-text";
      textEl.textContent = q.text;
      head.appendChild(numEl);
      head.appendChild(textEl);
      qEl.appendChild(head);

      var optsWrap = document.createElement("div");
      optsWrap.className = "quiz-options";

      var explainEl = document.createElement("p");
      explainEl.className = "quiz-explain";
      explainEl.hidden = true;

      var answered = false;

      q.options.forEach(function (optionText, oIndex) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "quiz-option";

        var letterEl = document.createElement("span");
        letterEl.className = "quiz-option-letter";
        letterEl.textContent = letters[oIndex] || String(oIndex + 1);

        var labelEl = document.createElement("span");
        labelEl.textContent = optionText;

        btn.appendChild(letterEl);
        btn.appendChild(labelEl);

        btn.addEventListener("click", function () {
          if (answered) return;
          answered = true;
          answeredCount += 1;

          var buttons = optsWrap.querySelectorAll(".quiz-option");
          buttons.forEach(function (b) {
            b.disabled = true;
          });

          var isCorrect = oIndex === q.correctIndex;
          if (isCorrect) {
            btn.classList.add("is-correct");
            correctCount += 1;
          } else {
            btn.classList.add("is-incorrect");
            buttons[q.correctIndex].classList.add("is-correct");
          }

          explainEl.hidden = false;
          explainEl.innerHTML =
            "<strong>" + (isCorrect ? L.correctPrefix : L.incorrectPrefix) + "</strong> " +
            (q.explain || "");

          if (answeredCount === questions.length) {
            scoreP.textContent = L.scoreTemplate(correctCount, questions.length);
            summary.classList.add("is-visible");
            if (typeof onComplete === "function") {
              onComplete(correctCount, questions.length);
            }
          }
        });

        optsWrap.appendChild(btn);
      });

      qEl.appendChild(optsWrap);
      qEl.appendChild(explainEl);
      container.appendChild(qEl);
    });

    container.appendChild(summary);
  }

  var CHOICE_DEFAULT = {
    correctPrefix: "Correct — ",
    incorrectPrefix: "Not quite — "
  };

  /* ---- Choice exercise ----
     items: [{ text, choices: [string...], correctIndex, feedback }]
     One item = one statement with a small set of buttons to classify it. */
  function initChoiceExercise(containerSelector, items, labels) {
    var container = document.querySelector(containerSelector);
    if (!container) return;
    var L = withDefaults(labels, CHOICE_DEFAULT);

    items.forEach(function (item) {
      var itemEl = document.createElement("div");
      itemEl.className = "exercise-item";

      var textEl = document.createElement("p");
      textEl.className = "exercise-item-text";
      textEl.textContent = item.text;
      itemEl.appendChild(textEl);

      var choicesEl = document.createElement("div");
      choicesEl.className = "exercise-choices";

      var feedbackEl = document.createElement("p");
      feedbackEl.className = "feedback";
      feedbackEl.hidden = true;

      var answered = false;

      item.choices.forEach(function (choiceLabel, cIndex) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "option-btn";
        btn.textContent = choiceLabel;

        btn.addEventListener("click", function () {
          if (answered) return;
          answered = true;

          var buttons = choicesEl.querySelectorAll(".option-btn");
          buttons.forEach(function (b) {
            b.disabled = true;
          });

          var isCorrect = cIndex === item.correctIndex;
          if (isCorrect) {
            btn.classList.add("is-correct");
          } else {
            btn.classList.add("is-incorrect");
            buttons[item.correctIndex].classList.add("is-correct");
          }

          feedbackEl.hidden = false;
          feedbackEl.classList.add(isCorrect ? "is-correct" : "is-incorrect");
          feedbackEl.textContent = (isCorrect ? L.correctPrefix : L.incorrectPrefix) + (item.feedback || "");
        });

        choicesEl.appendChild(btn);
      });

      itemEl.appendChild(choicesEl);
      itemEl.appendChild(feedbackEl);
      container.appendChild(itemEl);
    });
  }

  var ORDER_DEFAULT = {
    checkButton: "Check my order",
    resultTemplate: function (correct, total) { return "<strong>" + correct + "</strong> of " + total + " in the right position."; }
  };

  /* ---- Order exercise ----
     correctSteps: [string...] already in the correct order.
     Renders them shuffled as buttons; clicking assigns the next slot. */
  function initOrderExercise(containerSelector, correctSteps, labels, onDone) {
    var container = document.querySelector(containerSelector);
    if (!container) return;
    var L = withDefaults(labels, ORDER_DEFAULT);

    var shuffled = correctSteps.slice();
    for (var i = shuffled.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = shuffled[i];
      shuffled[i] = shuffled[j];
      shuffled[j] = tmp;
    }

    var placedOrder = [];
    var buttonsByText = {};

    var listEl = document.createElement("div");
    listEl.className = "order-list";

    var checkBtn = document.createElement("button");
    checkBtn.type = "button";
    checkBtn.className = "btn btn-primary btn-sm";
    checkBtn.textContent = L.checkButton;
    checkBtn.hidden = true;

    shuffled.forEach(function (stepText) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "order-btn";

      var slot = document.createElement("span");
      slot.className = "order-slot";
      slot.textContent = "–";

      var label = document.createElement("span");
      label.textContent = stepText;

      btn.appendChild(slot);
      btn.appendChild(label);

      btn.addEventListener("click", function () {
        if (btn.classList.contains("is-placed")) return;
        placedOrder.push(stepText);
        btn.classList.add("is-placed");
        slot.textContent = String(placedOrder.length);

        if (placedOrder.length === correctSteps.length) {
          checkBtn.hidden = false;
        }
      });

      buttonsByText[stepText] = btn;
      listEl.appendChild(btn);
    });

    var resultEl = document.createElement("p");
    resultEl.className = "exercise-result";

    checkBtn.addEventListener("click", function () {
      var correct = 0;
      placedOrder.forEach(function (stepText, idx) {
        var btn = buttonsByText[stepText];
        if (stepText === correctSteps[idx]) {
          btn.classList.add("is-correct");
          correct += 1;
        } else {
          btn.classList.add("is-incorrect");
        }
      });
      resultEl.innerHTML = L.resultTemplate(correct, correctSteps.length);
      checkBtn.hidden = true;
      if (typeof onDone === "function") onDone(correct === correctSteps.length);
    });

    container.appendChild(listEl);
    container.appendChild(checkBtn);
    container.appendChild(resultEl);
  }

  var MATCH_DEFAULT = {
    choosePlaceholder: "Choose an option",
    checkButton: "Check answers",
    correctText: "Correct",
    incorrectTemplate: function (correctAnswer) { return "Correct answer: " + correctAnswer; },
    resultTemplate: function (correct, total) { return "<strong>" + correct + "</strong> of " + total + " correct."; }
  };

  /* ---- Match exercise ----
     items: [{ text, correct }], optionPool: [string...] shared dropdown choices. */
  function initMatchExercise(containerSelector, items, optionPool, labels, onDone) {
    var container = document.querySelector(containerSelector);
    if (!container) return;
    var L = withDefaults(labels, MATCH_DEFAULT);

    var rows = [];

    items.forEach(function (item) {
      var row = document.createElement("div");
      row.className = "select-row";

      var label = document.createElement("label");
      label.textContent = item.text;

      var select = document.createElement("select");
      var placeholderOpt = document.createElement("option");
      placeholderOpt.value = "";
      placeholderOpt.textContent = L.choosePlaceholder;
      select.appendChild(placeholderOpt);

      optionPool.forEach(function (optionText) {
        var opt = document.createElement("option");
        opt.value = optionText;
        opt.textContent = optionText;
        select.appendChild(opt);
      });

      var feedback = document.createElement("span");
      feedback.className = "row-feedback";

      row.appendChild(label);
      row.appendChild(select);
      row.appendChild(feedback);
      container.appendChild(row);

      rows.push({ select: select, feedback: feedback, correct: item.correct });
    });

    var checkBtn = document.createElement("button");
    checkBtn.type = "button";
    checkBtn.className = "btn btn-primary btn-sm";
    checkBtn.textContent = L.checkButton;

    var resultEl = document.createElement("p");
    resultEl.className = "exercise-result";

    checkBtn.addEventListener("click", function () {
      var correctCount = 0;
      rows.forEach(function (row) {
        var picked = row.select.value;
        var isCorrect = picked === row.correct;
        row.select.style.borderColor = isCorrect ? "var(--success)" : "var(--danger)";
        row.feedback.textContent = isCorrect ? L.correctText : L.incorrectTemplate(row.correct);
        row.feedback.style.color = isCorrect ? "var(--success)" : "var(--danger)";
        if (isCorrect) correctCount += 1;
      });
      resultEl.innerHTML = L.resultTemplate(correctCount, rows.length);
      if (typeof onDone === "function") onDone(correctCount === rows.length);
    });

    container.appendChild(checkBtn);
    container.appendChild(resultEl);
  }

  /* Translated UI chrome for the builders above (button text, feedback
     prefixes) — generic across every lesson, so it lives here once instead
     of being copy-pasted into all nine lesson pages. Lesson-specific
     content (questions, exercise items) still lives in each page. */
  var UI_LABELS = {
    en: {
      quiz: { correctPrefix: "Correct.", incorrectPrefix: "Not quite.", scoreTemplate: function (c, t) { return "You got " + c + " of " + t + " right"; }, summarySubtext: "You can review any explanation above at any time." },
      choice: { correctPrefix: "Correct — ", incorrectPrefix: "Not quite — " },
      order: { checkButton: "Check my order", resultTemplate: function (c, t) { return "<strong>" + c + "</strong> of " + t + " in the right position."; } },
      match: { choosePlaceholder: "Choose an option", checkButton: "Check answers", correctText: "Correct", incorrectTemplate: function (a) { return "Correct answer: " + a; }, resultTemplate: function (c, t) { return "<strong>" + c + "</strong> of " + t + " correct."; } }
    },
    pt: {
      quiz: { correctPrefix: "Correto.", incorrectPrefix: "Quase.", scoreTemplate: function (c, t) { return "Você acertou " + c + " de " + t; }, summarySubtext: "Você pode rever qualquer explicação acima quando quiser." },
      choice: { correctPrefix: "Certo — ", incorrectPrefix: "Quase — " },
      order: { checkButton: "Verificar minha ordem", resultTemplate: function (c, t) { return "<strong>" + c + "</strong> de " + t + " na posição correta."; } },
      match: { choosePlaceholder: "Escolha uma opção", checkButton: "Verificar respostas", correctText: "Correto", incorrectTemplate: function (a) { return "Resposta correta: " + a; }, resultTemplate: function (c, t) { return "<strong>" + c + "</strong> de " + t + " corretas."; } }
    },
    es: {
      quiz: { correctPrefix: "Correcto.", incorrectPrefix: "Casi.", scoreTemplate: function (c, t) { return "Acertaste " + c + " de " + t; }, summarySubtext: "Puedes revisar cualquier explicación de arriba cuando quieras." },
      choice: { correctPrefix: "Correcto — ", incorrectPrefix: "Casi — " },
      order: { checkButton: "Verificar mi orden", resultTemplate: function (c, t) { return "<strong>" + c + "</strong> de " + t + " en la posición correcta."; } },
      match: { choosePlaceholder: "Elige una opción", checkButton: "Verificar respuestas", correctText: "Correcto", incorrectTemplate: function (a) { return "Respuesta correcta: " + a; }, resultTemplate: function (c, t) { return "<strong>" + c + "</strong> de " + t + " correctas."; } }
    }
  };

  function getUILabels(lang) {
    return UI_LABELS[lang] || UI_LABELS.en;
  }

  return {
    getProgress: getProgress,
    isLessonComplete: isLessonComplete,
    countCompleted: countCompleted,
    completeLesson: completeLesson,
    initQuiz: initQuiz,
    initChoiceExercise: initChoiceExercise,
    initOrderExercise: initOrderExercise,
    initMatchExercise: initMatchExercise,
    getUILabels: getUILabels
  };
})();
