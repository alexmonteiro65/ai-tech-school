# Intermediate · Lesson 2 — "Your first MCP connector — connecting GitHub"
## Audio narration script (~2 min)

Source lesson: [`levels/intermediate/lesson-2.html`](../levels/intermediate/lesson-2.html)
Presenter voice: AITS, the AI Tech School mascot (first person). Plain audio narration format
— see the note in `video/beginner-lesson-2-script.md`.

---

## English

Hi, I'm AITS, your AI Tech School guide — here's the detailed walkthrough for this lesson. This lesson covers the idea that turns Claude from an assistant who talks about your work into one that can actually act on it: MCP.

MCP, the Model Context Protocol, is an open standard that lets Claude connect to external tools and data sources — like GitHub, Google Drive, or a database — in a consistent way. Without MCP, Claude only knows what's in the conversation. With MCP, Claude can look things up and take real actions through MCP servers.

Three words are worth knowing here. An MCP Server is the connector itself — for example, a GitHub MCP server. A Tool is a specific action a server exposes, like "create a pull request." And a Client is the app using the server — Claude Code, in our case.

Here's what connecting GitHub actually changes: Claude goes from an assistant who talks about your repository to one that can read issues, search code, and open pull requests — always with your visibility into what it's doing.

On the page, you'll match each of these MCP terms to its correct definition, then check your understanding with three quick questions. See you in Lesson 3: building your first automated task.

Before you try the quiz below, here's a quick preview of the three questions and their answers. Question 1: What problem does MCP solve? Is it It makes Claude faster, It gives Claude a standard way to connect to real tools and data, It replaces the need for prompts, or It's a new programming language? The answer is It gives Claude a standard way to connect to real tools and data — MCP is a protocol — a consistent way for Claude to reach external tools and data instead of a one-off integration per tool. Question 2: In MCP, what is a Tool? Is it The app using Claude, A specific action a server exposes, like "create a pull request", The AI model itself, or A type of prompt? The answer is A specific action a server exposes, like "create a pull request" — A Tool is one concrete action the MCP server makes available — the Client is the app, the Server is the connector. Question 3: After connecting the GitHub MCP server, what changes? Is it Nothing, it's cosmetic, Claude can take real actions on your repo, like opening pull requests, GitHub is deleted, or You lose access to your code? The answer is Claude can take real actions on your repo, like opening pull requests — Claude moves from discussing your repo to acting on it — reading issues, searching code, opening pull requests.

## Português (Brasil)

Oi, eu sou o AITS, seu guia da AI Tech School — aqui vai o passo a passo detalhado desta aula. Esta aula cobre a ideia que transforma o Claude de um assistente que fala sobre o seu trabalho em um que consegue agir de verdade sobre ele: o MCP.

O MCP, o Model Context Protocol, é um padrão aberto que permite ao Claude se conectar a ferramentas e fontes de dados externas — como GitHub, Google Drive ou um banco de dados — de forma consistente. Sem o MCP, o Claude só sabe o que está na conversa. Com o MCP, o Claude consegue consultar informações e realizar ações reais por meio de servidores MCP.

Vale a pena conhecer três palavras aqui. Um Servidor MCP é o conector em si — por exemplo, um servidor MCP do GitHub. Uma Ferramenta é uma ação específica que um servidor disponibiliza, como "criar um pull request". E um Cliente é o aplicativo que usa o servidor — o Claude Code, no nosso caso.

Veja o que realmente muda ao conectar o GitHub: o Claude passa de um assistente que fala sobre o seu repositório para um que consegue ler issues, buscar código e abrir pull requests — sempre com total visibilidade do que ele está fazendo.

Na página, você vai combinar cada um desses termos do MCP com sua definição correta, e depois verificar seu entendimento com três perguntas rápidas. Te vejo na Aula 3: construindo sua primeira tarefa automatizada.

