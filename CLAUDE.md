# AI Tech School (ATS)

## 1. Vision

AI Tech School teaches people — from complete beginners to working engineers —
how to actually use the modern AI ecosystem: Claude, Claude Code, the Model
Context Protocol (MCP), agents, and the tools built around them. The goal
stated in the tagline is literal: **"Learn to build with AI, not just use
it."**

The site is not a marketing page. It is a learning product. Every screen
either teaches something or points clearly at what to learn next.

**Content model: Anthropic Academy.** ATS teaches the same subject matter
Anthropic's own Academy teaches (Claude fundamentals → Claude Code → MCP →
the platform/API), so curriculum accuracy is anchored to the product itself,
not to third-party interpretations of it.

**Structure model: Codecademy.** Content is organized into explicit **Skill
Paths** — Beginner / Intermediate / Expert — each a fixed, ordered sequence
of lessons with clear milestones (what you'll learn, how long it takes, what
you can build after). No vague "browse and hope" navigation.

**Guide: Alex Monteiro, Founder.** ATS is fronted by its real founder, not a
mascot. Alex's presence (name, title, a short mission statement) appears on
the landing page and sets the tone: direct, practical, no hype. There is no
fictional character, no avatar illustration, no chatbot persona. If Alex's
bio or photo is added later, keep it factual — no invented credentials.

A small persistent widget (`js/guide.js`) puts Alex's "AM" monogram on
every page with a handful of rotating static tips. This is still not a
chatbot: no input box, no live AI call, just a fixed pool of short strings
cycled client-side. If it ever grows a text input or a real backend call,
that's a different feature needing its own review — not an incremental
change to this widget.

**Skill paths**, always presented in this order and never renamed:

| Path | Audience | Focus |
|---|---|---|
| Beginner | Never used Claude before | What Claude is, how to prompt it, what an API is |
| Intermediate | Comfortable with Claude, new to building | Installing Claude Code, your first MCP connector, your first automation |
| Expert | Ready to build production systems | Autonomous agents, multi-tool integration (Composio/MCP), deploying an automated AI-powered workflow |

Paths are progressive but not gated — anyone can open any lesson. No fake
paywalls, no fake "locked" states. Progress (which lessons are complete) is
tracked client-side only, in `localStorage`, purely to help a returning
learner pick up where they left off — never to block access.

## 2. Architecture Rules

- **No frameworks, no build step.** Pure HTML, CSS, and vanilla JavaScript.
  No React/Vue/Svelte, no bundler, no npm dependency for the site itself.
  Open any page directly (or serve the folder statically) and it works.
- **No external network calls from the site.** No CDN fonts, no analytics
  scripts, no third-party widgets, no live AI calls from lesson exercises.
  Every exercise and quiz is a self-contained client-side interaction —
  classification, matching, ordering, or a "build the config/prompt/
  pipeline" assembler — never a real API call. This keeps the school fast,
  private, free to run, and reviewable.
- **No paid/generative third-party APIs called from this project, ever.**
  This came up concretely: generating "The AI Universe" video via the
  Runway ML and HeyGen APIs was explicitly ruled out, for two independent
  reasons that both still apply to any future video, image, or audio
  generation idea. First, those are billed, key-authenticated APIs —
  putting a paid key in client-side JS exposes it to anyone who views
  source, and calling it from a server this project doesn't have would
  mean adding a backend, which contradicts the static-site rule above.
  Second, handling someone's API keys at all — even one at a time, even
  with explicit permission — isn't something this assistant does. The
  video pipeline that *did* ship instead: a hand-built SVG diagram
  (`diagrams/ai-universe.svg`), a script derived from it
  (`video/ai-universe-script.md`), and a static embed slot
  (`js/video.js` + `ai-universe-video.html` + a slot on each level's hub
  page) that shows a "coming soon" placeholder until real embed URLs (from
  a video the user generates and hosts themselves, e.g. on YouTube/Vimeo)
  are filled into `VIDEO_EMBED_URLS`. Don't revisit calling a generative
  video/image/voice API directly from this codebase without a real
  architecture conversation first.
