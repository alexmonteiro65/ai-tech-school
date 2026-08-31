(function () {
  "use strict";

  /* Mobile nav toggle */
  var navToggle = document.querySelector("[data-nav-toggle]");
  var mobileNav = document.querySelector("[data-mobile-nav]");

  if (navToggle && mobileNav) {
    navToggle.addEventListener("click", function () {
      var isOpen = mobileNav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });

    mobileNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        mobileNav.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* Scroll reveal */
  var revealEls = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && revealEls.length) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    revealEls.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    revealEls.forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  /* Homepage progress banner — shown only if the learner has completed
     at least one lesson, read from the shared ATS.getProgress() helper. */
  var banner = document.querySelector("[data-progress-banner]");
  if (banner && window.ATS && typeof window.ATS.getProgress === "function") {
    var progress = window.ATS.getProgress();
    var completedIds = Object.keys(progress).filter(function (id) {
      return progress[id];
    });
    if (completedIds.length > 0) {
      var countEl = banner.querySelector("[data-progress-count]");
      if (countEl) {
        countEl.textContent = String(completedIds.length);
      }
      banner.classList.add("is-visible");
    }
  }

  /* Footer year */
  var yearEl = document.querySelector("[data-year]");
  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }
})();