Antes de tentar o teste abaixo, aqui vai uma prévia rápida das três perguntas e suas respostas. Pergunta 1: Qual problema o MCP resolve? É Deixa o Claude mais rápido, Dá ao Claude uma forma padronizada de se conectar a ferramentas e dados reais, Elimina a necessidade de prompts, ou É uma nova linguagem de programação? A resposta é Dá ao Claude uma forma padronizada de se conectar a ferramentas e dados reais — O MCP é um protocolo — uma forma consistente de o Claude acessar ferramentas e dados externos, em vez de uma integração personalizada para cada ferramenta. Pergunta 2: No MCP, o que é uma Ferramenta (Tool)? É O aplicativo que usa o Claude, Uma ação específica que um servidor disponibiliza, como "criar um pull request", O próprio modelo de IA, ou Um tipo de prompt? A resposta é Uma ação específica que um servidor disponibiliza, como "criar um pull request" — Uma Ferramenta é uma ação concreta que o servidor MCP disponibiliza — o Cliente é o aplicativo, o Servidor é o conector. Pergunta 3: Depois de conectar o servidor MCP do GitHub, o que muda? É Nada, é só estético, O Claude consegue realizar ações reais no seu repositório, como abrir pull requests, O GitHub é apagado, ou Você perde o acesso ao seu código? A resposta é O Claude consegue realizar ações reais no seu repositório, como abrir pull requests — O Claude passa de discutir sobre o seu repositório para agir sobre ele — lendo issues, buscando código, abrindo pull requests.

## Español (Latinoamérica)

Hola, soy AITS, tu guía de AI Tech School — aquí va el recorrido detallado de esta lección. Esta lección cubre la idea que convierte a Claude de un asistente que habla sobre tu trabajo en uno que puede actuar sobre él de verdad: MCP.

MCP, el Model Context Protocol, es un estándar abierto que permite a Claude conectarse a herramientas y fuentes de datos externas — como GitHub, Google Drive o una base de datos — de forma consistente. Sin MCP, Claude solo sabe lo que hay en la conversación. Con MCP, Claude puede consultar información y realizar acciones reales a través de servidores MCP.

Vale la pena conocer tres palabras aquí. Un Servidor MCP es el conector en sí — por ejemplo, un servidor MCP de GitHub. Una Herramienta es una acción específica que un servidor expone, como "crear un pull request". Y un Cliente es la app que usa el servidor — Claude Code, en nuestro caso.

Esto es lo que realmente cambia al conectar GitHub: Claude pasa de ser un asistente que habla sobre tu repositorio a uno que puede leer issues, buscar código y abrir pull requests — siempre con total visibilidad de lo que está haciendo.

En la página vas a relacionar cada uno de estos términos de MCP con su definición correcta, y luego vas a verificar tu comprensión con tres preguntas rápidas. Nos vemos en la Lección 3: construyendo tu primera tarea automatizada.

Antes de intentar el cuestionario de abajo, aquí tienes un adelanto rápido de las tres preguntas y sus respuestas. Pregunta 1: ¿Qué problema resuelve MCP? ¿Es Hace que Claude sea más rápido, Le da a Claude una forma estándar de conectarse a herramientas y datos reales, Elimina la necesidad de prompts, o Es un nuevo lenguaje de programación? La respuesta es Le da a Claude una forma estándar de conectarse a herramientas y datos reales — MCP es un protocolo — una forma consistente de que Claude acceda a herramientas y datos externos, en lugar de una integración distinta por cada herramienta. Pregunta 2: En MCP, ¿qué es una Herramienta (Tool)? ¿Es La app que usa Claude, Una acción específica que un servidor expone, como "crear un pull request", El propio modelo de IA, o Un tipo de prompt? La respuesta es Una acción específica que un servidor expone, como "crear un pull request" — Una Herramienta es una acción concreta que el servidor MCP pone a disposición — el Cliente es la app, el Servidor es el conector. Pregunta 3: Después de conectar el servidor MCP de GitHub, ¿qué cambia? ¿Es Nada, es solo estético, Claude puede realizar acciones reales en tu repositorio, como abrir pull requests, Se elimina GitHub, o Pierdes el acceso a tu código? La respuesta es Claude puede realizar acciones reales en tu repositorio, como abrir pull requests — Claude pasa de hablar sobre tu repositorio a actuar sobre él — leyendo issues, buscando código, abriendo pull requests.