- **Same reasoning applies to Buffer, Later, or any social-scheduling
  API** — requested for @ai.tech.school and declined for identical reasons
  (billed API + OAuth credentials this assistant won't hold, no backend to
  run a schedule on). What shipped instead: `social/content-calendar.md`,
  a real 30-day plan meant to be posted by hand. If real scheduling is ever
  wanted, that's a backend + credentials decision for a human to make
  deliberately, not something to wire up incrementally.
- **Static content, static hosting.** Pages are plain files. Lesson/quiz
  data lives inline in each lesson's own `<script>` block (a small JS
  object passed to the shared quiz engine) — not fetched from a server.
- **One HTML file per page.** Shared CSS lives in `css/`, shared JS in
  `js/`. Don't inline large `<style>`/`<script>` blocks into pages once
  more than one page reuses them — factor shared rules out instead of
  copy-pasting.
- **Progress is enhancement, not gating.** `localStorage` tracks completed
  lessons so hub pages can show progress and the homepage can welcome back
  a returning learner. If storage is unavailable or cleared, the site still
  works — it just shows no progress, never an error.
- **Progressive enhancement.** Every page is readable and navigable with
  JavaScript disabled. JS adds behavior (mobile nav, scroll-reveal, quiz
  interactivity, exercises, progress tracking) — the explanation text of
  every lesson is plain HTML, never JS-rendered.

### Folder structure

```
ATS/
  CLAUDE.md
  index.html                     # landing page
  how-claude-code-works.html     # visual diagrams: the Claude Code loop, install, MCP
  ai-news.html                   # curated, dated snapshot of AI ecosystem news
  ai-universe-video.html         # dedicated page for "The AI Universe" explainer video
  diagrams/
    ai-universe.svg              # source diagram behind the video script (Claude → Prompts/Chat → API → MCP → Connectors → Agents)
  video/
    ai-universe-script.md        # 2-minute presenter script, EN/PT/ES, scene-by-scene, tied to the diagram
  social/
    logo.svg, profile.png        # @ai.tech.school profile picture (lightning bolt + "ATS", not the site's bracket mark — deliberate, a profile pic at circular-crop size needs different treatment than the inline site logo)
    post-1-launch.* … post-9-cta.*      # 9 ready-to-post graphics (SVG source + rendered PNG), fill a complete 3×3 grid in order
    captions.md                  # EN/PT/ES captions per post
    reels-scripts.md             # 3 Reels scripts (60s each) — scripts only, no video generated
    profile-setup.md             # bio/link/profile-picture text, ready to paste in manually
    accounts-to-follow.md        # 20 hand-verified real Instagram accounts (wrong-guess handles caught and logged, not just assumed)
    content-calendar.md          # 30-day manual posting plan — 9 posts weeks 1–3, 3 Reels week 4
  css/
    style.css                    # global design system + all page styles
  js/
    main.js                      # global behavior: nav, scroll-reveal, footer year, progress banner
    lesson.js                    # shared engine: quiz/exercise checking, progress, badges, UI labels
    i18n.js                      # language-switching engine (see section 5)
    guide.js                     # persistent "AM" tips widget, every page (see section 1)
    video.js                     # video-embed config + placeholder renderer (see note below)
  assets/                        # icons/images, added as needed (SVG preferred)
  levels/
    beginner/
      index.html                 # path overview: what/how long/what you'll build + lesson list
      lesson-1.html … lesson-3.html
    intermediate/
      index.html
      lesson-1.html … lesson-3.html
    expert/
      index.html
      lesson-1.html … lesson-3.html
```

Adding a lesson means adding one HTML file under the right `levels/<path>/`
folder and one row in that path's `index.html` lesson list. Don't invent a
different folder shape per path. A standalone page like
`how-claude-code-works.html` or `ai-news.html` lives at the ATS root
alongside `index.html` — add its link to every page's nav (main-nav,
mobile-nav, footer) and its `nav.*` key to every page's dictionary, the
same way `nav.howItWorks` and `nav.news` were added.

## 3. Design System

Professional dark theme. Zero emojis, anywhere, in code or copy. No
cartoon or illustrated characters — icons are simple inline SVG (thin
stroke, monochrome, tinted by `currentColor`) or plain typographic badges
(e.g. a two-letter monogram, a path index like "01"). Consistent use of CSS
custom properties defined once in `css/style.css` under `:root` — never
hardcode a color, spacing value, or radius directly in a rule if a token
already exists for it.

