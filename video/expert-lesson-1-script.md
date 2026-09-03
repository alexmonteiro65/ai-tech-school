# Expert · Lesson 1 — "Building AI agents that work autonomously"
## Audio narration script (~2:15)

Source lesson: [`levels/expert/lesson-1.html`](../levels/expert/lesson-1.html)
Presenter voice: AITS, the AI Tech School mascot (first person). Plain audio narration format
— see the note in `video/beginner-lesson-2-script.md`.

---

## English

Hi, I'm A.I.T.S., your AI Tech School guide — here's the detailed walkthrough for this lesson. Welcome to Expert — and let's start with the idea that defines this whole path: agents.

An agent is an AI system that loops: observe, gather information. Think, decide what to do. Act, take an action, often via a tool. Then repeat — until the goal is done, largely without a human approving every single step. That's the key difference from Claude Code's default mode, where you review each step. An agent is trusted to make a chain of decisions on its own, within guardrails you define up front.

Here's the real risk: autonomy means mistakes can compound before a human notices. Good agent design always includes three things. Clear boundaries — exactly what it's allowed to touch. Observability — logs of what it actually did. And a stopping condition — a limit, or a point where it must hand off to a human.

A concrete example: an agent that monitors a support inbox and drafts replies — but only sends automatically for the cases it's confident about, and escalates everything else to a human. Notice what's happening there — it's not "no autonomy" and it's not "total autonomy" either. It's autonomy with a boundary around it.

On the page, you'll configure the permissions for an agent like that one yourself, and see what happens when a setup is missing a guardrail. Then three quick questions. See you in Lesson 2: connecting ten-plus tools.

Before you try the quiz below, here's a quick preview of the three questions and their answers. Question 1: What defines an "agent" as opposed to a simple prompt-response? Is it It only ever answers one question, It loops through observe, think, act on its own toward a goal, It's a bigger AI model, or It has no tools? The answer is It loops through observe, think, act on its own toward a goal — The defining trait is the autonomous loop toward a goal — not size or a single exchange. Question 2: What is the main risk of full autonomy? Is it It's too slow, Mistakes can compound before a human notices, It costs nothing, or It can't use tools? The answer is Mistakes can compound before a human notices — Without review at each step, an early mistake can cascade into several more before anyone catches it. Question 3: Which of these is a good guardrail for an autonomous agent? Is it No limits, let it run forever, A clear stopping condition and defined boundaries, Removing all logging to keep it simple, or Letting it modify its own permissions? The answer is A clear stopping condition and defined boundaries — A stopping condition and defined boundaries are exactly what limit how far a mistake can go.

## Português (Brasil)

Oi, eu sou o A.I.T.S., seu guia da AI Tech School — aqui vai o passo a passo detalhado desta aula. Bem-vindo ao Avançado — e vamos começar pela ideia que define toda essa trilha: agentes.

Um agente é um sistema de IA que funciona em ciclo: observar, coletar informações. Pensar, decidir o que fazer. Agir, realizar uma ação, geralmente por meio de uma ferramenta. E repetir — até a meta ser cumprida, em grande parte sem um humano aprovando cada etapa. Essa é a principal diferença em relação ao modo padrão do Claude Code, em que você revisa cada etapa. Um agente tem a confiança para tomar uma sequência de decisões sozinho, dentro de limites que você define previamente.

Aqui está o risco real: autonomia significa que erros podem se acumular antes que um humano perceba. Um bom projeto de agente sempre inclui três coisas. Limites claros — exatamente o que ele pode acessar. Observabilidade — registros do que ele realmente fez. E uma condição de parada — um limite, ou um ponto em que ele precisa repassar para um humano.

Um exemplo concreto: um agente que monitora uma caixa de suporte e redige respostas — mas só envia automaticamente nos casos em que tem confiança, e encaminha todo o resto para um humano. Repare o que está acontecendo ali — não é "nenhuma autonomia" e também não é "autonomia total". É autonomia com um limite ao redor dela.

Na página, você vai configurar as permissões de um agente assim, com as próprias mãos, e ver o que acontece quando uma configuração está sem alguma salvaguarda. Depois, três perguntas rápidas. Te vejo na Aula 2: conectando mais de dez ferramentas.

