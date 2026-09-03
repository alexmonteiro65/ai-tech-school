# Beginner · Lesson 2 — "Your first prompt — how to talk to AI correctly"
## Audio narration script (~2 min)

Source lesson: [`levels/beginner/lesson-2.html`](../levels/beginner/lesson-2.html)
Presenter voice: AITS, the AI Tech School mascot (first person, matches
`video/ai-universe-script.md` and `video/beginner-lesson-1-script.md`)
Format note: this is a plain **audio** narration (read aloud by the site's
Piper TTS pipeline — see `scripts/generate_narration.py`), not an avatar
video script, so there's no on-screen-timing table here — just the
narration text per language, read straight through under the lesson's
"Listen to it explained" player.

---

## English

Hi, I'm A.I.T.S., your AI Tech School guide — here's the detailed walkthrough for this lesson. In the last lesson we covered what Claude actually is. Now let's put that to work: how do you actually talk to it? A prompt is just the instruction you give Claude, and here's the whole lesson in one line — vague prompts get vague results, specific prompts get results you can actually use.

So how do you write a specific one? Use four parts. Task: what you actually want done. Context: the details Claude needs to do it well. Format: how you want the answer shaped — length, structure. And optionally, tone: the voice you want it written in.

Let's compare two prompts. Vague: "write about dogs." Specific: "write a 100-word paragraph for a children's book about why dogs make loyal pets, in a warm, simple tone." Same topic, completely different result — because the second one actually tells Claude what you need.

One more thing before you try it yourself: treat the first response as a draft, not a final answer. If it's not quite right, don't start over — just refine your prompt with more detail.

On the page, you'll build a real prompt yourself using this four-part formula, then check your understanding with three quick questions. See you in Lesson 3: what an API actually is.

Before you try the quiz below, here's a quick preview of the three questions and their answers. Question 1: What usually causes a disappointing AI response? Is it The AI is broken, A vague or underspecified prompt, Using too many words, or Asking more than one question? The answer is A vague or underspecified prompt — Vague instructions leave Claude guessing at what you actually want — specificity is what improves results. Question 2: Which prompt is more likely to get a useful result? Is it "Write about dogs", "Write a 100-word, warm-toned paragraph for a children's book about why dogs make loyal pets", "Dogs", or "Tell me stuff"? The answer is "Write a 100-word, warm-toned paragraph for a children's book about why dogs make loyal pets" — It specifies the task, format, length, audience, and tone — all four parts of the formula. Question 3: What should you do if the first response isn't quite right? Is it Give up, Treat it as a draft and refine your prompt, Assume Claude can't help with this, or Start over in a different tool? The answer is Treat it as a draft and refine your prompt — Iterating on your prompt with more detail is normal and usually gets you where you want faster than starting over.

## Português (Brasil)

Oi, eu sou o A.I.T.S., seu guia da AI Tech School — aqui vai o passo a passo detalhado desta aula. Na aula passada, vimos o que o Claude realmente é. Agora vamos colocar isso em prática: como você fala com ele de verdade? Um prompt é só a instrução que você dá ao Claude, e aqui está a aula inteira em uma frase — prompts vagos geram resultados vagos, prompts específicos geram resultados que você realmente consegue usar.

Então, como você escreve um prompt específico? Use quatro partes. Tarefa: o que você realmente quer que seja feito. Contexto: os detalhes que o Claude precisa para fazer bem. Formato: como você quer que a resposta seja moldada — tamanho, estrutura. E, opcionalmente, tom: o estilo em que você quer que seja escrito.

Vamos comparar dois prompts. Vago: "escreva sobre cachorros." Específico: "escreva um parágrafo de 100 palavras para um livro infantil sobre por que cachorros são animais leais, em um tom caloroso e simples." Mesmo assunto, resultado completamente diferente — porque o segundo realmente diz ao Claude o que você precisa.

Mais uma coisa antes de você tentar sozinho: trate a primeira resposta como um rascunho, não como a resposta final. Se não estiver bem, não recomece do zero — só refine seu prompt com mais detalhes.

Na página, você vai montar um prompt de verdade usando essa fórmula de quatro partes, e depois verificar seu entendimento com três perguntas rápidas. Te vejo na Aula 3: o que é uma API, de verdade.