**Color roles** (see `:root` in `style.css` for exact hex values):
- `--bg`, `--bg-elevated`, `--surface`, `--border` — layout surfaces
- `--text`, `--text-muted`, `--text-faint` — typography
- `--accent-purple` / `--accent-blue` — primary brand gradient (logo, CTAs)
- `--path-beginner` (emerald), `--path-intermediate` (sky blue),
  `--path-expert` (violet) — each skill path keeps its own accent color
  everywhere it appears (cards, tags, buttons, quiz feedback) so a learner
  always knows which path they're in.
- `--success` (correct quiz feedback), `--danger` (incorrect quiz feedback)
  — used only inside exercises/quizzes, never as decoration.

**Type:** system font stack (no web font download). A monospace stack is
reserved for code snippets, terminal examples, and config previews.

**Spacing/radius:** use the `--space-*` and `--radius-*` scale defined in
`style.css`. Don't invent one-off magic numbers.

**Motion:** subtle only — fades, slides. Always respect
`prefers-reduced-motion: reduce` by disabling non-essential animation.

## 4. Lesson Page Architecture

Every lesson page follows the same four-part structure, in this order:

1. **Explanation** — plain-language teaching content with a concrete,
   real-world example. No unexplained jargon; a new term is defined the
   first time it's used.
2. **Exercise** — exactly one interactive, hands-on activity the learner
   completes themselves (classify, match, order, or assemble something).
   It gives immediate visual feedback. It is never a passive "click next."
3. **Quiz** — exactly three multiple-choice questions. Each answer gives
   instant feedback (correct/incorrect + a one-line reason) the moment the
   learner picks an option. Score is shown at the end; there is no minimum
   score required to finish — this teaches, it doesn't gatekeep.
4. **Badge** — a completion badge naming the specific skill just learned
   (e.g. "Prompting Basics"), shown after the quiz is finished. Completing
   a lesson marks it done in `localStorage` via `js/lesson.js`, which the
   path's hub page and the homepage read to show progress.

All four parts are built with the shared helpers in `js/lesson.js`
(`initQuiz(...)`, `markLessonComplete(...)`, `getProgress()`). Exercise
interactivity is written per-lesson (each exercise is genuinely different)
but must reuse the shared `.exercise-box`, `.option-btn`, `.feedback`
classes from `style.css` rather than inventing new visual patterns.

## 5. Internationalization (i18n)

ATS supports English, Brazilian Portuguese (`pt`), and Latin American
Spanish (`es`) — always in that order wherever the switcher appears. The
engine is `js/i18n.js` (`ATS.i18n.init/setLanguage/getLanguage`); every page
loads it and calls `ATS.i18n.init(dict, onLanguageChange)`.

- **Translation dictionaries live inline per page**, the same way quiz and
  exercise data does — a `const PAGE_I18N = { en: {...}, pt: {...}, es:
  {...} }` object in the page's own `<script>` block. Don't centralize all
  copy into one shared file; a page's translations are that page's content.
- **Static text** (headings, paragraphs, nav, buttons, footer) is marked in
  HTML with `data-i18n="key"` (plain text), `data-i18n-html="key"` (when the
  string needs inline markup, e.g. a `<strong>` or the hero's accent
  `<span>`), or `data-i18n-placeholder="key"` (form placeholders). The
  engine walks these on init and on every language switch.
- **Dynamically-rendered content** (quiz questions, exercise items, assembled
  prompts/pipelines) cannot be reached by a DOM attribute — the page passes
  `onLanguageChange` to `ATS.i18n.init(...)`, and that callback clears the
  relevant container(s) and re-invokes the shared exercise/quiz builders
  with that language's data. Re-rendering an in-progress exercise or quiz on
  a language switch is expected behavior, not a bug — completion state
  (the badge, `localStorage` progress) is untouched by it.
- **Generic UI chrome** for the quiz/exercise builders (button text like
  "Check answers", feedback prefixes like "Correct — ") is not lesson
  content — it's translated once via `ATS.getUILabels(lang)` in
  `js/lesson.js` and passed as the `labels` argument to `initQuiz` /
  `initChoiceExercise` / `initOrderExercise` / `initMatchExercise`. Don't
  copy these strings into a lesson page's own dictionary.
