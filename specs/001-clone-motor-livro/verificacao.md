# Verificação 001 — evidência ("prove, não declare")

Saídas reais dos portões, executadas em 2026-08-01 nesta branch.

## Build do site + portão de qualidade por página

```
$ cd publicar && npm run build

✓ Grafo do livro: 11 nós, 30 arestas
✓ Livro gerado [pt]: 16 páginas + capa em docs/ (links internos OK)
✓ template verificado [pt]: 11 capítulos com C01/N02 + 5 páginas de aparato OK
```

Atende **CA-1**, **CA-2** e **CA-4** (o motor falha o build se um item do sumário não tiver arquivo, e a verificação por página checa hero, numeração, tempo de leitura, downloads e datação de cada capítulo).

## Testes do tutor

```
$ cd chat-companion/backend && python -m pytest -q

14 passed, 1 warning in 0.53s
```

Atende **CA-6**. Dois testes foram reescritos porque codificavam o gating do livro de origem (o loop de ferramentas só abria no cap. 2). Aqui a busca no texto vale desde a capa — o tutor precisa citar a fonte já na primeira pergunta —, e os testes passaram a verificar o gating novo: no cap. 0 estão ativos tutor e busca; a Nuvem entra no cap. 6; as injeções (cap. 8) seguem bloqueadas.

## Ausência de resíduo do livro de origem

```
$ grep -ril "harness" docs/ | grep -v "historico|teoria-das-restricoes.md"
(vazio)
```

Atende **CA-3**. As duas exceções filtradas são intencionais: o `HISTORICO.md` registra que o motor veio do livro *Engenharia de Harness*, e o Markdown do livro completo é a concatenação que inclui esse histórico.

## Objeto interativo

```
$ grep -o 'data-viz="[^"]*"' docs/02-causa-e-efeito.html
data-viz="classificar-conexao"

$ ls docs/assets/viz.js
docs/assets/viz.js   (compilado por esbuild)
```

Atende **CA-5**. Além da presença no HTML, o objeto foi exercitado ponta a ponta em navegador (Playwright/Chromium):

- resposta errada → alternativa correta marcada em verde, a escolhida em vermelho, e devolutiva explicativa exibida (*"É causa e efeito. A primeira parte PRODUZ a segunda por si só…"*);
- resposta certa → devolutiva de acerto;
- percurso completo → placar final (*"3 de 5 — vale reler a distinção antes de seguir: causa e efeito PRODUZ; pré-requisito HABILITA."*).

## Espelho de capacidades

`COMPANION_CAPS` (`publicar/build.mjs`) foi **gerado a partir** de `capabilities.py`, não transcrito à mão — as 11 capacidades e os capítulos de liberação são idênticos nos dois lados. Atende **CA-7**.

## Fontes

Cada conceito de TOC apresentado cita a obra de origem na primeira ocorrência, e a [bibliografia](../../livro/bibliografia.md) lista as fontes primárias (Goldratt, Dettmer, Scheinkopf, Cox & Schleier) e a fundamentação cognitiva (Kahneman). Nenhum material de terceiros é reproduzido. Atende **CA-8**.

## Verificação visual

Inspecionado em navegador: capa, página de capítulo (com a navegação modular na lateral) e o objeto interativo nos três estados. Três defeitos encontrados e corrigidos nesta rodada:

1. a capa ainda era a do livro de origem — substituída por arte própria em SVG (a corrente com o elo restritivo em âmbar);
2. o convite "this book is also available in English" aparecia sem existir edição EN — desativado enquanto o livro for monolíngue;
3. o DOI do livro de origem vazava no rodapé — passou a ser condicional.