Antes de tentar o teste abaixo, aqui vai uma prévia rápida das três perguntas e suas respostas. Pergunta 1: O que define um "agente", em contraste com uma simples resposta a um prompt? É Ele só responde a uma pergunta, Ele funciona em ciclo de observar, pensar e agir sozinho rumo a uma meta, É um modelo de IA maior, ou Ele não usa ferramentas? A resposta é Ele funciona em ciclo de observar, pensar e agir sozinho rumo a uma meta — A característica que define é o ciclo autônomo em direção a uma meta — não o tamanho ou uma única troca. Pergunta 2: Qual é o principal risco da autonomia total? É É lento demais, Erros podem se acumular antes que um humano perceba, Não custa nada, ou Não consegue usar ferramentas? A resposta é Erros podem se acumular antes que um humano perceba — Sem revisão a cada etapa, um erro inicial pode se transformar em vários outros antes que alguém perceba. Pergunta 3: Qual destas é uma boa salvaguarda para um agente autônomo? É Sem limites, deixá-lo rodar para sempre, Uma condição de parada clara e limites bem definidos, Remover todos os registros para simplificar, ou Deixá-lo modificar as próprias permissões? A resposta é Uma condição de parada clara e limites bem definidos — Uma condição de parada e limites bem definidos são exatamente o que limita até onde um erro pode ir.

## Español (Latinoamérica)

Hola, soy A.I.T.S., tu guía de AI Tech School — aquí va el recorrido detallado de esta lección. Bienvenido a Experto — y empecemos por la idea que define toda esta ruta: los agentes.

Un agente es un sistema de IA que funciona en bucle: observar, recopilar información. Pensar, decidir qué hacer. Actuar, realizar una acción, a menudo mediante una herramienta. Y repetir — hasta cumplir el objetivo, en gran parte sin que un humano apruebe cada paso. Esa es la diferencia clave con el modo predeterminado de Claude Code, donde revisas cada paso. Un agente tiene la confianza para tomar una cadena de decisiones por sí solo, dentro de límites que defines de antemano.

Aquí está el riesgo real: la autonomía significa que los errores pueden acumularse antes de que un humano se dé cuenta. Un buen diseño de agente siempre incluye tres cosas. Límites claros — exactamente qué puede tocar. Observabilidad — registros de lo que realmente hizo. Y una condición de parada — un límite, o un punto en el que debe pasarle el control a un humano.

Un ejemplo concreto: un agente que monitorea una bandeja de soporte y redacta respuestas — pero solo las envía automáticamente en los casos donde tiene confianza, y escala todo lo demás a un humano. Fíjate qué está pasando ahí — no es "cero autonomía" y tampoco es "autonomía total". Es autonomía con un límite alrededor.

En la página vas a configurar los permisos de un agente como ese tú mismo, y vas a ver qué pasa cuando a una configuración le falta alguna salvaguarda. Después, tres preguntas rápidas. Nos vemos en la Lección 2: conectando más de diez herramientas.

Antes de intentar el cuestionario de abajo, aquí tienes un adelanto rápido de las tres preguntas y sus respuestas. Pregunta 1: ¿Qué define a un "agente" frente a una simple respuesta a un prompt? ¿Es Solo responde una pregunta, Funciona en un bucle de observar, pensar y actuar por sí solo hacia un objetivo, Es un modelo de IA más grande, o No usa herramientas? La respuesta es Funciona en un bucle de observar, pensar y actuar por sí solo hacia un objetivo — El rasgo definitorio es el bucle autónomo hacia un objetivo — no el tamaño ni un solo intercambio. Pregunta 2: ¿Cuál es el principal riesgo de la autonomía total? ¿Es Es demasiado lenta, Los errores pueden acumularse antes de que un humano se dé cuenta, No cuesta nada, o No puede usar herramientas? La respuesta es Los errores pueden acumularse antes de que un humano se dé cuenta — Sin revisión en cada paso, un error temprano puede convertirse en varios más antes de que alguien lo note. Pregunta 3: ¿Cuál de estas es una buena salvaguarda para un agente autónomo? ¿Es Sin límites, dejarlo correr para siempre, Una condición de parada clara y límites definidos, Eliminar todos los registros para simplificar, o Dejar que modifique sus propios permisos? La respuesta es Una condición de parada clara y límites definidos — Una condición de parada y límites definidos son exactamente lo que limita hasta dónde puede llegar un error.