- **English is the language actually written in the HTML.** The page must
  still read correctly with JavaScript disabled — it just won't be
  switchable, and dynamically-rendered exercises/quizzes won't render at
  all without JS regardless of language (see the no-JS caveat in section 2).
- The switcher itself is three buttons (`data-lang-btn="en|pt|es"`) in the
  header, always visible at every breakpoint — the `.header-cta` button is
  what hides on narrow screens to make room, never the switcher.
- Adding a fourth language means adding a key to `ATS.i18n.SUPPORTED` in
  `js/i18n.js`, a button in every page's switcher markup, and a new
  language block in every page's dictionary — there's no partial-language
  state to design around; a page either has all three (soon four) or the
  build isn't done.

## 6. Coding Standards

**HTML**
- Semantic elements first (`header`, `nav`, `main`, `section`, `article`,
  `footer`, `button` for actions, `a` for navigation). Div soup is a bug.
- Every interactive element is keyboard-reachable and has a visible focus
  state.
- One `<h1>` per page. Heading levels never skip. Lesson pages include a
  breadcrumb (`Home / <Path> / Lesson N`) as a `<nav aria-label="Breadcrumb">`.

**CSS**
- Mobile-first: base rules target the smallest viewport; `min-width` media
  queries layer on enhancements for larger screens. Never write a
  `max-width` query as the primary layout mechanism.
- Class naming: lowercase, hyphenated, lightly BEM-flavored
  (`.path-card`, `.path-card__title`, `.path-card--expert`). No IDs used
  for styling — IDs are reserved for anchors and JS hooks.
- Flexbox/Grid for layout. No floats, no fixed pixel widths on layout
  containers.
- No `!important`. If a rule needs to win, fix the specificity or the
  cascade order instead.

**JavaScript**
- Vanilla scripts, no globals beyond one namespace object (`window.ATS`)
  exposed by `js/lesson.js` for the shared helpers. Everything else stays
  scoped inside an IIFE — don't leak variables onto `window`.
- No dependencies. This is a teaching site — the code itself should be a
  good example of plain, readable JS.
- Feature-detect before using an API (`if ('IntersectionObserver' in
  window)`, try/catch around `localStorage`), and fail gracefully rather
  than throwing.

**Accessibility & performance**
- Contrast ratio ≥ 4.5:1 for body text against its background.
- Quiz/exercise feedback is never color-only — always paired with text
  ("Correct" / "Not quite") and an icon shape, for colorblind and
  screen-reader users.
- No layout-shifting images — always set intrinsic `width`/`height` or use
  `aspect-ratio` once real images are added.
- Keep every page lean enough to load instantly on a mid-tier mobile
  connection; this is a promise the "no frameworks" rule exists to keep.

## 7. Content Conventions

- Copy is written to the learner, second person ("you'll build...", not
  "students will build..."). Direct and practical — explain plainly, don't
  hype, don't gatekeep with jargon.
- Every path and every lesson names concrete outcomes (not vague promises
  like "learn AI") so a visitor can tell in five seconds if it's for them.
- No claims of certification, job guarantees, or specific salary outcomes.
  Teach the tools; don't oversell them.
- Every exercise and quiz question must reflect something actually true
  about Claude, Claude Code, MCP, or the tools named (Composio, GitHub,
  etc.) as of when it was written — this is a teaching product, accuracy
  is the product.

## 8. Working Conventions for Claude Code in This Repo

- Read this file before making structural changes (new pages, new shared
  CSS/JS, new folders).
- When adding a new lesson, reuse the existing design tokens and lesson
  components from `css/style.css` and the shared engine in `js/lesson.js`
  rather than redefining them — the whole site should look and behave like
  one product.
- Don't add a framework, build tool, or external dependency to solve a
  problem that plain HTML/CSS/JS already solves well. If a real need for
  tooling shows up later, raise it explicitly rather than introducing it
  quietly in an unrelated change.
- Keep this document in sync: if an architecture rule, the guide, or the
  design direction changes, update this file in the same change, not as an
  afterthought.
