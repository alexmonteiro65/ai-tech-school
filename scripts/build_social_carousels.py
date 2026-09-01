#!/usr/bin/env python3
"""
One-time content-generation tool (not part of any CI pipeline): builds the
EN/PT/ES carousel slide SVGs for the 9 launch posts, so each Instagram post
can be a 3-slide carousel (English first, then Portuguese, then Spanish)
instead of an English-only single image — per Alex's explicit request that
"there's no translation for the post itself."

Each of the 9 xxxx() functions below reproduces one existing post's exact
layout (same positions, colors, shapes as social/post-N-*.svg) with only the
text swapped per language. Line breaks are chosen by hand per language
rather than computed, because translated text runs a different length than
English and a generic word-wrap would fight the fixed-width boxes used
throughout these designs.

Run: python3 scripts/build_social_carousels.py
Writes: social/carousels/post-N-{en,pt,es}.svg (27 files)

Rendering those to PNG is a separate step (headless-Chromium screenshot —
see the render step this was generated alongside) since this repo has no
SVG rasterizer installed.
"""
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "social", "carousels")

LANGS = ["en", "pt", "es"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------
# Post 1 — Launch announcement
# ---------------------------------------------------------------------------
POST1 = {
    "en": dict(eyebrow="NEW PLATFORM", tagline="Learn to build with AI, not just use it.",
               pill1="3 skill paths", pill2="9 lessons", footer="LINK IN BIO"),
    "pt": dict(eyebrow="NOVA PLATAFORMA", tagline="Aprenda a construir com IA, não só usá-la.",
               pill1="3 trilhas", pill2="9 aulas", footer="LINK NA BIO"),
    "es": dict(eyebrow="NUEVA PLATAFORMA", tagline="Aprende a construir con IA, no solo a usarla.",
               pill1="3 rutas", pill2="9 lecciones", footer="LINK EN BIO"),
}


def post1(t):
    return f"""<svg viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, -apple-system, Helvetica, Arial, sans-serif" role="img" aria-labelledby="title desc">
  <title id="title">AI Tech School — Launch Announcement</title>
  <desc id="desc">Instagram launch post: AI Tech School logo and tagline, learn to build with AI, three skill paths, nine lessons.</desc>
  <defs>
    <linearGradient id="brandGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8b5cf6"/><stop offset="100%" stop-color="#3b82f6"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="38%" r="55%">
      <stop offset="0%" stop-color="#26193f"/><stop offset="100%" stop-color="#0a0c12"/>
    </radialGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#glow)"/>
  <text x="540" y="270" text-anchor="middle" fill="#3b82f6" font-size="26" font-weight="700" letter-spacing="3">{esc(t['eyebrow'])}</text>
  <rect x="470" y="330" width="140" height="140" rx="32" fill="url(#brandGradient)"/>
  <g transform="translate(486,346) scale(4.5)">
    <path d="M8 4 3 12l5 8M16 4l5 8-5 8" stroke="#ffffff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="540" y="560" text-anchor="middle" fill="#f4f6fb" font-size="76" font-weight="800" letter-spacing="1">AI TECH SCHOOL</text>
  <text x="540" y="630" text-anchor="middle" fill="#9aa3b8" font-size="30" font-weight="500">{esc(t['tagline'])}</text>
  <g font-size="24" font-weight="700" fill="#f4f6fb">
    <rect x="150" y="720" width="230" height="66" rx="33" fill="#161a26" stroke="#262c3d" stroke-width="2"/>
    <text x="265" y="762" text-anchor="middle">{esc(t['pill1'])}</text>
    <rect x="415" y="720" width="250" height="66" rx="33" fill="#161a26" stroke="#262c3d" stroke-width="2"/>
    <text x="540" y="762" text-anchor="middle">{esc(t['pill2'])}</text>
    <rect x="700" y="720" width="230" height="66" rx="33" fill="#161a26" stroke="#262c3d" stroke-width="2"/>
    <text x="815" y="762" text-anchor="middle">EN · PT · ES</text>
  </g>
  <text x="540" y="960" text-anchor="middle" fill="#656d82" font-size="26" font-weight="600" letter-spacing="1">{esc(t['footer'])}</text>
</svg>
"""


# ---------------------------------------------------------------------------
# Post 2 — What is Claude
# ---------------------------------------------------------------------------
POST2 = {
    "en": dict(eyebrow="VISUAL EXPLAINER", title="What is Claude, really?",
               sub1="An AI model that reads what you give it and writes",
               sub2="an original, reasoned response — not a search engine.",
               f1t="Reads & writes in plain language", f1d="Emails, code, plans, explanations — whatever you need written.",
               f2t="Reasons step by step", f2d="Works through a problem with you, not just a one-shot answer.",
               f3t="Doesn't know live data on its own", f3d="Needs a connected tool to check today's news, prices, or events."),
    "pt": dict(eyebrow="EXPLICAÇÃO VISUAL", title="O que é o Claude, afinal?",
               sub1="Um modelo de IA que lê o que você fornece e escreve",
               sub2="uma resposta original e raciocinada — não é um buscador.",
               f1t="Lê e escreve em linguagem natural", f1d="E-mails, código, planos, explicações — o que você precisar escrever.",
               f2t="Raciocina passo a passo", f2d="Trabalha um problema junto com você, não dá só uma resposta pronta.",
               f3t="Não conhece dados em tempo real sozinho", f3d="Precisa de uma ferramenta conectada para ver notícias, preços ou eventos de hoje."),
    "es": dict(eyebrow="EXPLICACIÓN VISUAL", title="¿Qué es Claude, en realidad?",
               sub1="Un modelo de IA que lee lo que le das y escribe",
               sub2="una respuesta original y razonada — no es un buscador.",
               f1t="Lee y escribe en lenguaje natural", f1d="Correos, código, planes, explicaciones — lo que necesites escribir.",
               f2t="Razona paso a paso", f2d="Trabaja un problema contigo, no te da solo una respuesta de una vez.",
               f3t="No conoce datos en tiempo real por sí solo", f3d="Necesita una herramienta conectada para ver noticias, precios o eventos de hoy."),
}


def post2(t):
    return f"""<svg viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, -apple-system, Helvetica, Arial, sans-serif" role="img" aria-labelledby="title desc">
  <title id="title">What is Claude AI — simple explanation</title>
  <desc id="desc">Instagram post explaining Claude in plain language.</desc>
  <defs>
    <radialGradient id="glowWC" cx="50%" cy="10%" r="70%">
      <stop offset="0%" stop-color="#1c1533"/><stop offset="100%" stop-color="#0a0c12"/>
    </radialGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#glowWC)"/>
  <text x="540" y="120" text-anchor="middle" fill="#3b82f6" font-size="26" font-weight="700" letter-spacing="3">{esc(t['eyebrow'])}</text>
  <text x="540" y="185" text-anchor="middle" fill="#f4f6fb" font-size="48" font-weight="800">{esc(t['title'])}</text>
  <g fill="#9aa3b8" font-size="25" text-anchor="middle">
    <text x="540" y="235">{esc(t['sub1'])}</text>
    <text x="540" y="270">{esc(t['sub2'])}</text>
  </g>
  <g>
    <rect x="90" y="330" width="900" height="180" rx="24" fill="#161a26" stroke="#262c3d" stroke-width="2"/>
    <circle cx="180" cy="420" r="42" fill="#3b82f6" fill-opacity="0.15" stroke="#3b82f6" stroke-width="2"/>
    <path d="M 165 420 h 30 M 165 408 h 30 M 165 432 h 20" stroke="#3b82f6" stroke-width="3" stroke-linecap="round" transform="translate(0,-12)"/>
    <text x="250" y="410" fill="#f4f6fb" font-size="27" font-weight="800">{esc(t['f1t'])}</text>
    <text x="250" y="448" fill="#9aa3b8" font-size="21">{esc(t['f1d'])}</text>
  </g>
  <g>
    <rect x="90" y="530" width="900" height="180" rx="24" fill="#161a26" stroke="#262c3d" stroke-width="2"/>
    <circle cx="180" cy="620" r="42" fill="#8b5cf6" fill-opacity="0.15" stroke="#8b5cf6" stroke-width="2"/>
    <path d="M 165 608 l 15 12 l -15 12 M 195 632 h -12" stroke="#8b5cf6" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="250" y="610" fill="#f4f6fb" font-size="27" font-weight="800">{esc(t['f2t'])}</text>
    <text x="250" y="648" fill="#9aa3b8" font-size="21">{esc(t['f2d'])}</text>
  </g>
  <g>
    <rect x="90" y="730" width="900" height="180" rx="24" fill="#161a26" stroke="#f87171" stroke-opacity="0.5" stroke-width="2"/>
    <rect x="90" y="730" width="900" height="180" rx="24" fill="#f87171" fill-opacity="0.05"/>
    <circle cx="180" cy="820" r="42" fill="#f87171" fill-opacity="0.15" stroke="#f87171" stroke-width="2"/>
    <text x="180" y="833" text-anchor="middle" fill="#f87171" font-size="34" font-weight="800">!</text>
    <text x="250" y="810" fill="#f4f6fb" font-size="27" font-weight="800">{esc(t['f3t'])}</text>
    <text x="250" y="848" fill="#9aa3b8" font-size="21">{esc(t['f3d'])}</text>
  </g>
  <text x="540" y="1010" text-anchor="middle" fill="#656d82" font-size="26" font-weight="700" letter-spacing="1">AI TECH SCHOOL</text>
</svg>
"""


# ---------------------------------------------------------------------------
# Post 3 — API vs MCP
# ---------------------------------------------------------------------------
POST3 = {
    "en": dict(eyebrow="VISUAL EXPLAINER", title="API vs MCP", sub="Two different ways software reaches Claude",
               api=["You call specific|endpoints", "No memory between|calls", "Custom code needed|per tool", "General-purpose,|not AI-specific"],
               mcp=["Claude discovers|tools itself", "Keeps context|across steps", "One standard,|many tools", "Built for how AI|models actually work"]),
    "pt": dict(eyebrow="EXPLICAÇÃO VISUAL", title="API vs. MCP", sub="Duas formas diferentes de o software acessar o Claude",
               api=["Você chama endpoints|específicos", "Sem memória entre|as chamadas", "Precisa de código|próprio por ferramenta", "Uso geral,|não é feito para IA"],
               mcp=["O Claude descobre|as ferramentas sozinho", "Mantém o contexto|entre as etapas", "Um só padrão,|muitas ferramentas", "Feito para como a IA|realmente funciona"]),
    "es": dict(eyebrow="EXPLICACIÓN VISUAL", title="API vs. MCP", sub="Dos formas distintas de que el software llegue a Claude",
               api=["Llamas endpoints|específicos", "Sin memoria entre|las llamadas", "Necesita código propio|por herramienta", "De uso general,|no pensado para IA"],
               mcp=["Claude descubre las|herramientas solo", "Mantiene el contexto|entre los pasos", "Un solo estándar,|muchas herramientas", "Hecho para cómo la IA|realmente funciona"]),
}


def _two_line_block(x, y1, y2, text):
    line1, line2 = text.split("|")
    return f'<text x="{x}" y="{y1}" text-anchor="middle" fill="#f4f6fb" font-size="23" font-weight="700">{esc(line1)}</text>\n    <text x="{x}" y="{y2}" text-anchor="middle" fill="#f4f6fb" font-size="23" font-weight="700">{esc(line2)}</text>'


def post3(t):
    api_ys = [(410, 440), (530, 560), (650, 680), (770, 800)]
    mcp_ys = [(410, 440), (530, 560), (650, 680), (770, 800)]
    api_blocks = "\n    ".join(_two_line_block(300, y1, y2, txt) for (y1, y2), txt in zip(api_ys, t["api"]))
    mcp_blocks = "\n    ".join(_two_line_block(780, y1, y2, txt) for (y1, y2), txt in zip(mcp_ys, t["mcp"]))
    return f"""<svg viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, -apple-system, Helvetica, Arial, sans-serif" role="img" aria-labelledby="title desc">
  <title id="title">API vs MCP, explained simply</title>
  <desc id="desc">Instagram post comparing traditional APIs and the Model Context Protocol side by side.</desc>
  <defs>
    <radialGradient id="glowAM" cx="50%" cy="10%" r="70%">
      <stop offset="0%" stop-color="#1a1530"/><stop offset="100%" stop-color="#0a0c12"/>
    </radialGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#glowAM)"/>
  <text x="540" y="110" text-anchor="middle" fill="#3b82f6" font-size="26" font-weight="700" letter-spacing="3">{esc(t['eyebrow'])}</text>
  <text x="540" y="172" text-anchor="middle" fill="#f4f6fb" font-size="50" font-weight="800">{esc(t['title'])}</text>
  <text x="540" y="212" text-anchor="middle" fill="#9aa3b8" font-size="23">{esc(t['sub'])}</text>
  <g>
    <rect x="80" y="270" width="440" height="700" rx="24" fill="#161a26" stroke="#3b82f6" stroke-opacity="0.5" stroke-width="2"/>
    <text x="300" y="335" text-anchor="middle" fill="#3b82f6" font-size="34" font-weight="800" letter-spacing="1">API</text>
    {api_blocks}
  </g>
  <g>
    <rect x="560" y="270" width="440" height="700" rx="24" fill="#161a26" stroke="#8b5cf6" stroke-opacity="0.6" stroke-width="2"/>
    <rect x="560" y="270" width="440" height="700" rx="24" fill="#8b5cf6" fill-opacity="0.06"/>
    <text x="780" y="335" text-anchor="middle" fill="#8b5cf6" font-size="34" font-weight="800" letter-spacing="1">MCP</text>
    {mcp_blocks}
  </g>
  <text x="540" y="1010" text-anchor="middle" fill="#656d82" font-size="26" font-weight="700" letter-spacing="1">AI TECH SCHOOL</text>
</svg>
"""


# ---------------------------------------------------------------------------
# Post 4 — Three skill paths (reuses the site's own established translations)
# ---------------------------------------------------------------------------
POST4 = {
    "en": dict(eyebrow="CHOOSE YOUR PATH", title="Three levels. Pick where you are.",
               c1tag="01 · BEGINNER", c1title="Never touched Claude before", c1desc="What Claude is, how to prompt it, what an API does.",
               c2tag="02 · INTERMEDIATE", c2title="Ready to start building", c2desc="Install Claude Code, connect MCP, automate a task.",
               c3tag="03 · EXPERT", c3title="Building AI professionally", c3desc="Autonomous agents, 10+ connected tools, real deployment."),
    "pt": dict(eyebrow="ESCOLHA SUA TRILHA", title="Três níveis. Escolha onde você está.",
               c1tag="01 · INICIANTE", c1title="Nunca usou o Claude antes", c1desc="O que é o Claude, como fazer prompts, o que é uma API.",
               c2tag="02 · INTERMEDIÁRIO", c2title="Pronto para começar a construir", c2desc="Instale o Claude Code, conecte o MCP, automatize uma tarefa.",
               c3tag="03 · AVANÇADO", c3title="Construindo IA profissionalmente", c3desc="Agentes autônomos, 10+ ferramentas conectadas, implantação real."),
    "es": dict(eyebrow="ELIGE TU RUTA", title="Tres niveles. Elige dónde estás.",
               c1tag="01 · PRINCIPIANTE", c1title="Nunca usaste Claude antes", c1desc="Qué es Claude, cómo escribirle prompts, qué es una API.",
               c2tag="02 · INTERMEDIO", c2title="Listo para empezar a construir", c2desc="Instala Claude Code, conecta el MCP, automatiza una tarea.",
               c3tag="03 · EXPERTO", c3title="Construyendo IA profesionalmente", c3desc="Agentes autónomos, 10+ herramientas conectadas, despliegue real."),
}


def post4(t):
    return f"""<svg viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, -apple-system, Helvetica, Arial, sans-serif" role="img" aria-labelledby="title desc">
  <title id="title">AI Tech School — Three Skill Paths</title>
  <desc id="desc">Instagram post showing the three AI Tech School skill paths.</desc>
  <defs>
    <radialGradient id="glow2" cx="50%" cy="10%" r="70%">
      <stop offset="0%" stop-color="#1a1530"/><stop offset="100%" stop-color="#0a0c12"/>
    </radialGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#glow2)"/>
  <text x="540" y="120" text-anchor="middle" fill="#3b82f6" font-size="26" font-weight="700" letter-spacing="3">{esc(t['eyebrow'])}</text>
  <text x="540" y="180" text-anchor="middle" fill="#f4f6fb" font-size="44" font-weight="800">{esc(t['title'])}</text>
  <g>
    <rect x="90" y="260" width="900" height="220" rx="24" fill="#161a26" stroke="#34d399" stroke-opacity="0.6" stroke-width="2"/>
    <rect x="90" y="260" width="900" height="220" rx="24" fill="#34d399" fill-opacity="0.06"/>
    <text x="130" y="330" fill="#34d399" font-size="22" font-weight="800" letter-spacing="2">{esc(t['c1tag'])}</text>
    <text x="130" y="380" fill="#f4f6fb" font-size="32" font-weight="800">{esc(t['c1title'])}</text>
    <text x="130" y="425" fill="#9aa3b8" font-size="24">{esc(t['c1desc'])}</text>
  </g>
  <g>
    <rect x="90" y="500" width="900" height="220" rx="24" fill="#161a26" stroke="#38bdf8" stroke-opacity="0.6" stroke-width="2"/>
    <rect x="90" y="500" width="900" height="220" rx="24" fill="#38bdf8" fill-opacity="0.06"/>
    <text x="130" y="570" fill="#38bdf8" font-size="22" font-weight="800" letter-spacing="2">{esc(t['c2tag'])}</text>
    <text x="130" y="620" fill="#f4f6fb" font-size="32" font-weight="800">{esc(t['c2title'])}</text>
    <text x="130" y="665" fill="#9aa3b8" font-size="24">{esc(t['c2desc'])}</text>
  </g>
  <g>
    <rect x="90" y="740" width="900" height="220" rx="24" fill="#161a26" stroke="#c084fc" stroke-opacity="0.6" stroke-width="2"/>
    <rect x="90" y="740" width="900" height="220" rx="24" fill="#c084fc" fill-opacity="0.06"/>
    <text x="130" y="810" fill="#c084fc" font-size="22" font-weight="800" letter-spacing="2">{esc(t['c3tag'])}</text>
    <text x="130" y="860" fill="#f4f6fb" font-size="32" font-weight="800">{esc(t['c3title'])}</text>
    <text x="130" y="905" fill="#9aa3b8" font-size="24">{esc(t['c3desc'])}</text>
  </g>
  <text x="540" y="1020" text-anchor="middle" fill="#656d82" font-size="26" font-weight="700" letter-spacing="1">AI TECH SCHOOL</text>
</svg>
"""


# ---------------------------------------------------------------------------
# Post 5 — What is Claude Code
# ---------------------------------------------------------------------------
POST5 = {
    "en": dict(eyebrow="VISUAL EXPLAINER", title="What is Claude Code?", sub="Claude, inside your terminal — not just a chat window.",
               s1t="You ask in plain English", s1d='"Fix the failing test in checkout.js"',
               s2t="Claude reads your real files", s2d="Not a description of your project — the project itself.",
               s3t="You approve before it runs", s3d="Nothing changes in your project without your say-so."),
    "pt": dict(eyebrow="EXPLICAÇÃO VISUAL", title="O que é o Claude Code?", sub="O Claude, dentro do seu terminal — não só uma janela de chat.",
               s1t="Você pede em português simples", s1d='"Corrija o teste que está falhando em checkout.js"',
               s2t="O Claude lê seus arquivos reais", s2d="Não uma descrição do seu projeto — o projeto em si.",
               s3t="Você aprova antes de rodar", s3d="Nada muda no seu projeto sem o seu aval."),
    "es": dict(eyebrow="EXPLICACIÓN VISUAL", title="¿Qué es Claude Code?", sub="Claude, dentro de tu terminal — no solo una ventana de chat.",
               s1t="Pides las cosas en español simple", s1d='"Arregla la prueba que falla en checkout.js"',
               s2t="Claude lee tus archivos reales", s2d="No una descripción de tu proyecto — el proyecto en sí.",
               s3t="Tú apruebas antes de que se ejecute", s3d="Nada cambia en tu proyecto sin tu autorización."),
}


def post5(t):
    return f"""<svg viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, -apple-system, Helvetica, Arial, sans-serif" role="img" aria-labelledby="title desc">
  <title id="title">What is Claude Code?</title>
  <desc id="desc">Instagram post explaining Claude Code in three steps.</desc>
  <defs>
    <radialGradient id="glowCC" cx="50%" cy="12%" r="70%">
      <stop offset="0%" stop-color="#182238"/><stop offset="100%" stop-color="#0a0c12"/>
    </radialGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#glowCC)"/>
  <text x="540" y="130" text-anchor="middle" fill="#3b82f6" font-size="26" font-weight="700" letter-spacing="3">{esc(t['eyebrow'])}</text>
  <text x="540" y="195" text-anchor="middle" fill="#f4f6fb" font-size="46" font-weight="800">{esc(t['title'])}</text>
  <text x="540" y="240" text-anchor="middle" fill="#9aa3b8" font-size="24">{esc(t['sub'])}</text>
  <g>
    <rect x="90" y="300" width="900" height="200" rx="24" fill="#161a26" stroke="#262c3d" stroke-width="2"/>
    <circle cx="180" cy="400" r="42" fill="#3b82f6" fill-opacity="0.15" stroke="#3b82f6" stroke-width="2"/>
    <text x="180" y="415" text-anchor="middle" fill="#3b82f6" font-size="34" font-weight="800">1</text>
    <text x="250" y="385" fill="#f4f6fb" font-size="30" font-weight="800">{esc(t['s1t'])}</text>
    <text x="250" y="425" fill="#9aa3b8" font-size="23">{esc(t['s1d'])}</text>
  </g>
  <g>
    <rect x="90" y="520" width="900" height="200" rx="24" fill="#161a26" stroke="#262c3d" stroke-width="2"/>
    <circle cx="180" cy="620" r="42" fill="#8b5cf6" fill-opacity="0.15" stroke="#8b5cf6" stroke-width="2"/>
    <text x="180" y="635" text-anchor="middle" fill="#8b5cf6" font-size="34" font-weight="800">2</text>
    <text x="250" y="605" fill="#f4f6fb" font-size="30" font-weight="800">{esc(t['s2t'])}</text>
    <text x="250" y="645" fill="#9aa3b8" font-size="23">{esc(t['s2d'])}</text>
  </g>
  <g>
    <rect x="90" y="740" width="900" height="200" rx="24" fill="#161a26" stroke="#34d399" stroke-opacity="0.6" stroke-width="2"/>
    <rect x="90" y="740" width="900" height="200" rx="24" fill="#34d399" fill-opacity="0.06"/>
    <circle cx="180" cy="840" r="42" fill="#34d399" fill-opacity="0.15" stroke="#34d399" stroke-width="2"/>
    <text x="180" y="855" text-anchor="middle" fill="#34d399" font-size="34" font-weight="800">3</text>
    <text x="250" y="825" fill="#f4f6fb" font-size="30" font-weight="800">{esc(t['s3t'])}</text>
    <text x="250" y="865" fill="#9aa3b8" font-size="23">{esc(t['s3d'])}</text>
  </g>
  <text x="540" y="1010" text-anchor="middle" fill="#656d82" font-size="26" font-weight="700" letter-spacing="1">AI TECH SCHOOL</text>
</svg>
"""


# ---------------------------------------------------------------------------
# Post 6 — What is an AI Agent
# ---------------------------------------------------------------------------
POST6 = {
    "en": dict(eyebrow="VISUAL EXPLAINER", title="What is an AI Agent?", sub="Not just a chatbot — a loop.",
               observe="OBSERVE", observe_d="gather info", think="THINK", think_d="decide next step",
               act="ACT", act_d="use a tool", tail1="Repeats until the goal is done —", tail2="largely without a human approving every step."),
    "pt": dict(eyebrow="EXPLICAÇÃO VISUAL", title="O que é um Agente de IA?", sub="Não é só um chatbot — é um ciclo.",
               observe="OBSERVAR", observe_d="reunir informação", think="PENSAR", think_d="decidir o próximo passo",
               act="AGIR", act_d="usar uma ferramenta", tail1="Repete até o objetivo ser concluído —", tail2="em geral, sem um humano aprovar cada etapa."),
    "es": dict(eyebrow="EXPLICACIÓN VISUAL", title="¿Qué es un Agente de IA?", sub="No es solo un chatbot — es un ciclo.",
               observe="OBSERVAR", observe_d="reunir información", think="PENSAR", think_d="decidir el próximo paso",
               act="ACTUAR", act_d="usar una herramienta", tail1="Se repite hasta cumplir el objetivo —", tail2="casi siempre sin que un humano apruebe cada paso."),
}


def post6(t):
    return f"""<svg viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, -apple-system, Helvetica, Arial, sans-serif" role="img" aria-labelledby="title desc">
  <title id="title">What is an AI Agent?</title>
  <desc id="desc">Instagram post explaining AI agents as a loop of observe, think, and act.</desc>
  <defs>
    <radialGradient id="glowAG" cx="50%" cy="42%" r="60%">
      <stop offset="0%" stop-color="#241a3d"/><stop offset="100%" stop-color="#0a0c12"/>
    </radialGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#glowAG)"/>
  <text x="540" y="110" text-anchor="middle" fill="#3b82f6" font-size="26" font-weight="700" letter-spacing="3">{esc(t['eyebrow'])}</text>
  <text x="540" y="175" text-anchor="middle" fill="#f4f6fb" font-size="46" font-weight="800">{esc(t['title'])}</text>
  <text x="540" y="215" text-anchor="middle" fill="#9aa3b8" font-size="25">{esc(t['sub'])}</text>
  <circle cx="540" cy="560" r="260" fill="none" stroke="#262c3d" stroke-width="3"/>
  <circle cx="540" cy="300" r="80" fill="#161a26" stroke="#3b82f6" stroke-width="3"/>
  <text x="540" y="292" text-anchor="middle" fill="#3b82f6" font-size="22" font-weight="800">{esc(t['observe'])}</text>
  <text x="540" y="318" text-anchor="middle" fill="#9aa3b8" font-size="15">{esc(t['observe_d'])}</text>
  <circle cx="765" cy="710" r="80" fill="#161a26" stroke="#8b5cf6" stroke-width="3"/>
  <text x="765" y="702" text-anchor="middle" fill="#8b5cf6" font-size="22" font-weight="800">{esc(t['think'])}</text>
  <text x="765" y="728" text-anchor="middle" fill="#9aa3b8" font-size="15">{esc(t['think_d'])}</text>
  <circle cx="315" cy="710" r="80" fill="#161a26" stroke="#34d399" stroke-width="3"/>
  <text x="315" y="702" text-anchor="middle" fill="#34d399" font-size="22" font-weight="800">{esc(t['act'])}</text>
  <text x="315" y="728" text-anchor="middle" fill="#9aa3b8" font-size="15">{esc(t['act_d'])}</text>
  <path d="M 610 340 A 260 260 0 0 1 740 635" fill="none" stroke="#656d82" stroke-width="3" marker-end="url(#agentArrow)"/>
  <path d="M 690 760 A 260 260 0 0 1 390 760" fill="none" stroke="#656d82" stroke-width="3" marker-end="url(#agentArrow)"/>
  <path d="M 340 635 A 260 260 0 0 1 470 340" fill="none" stroke="#656d82" stroke-width="3" marker-end="url(#agentArrow)"/>
  <defs>
    <marker id="agentArrow" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#656d82"/>
    </marker>
  </defs>
  <text x="540" y="880" text-anchor="middle" fill="#9aa3b8" font-size="22">{esc(t['tail1'])}</text>
  <text x="540" y="915" text-anchor="middle" fill="#9aa3b8" font-size="22">{esc(t['tail2'])}</text>
  <text x="540" y="1010" text-anchor="middle" fill="#656d82" font-size="26" font-weight="700" letter-spacing="1">AI TECH SCHOOL</text>
</svg>
"""


# ---------------------------------------------------------------------------
# Post 7 — Free tools
# ---------------------------------------------------------------------------
POST7 = {
    "en": dict(eyebrow="FREE & UNDERRATED", title="4 free AI tools", sub="you're probably not using yet",
               t1="Gemini Notebook", d1="Formerly NotebookLM — upload sources, get answers grounded in them.", n1="Free: 100 notebooks, 50 sources each, 50 questions a day",
               t2="Google AI Studio", d2="A free playground to prototype with Gemini models using plain prompts.", n2="Free access in most regions",
               t3="Hugging Face Spaces", d3="Free hosting to run and share open-source AI models and demos.", n3="Free tier, no credit card",
               t4="GitHub Copilot (free tier)", d4="Free tier available for individual accounts and verified students.", n4="Check current eligibility on github.com"),
    "pt": dict(eyebrow="GRÁTIS E SUBESTIMADAS", title="4 ferramentas de IA grátis", sub="que você provavelmente ainda não usa",
               t1="Gemini Notebook", d1="Antigo NotebookLM — envie suas fontes e receba respostas baseadas nelas.", n1="Grátis: 100 notebooks, 50 fontes cada, 50 perguntas por dia",
               t2="Google AI Studio", d2="Um playground gratuito para prototipar com modelos Gemini usando prompts simples.", n2="Acesso gratuito na maioria das regiões",
               t3="Hugging Face Spaces", d3="Hospedagem grátis para rodar e compartilhar modelos e demos de IA de código aberto.", n3="Plano grátis, sem cartão de crédito",
               t4="GitHub Copilot (plano grátis)", d4="Plano grátis disponível para contas individuais e estudantes verificados.", n4="Confira a elegibilidade atual em github.com"),
    "es": dict(eyebrow="GRATIS Y SUBVALORADAS", title="4 herramientas de IA gratis", sub="que probablemente no estés usando",
               t1="Gemini Notebook", d1="Antes NotebookLM — sube tus fuentes y recibe respuestas basadas en ellas.", n1="Gratis: 100 notebooks, 50 fuentes cada uno, 50 preguntas al día",
               t2="Google AI Studio", d2="Un espacio gratuito para prototipar con modelos Gemini usando prompts simples.", n2="Acceso gratuito en la mayoría de regiones",
               t3="Hugging Face Spaces", d3="Alojamiento gratis para correr y compartir modelos y demos de IA de código abierto.", n3="Plan gratis, sin tarjeta de crédito",
               t4="GitHub Copilot (plan gratis)", d4="Plan gratis disponible para cuentas individuales y estudiantes verificados.", n4="Revisa la elegibilidad actual en github.com"),
}


def post7(t):
    return f"""<svg viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, -apple-system, Helvetica, Arial, sans-serif" role="img" aria-labelledby="title desc">
  <title id="title">Free AI tools you don't know about</title>
  <desc id="desc">Instagram post listing four genuinely free AI tools.</desc>
  <defs>
    <radialGradient id="glowFT" cx="50%" cy="10%" r="70%">
      <stop offset="0%" stop-color="#182238"/><stop offset="100%" stop-color="#0a0c12"/>
    </radialGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#glowFT)"/>
  <text x="540" y="115" text-anchor="middle" fill="#3b82f6" font-size="24" font-weight="700" letter-spacing="2">{esc(t['eyebrow'])}</text>
  <text x="540" y="180" text-anchor="middle" fill="#f4f6fb" font-size="44" font-weight="800">{esc(t['title'])}</text>
  <text x="540" y="225" text-anchor="middle" fill="#9aa3b8" font-size="25">{esc(t['sub'])}</text>
  <g>
    <rect x="90" y="280" width="900" height="165" rx="20" fill="#161a26" stroke="#262c3d" stroke-width="2"/>
    <text x="130" y="335" fill="#3b82f6" font-size="28" font-weight="800">{esc(t['t1'])}</text>
    <text x="130" y="370" fill="#9aa3b8" font-size="20">{esc(t['d1'])}</text>
    <text x="130" y="400" fill="#656d82" font-size="17">{esc(t['n1'])}</text>
  </g>
  <g>
    <rect x="90" y="465" width="900" height="165" rx="20" fill="#161a26" stroke="#262c3d" stroke-width="2"/>
    <text x="130" y="520" fill="#8b5cf6" font-size="28" font-weight="800">{esc(t['t2'])}</text>
    <text x="130" y="555" fill="#9aa3b8" font-size="20">{esc(t['d2'])}</text>
    <text x="130" y="585" fill="#656d82" font-size="17">{esc(t['n2'])}</text>
  </g>
  <g>
    <rect x="90" y="650" width="900" height="165" rx="20" fill="#161a26" stroke="#262c3d" stroke-width="2"/>
    <text x="130" y="705" fill="#38bdf8" font-size="28" font-weight="800">{esc(t['t3'])}</text>
    <text x="130" y="740" fill="#9aa3b8" font-size="20">{esc(t['d3'])}</text>
    <text x="130" y="770" fill="#656d82" font-size="17">{esc(t['n3'])}</text>
  </g>
  <g>
    <rect x="90" y="835" width="900" height="165" rx="20" fill="#161a26" stroke="#34d399" stroke-opacity="0.5" stroke-width="2"/>
    <rect x="90" y="835" width="900" height="165" rx="20" fill="#34d399" fill-opacity="0.05"/>
    <text x="130" y="890" fill="#34d399" font-size="28" font-weight="800">{esc(t['t4'])}</text>
    <text x="130" y="925" fill="#9aa3b8" font-size="20">{esc(t['d4'])}</text>
    <text x="130" y="955" fill="#656d82" font-size="17">{esc(t['n4'])}</text>
  </g>
  <text x="540" y="1050" text-anchor="middle" fill="#656d82" font-size="24" font-weight="700" letter-spacing="1">AI TECH SCHOOL</text>
</svg>
"""


# ---------------------------------------------------------------------------
# Post 8 — Founder quote
# ---------------------------------------------------------------------------
POST8 = {
    "en": dict(eyebrow="MEET THE FOUNDER", name="Alex Monteiro", role="FOUNDER, AI TECH SCHOOL",
               q1='"I built ATS to teach the AI ecosystem', q2="the way I wish someone had taught it to me —", q3='in order, hands-on, and without the hype."'),
    "pt": dict(eyebrow="CONHEÇA O FUNDADOR", name="Alex Monteiro", role="FUNDADOR, AI TECH SCHOOL",
               q1='"Eu criei a AITS para ensinar o ecossistema de IA', q2="do jeito que eu gostaria que tivessem me ensinado —", q3='em ordem, na prática, e sem o exagero."'),
    "es": dict(eyebrow="CONOCE AL FUNDADOR", name="Alex Monteiro", role="FUNDADOR, AI TECH SCHOOL",
               q1='"Creé AITS para enseñar el ecosistema de IA', q2="como me hubiera gustado que me lo enseñaran —", q3='en orden, de forma práctica, y sin el exagero."'),
}


def post8(t):
    return f"""<svg viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, -apple-system, Helvetica, Arial, sans-serif" role="img" aria-labelledby="title desc">
  <title id="title">AI Tech School — Founder Story</title>
  <desc id="desc">Instagram post introducing Alex Monteiro, founder of AI Tech School.</desc>
  <defs>
    <linearGradient id="avatarGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8b5cf6"/><stop offset="100%" stop-color="#3b82f6"/>
    </linearGradient>
    <radialGradient id="glow3" cx="50%" cy="30%" r="60%">
      <stop offset="0%" stop-color="#241a3d"/><stop offset="100%" stop-color="#0a0c12"/>
    </radialGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#glow3)"/>
  <text x="540" y="150" text-anchor="middle" fill="#3b82f6" font-size="26" font-weight="700" letter-spacing="3">{esc(t['eyebrow'])}</text>
  <circle cx="540" cy="330" r="120" fill="url(#avatarGradient)"/>
  <text x="540" y="358" text-anchor="middle" fill="#ffffff" font-size="72" font-weight="800">AM</text>
  <text x="540" y="520" text-anchor="middle" fill="#f4f6fb" font-size="56" font-weight="800">{esc(t['name'])}</text>
  <text x="540" y="565" text-anchor="middle" fill="#3b82f6" font-size="26" font-weight="700" letter-spacing="1">{esc(t['role'])}</text>
  <g fill="#9aa3b8" font-size="29" text-anchor="middle">
    <text x="540" y="670">{esc(t['q1'])}</text>
    <text x="540" y="715">{esc(t['q2'])}</text>
    <text x="540" y="760">{esc(t['q3'])}</text>
  </g>
  <rect x="440" y="830" width="200" height="4" rx="2" fill="#262c3d"/>
  <text x="540" y="960" text-anchor="middle" fill="#656d82" font-size="26" font-weight="700" letter-spacing="1">AI TECH SCHOOL</text>
</svg>
"""


# ---------------------------------------------------------------------------
# Post 9 — CTA
# ---------------------------------------------------------------------------
POST9 = {
    "en": dict(eyebrow="TODAY IS A GOOD DAY TO START", line1="Stop scrolling.", line2="Start building.",
               sub1="Lesson 1 of the Beginner path is free", sub2="and takes about 10 minutes.",
               cta="START LESSON 1", footer="LINK IN BIO"),
    "pt": dict(eyebrow="HOJE É UM ÓTIMO DIA PARA COMEÇAR", line1="Pare de rolar a tela.", line2="Comece a construir.",
               sub1="A Aula 1 da trilha Iniciante é grátis", sub2="e leva cerca de 10 minutos.",
               cta="COMEÇAR AULA 1", footer="LINK NA BIO"),
    "es": dict(eyebrow="HOY ES UN BUEN DÍA PARA EMPEZAR", line1="Deja de hacer scroll.", line2="Empieza a construir.",
               sub1="La Lección 1 de la ruta Principiante es gratis", sub2="y toma unos 10 minutos.",
               cta="EMPEZAR LECCIÓN 1", footer="LINK EN BIO"),
}


def post9(t):
    return f"""<svg viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, -apple-system, Helvetica, Arial, sans-serif" role="img" aria-labelledby="title desc">
  <title id="title">Call to action — start learning today</title>
  <desc id="desc">Instagram post prompting the viewer to start the free Beginner lesson today.</desc>
  <defs>
    <linearGradient id="ctaGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8b5cf6"/><stop offset="100%" stop-color="#3b82f6"/>
    </linearGradient>
    <radialGradient id="glowCTA" cx="50%" cy="40%" r="65%">
      <stop offset="0%" stop-color="#22163f"/><stop offset="100%" stop-color="#0a0c12"/>
    </radialGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#glowCTA)"/>
  <text x="540" y="260" text-anchor="middle" fill="#3b82f6" font-size="24" font-weight="700" letter-spacing="2">{esc(t['eyebrow'])}</text>
  <text x="540" y="380" text-anchor="middle" fill="#f4f6fb" font-size="64" font-weight="800">{esc(t['line1'])}</text>
  <text x="540" y="460" text-anchor="middle" fill="#f4f6fb" font-size="64" font-weight="800">{esc(t['line2'])}</text>
  <text x="540" y="540" text-anchor="middle" fill="#9aa3b8" font-size="28">{esc(t['sub1'])}</text>
  <text x="540" y="580" text-anchor="middle" fill="#9aa3b8" font-size="28">{esc(t['sub2'])}</text>
  <rect x="300" y="660" width="480" height="90" rx="45" fill="url(#ctaGradient)"/>
  <text x="540" y="716" text-anchor="middle" fill="#ffffff" font-size="30" font-weight="800">{esc(t['cta'])}</text>
  <text x="540" y="820" text-anchor="middle" fill="#656d82" font-size="26" font-weight="700" letter-spacing="1">{esc(t['footer'])}</text>
  <text x="540" y="1010" text-anchor="middle" fill="#656d82" font-size="26" font-weight="700" letter-spacing="1">AI TECH SCHOOL</text>
</svg>
"""


POSTS = [
    ("post-1-launch", POST1, post1),
    ("post-2-what-is-claude", POST2, post2),
    ("post-3-api-vs-mcp", POST3, post3),
    ("post-4-levels", POST4, post4),
    ("post-5-claude-code", POST5, post5),
    ("post-6-ai-agent", POST6, post6),
    ("post-7-free-tools", POST7, post7),
    ("post-8-quote", POST8, post8),
    ("post-9-cta", POST9, post9),
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    count = 0
    for slug, translations, builder in POSTS:
        for lang in LANGS:
            svg = builder(translations[lang])
            out_path = os.path.join(OUT_DIR, f"{slug}-{lang}.svg")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(svg)
            count += 1
    print(f"Wrote {count} SVG files to {OUT_DIR}")


if __name__ == "__main__":
    main()