Antes de tentar o teste abaixo, aqui vai uma prévia rápida das três perguntas e suas respostas. Pergunta 1: O que geralmente causa uma resposta decepcionante da IA? É A IA está com defeito, Um prompt vago ou pouco específico, Usar palavras demais, ou Fazer mais de uma pergunta? A resposta é Um prompt vago ou pouco específico — Instruções vagas deixam o Claude tendo que adivinhar o que você quer — especificidade é o que melhora os resultados. Pergunta 2: Qual prompt tem mais chance de gerar um resultado útil? É "Escreva sobre cachorros", "Escreva um parágrafo de 100 palavras, em tom caloroso, para um livro infantil sobre por que cachorros são leais", "Cachorros", ou "Me conte umas coisas"? A resposta é "Escreva um parágrafo de 100 palavras, em tom caloroso, para um livro infantil sobre por que cachorros são leais" — Ele especifica a tarefa, o formato, o tamanho, o público e o tom — as quatro partes da fórmula. Pergunta 3: O que você deve fazer se a primeira resposta não ficar boa? É Desistir, Tratar como um rascunho e refinar seu prompt, Achar que o Claude não pode ajudar com isso, ou Recomeçar em outra ferramenta? A resposta é Tratar como um rascunho e refinar seu prompt — Iterar no seu prompt com mais detalhes é normal e geralmente chega no resultado mais rápido do que recomeçar.

## Español (Latinoamérica)

Hola, soy A.I.T.S., tu guía de AI Tech School — aquí va el recorrido detallado de esta lección. En la lección pasada vimos qué es Claude en realidad. Ahora vamos a ponerlo en práctica: ¿cómo le hablas de verdad? Un prompt es solo la instrucción que le das a Claude, y aquí está toda la lección en una frase — prompts vagos producen resultados vagos, prompts específicos producen resultados que realmente puedes usar.

Entonces, ¿cómo escribes uno específico? Usa cuatro partes. Tarea: lo que realmente quieres que se haga. Contexto: los detalles que Claude necesita para hacerlo bien. Formato: cómo quieres que se estructure la respuesta — extensión, estructura. Y, opcionalmente, tono: el estilo en el que quieres que esté escrito.

Comparemos dos prompts. Vago: "escribe sobre perros." Específico: "escribe un párrafo de 100 palabras para un libro infantil sobre por qué los perros son mascotas leales, en un tono cálido y simple." Mismo tema, resultado completamente distinto — porque el segundo sí le dice a Claude lo que necesitas.

Una cosa más antes de que lo intentes tú mismo: trata la primera respuesta como un borrador, no como la respuesta final. Si no queda del todo bien, no empieces de cero — solo refina tu prompt con más detalle.

En la página vas a armar un prompt real usando esta fórmula de cuatro partes, y luego vas a verificar tu comprensión con tres preguntas rápidas. Nos vemos en la Lección 3: qué es una API, en realidad.

Antes de intentar el cuestionario de abajo, aquí tienes un adelanto rápido de las tres preguntas y sus respuestas. Pregunta 1: ¿Qué suele causar una respuesta decepcionante de la IA? ¿Es La IA está fallando, Un prompt vago o poco específico, Usar demasiadas palabras, o Hacer más de una pregunta? La respuesta es Un prompt vago o poco específico — Las instrucciones vagas dejan a Claude adivinando qué quieres — la especificidad es lo que mejora los resultados. Pregunta 2: ¿Qué prompt tiene más probabilidades de dar un resultado útil? ¿Es "Escribe sobre perros", "Escribe un párrafo de 100 palabras, en tono cálido, para un libro infantil sobre por qué los perros son leales", "Perros", o "Cuéntame cosas"? La respuesta es "Escribe un párrafo de 100 palabras, en tono cálido, para un libro infantil sobre por qué los perros son leales" — Especifica la tarea, el formato, la extensión, la audiencia y el tono — las cuatro partes de la fórmula. Pregunta 3: ¿Qué deberías hacer si la primera respuesta no queda del todo bien? ¿Es Rendirte, Tratarla como un borrador y refinar tu prompt, Asumir que Claude no puede ayudarte con esto, o Empezar de nuevo en otra herramienta? La respuesta es Tratarla como un borrador y refinar tu prompt — Iterar tu prompt con más detalle es normal y suele llevarte al resultado más rápido que empezar de cero.
