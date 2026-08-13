// Motor do livro — Markdown (livro/) -> site HTML navegável (docs/).
// App próprio (não framework): usa markdown-it como biblioteca de parsing;
// o motor em si — navegação, tema, callouts, ilhas de visualização — é nosso.
// Uso: node build.mjs                (passada PT -> docs/)
//      LIVRO_LANG=en node build.mjs  (passada EN -> docs/en/; RODAR APÓS a PT)
//
// i18n (spec 067): o PT é a fonte canônica; o EN é artefato derivado. Cada
// fonte EN carrega na 1ª linha `<!-- i18n fonte:<pt> edicao:X hash:<md5-8> -->`;
// o build compara o hash com o fonte PT atual e gera o SELO DE SINCRONIA
// (em dia / atrasado) — tradução velha nunca finge ser atual.
//
// Convenções de conteúdo reconhecidas:
//  - 1º blockquote "**Conteúdo revisado em/Content revised in" -> selo de data
//  - Seções ## de tipos pedagógicos -> callout próprio (Diátaxis/Bloom)
//  - Links internos .md -> reescritos para .html; links .html passam intactos
//  - <div data-viz="..."> -> ilha de visualização

import { readFileSync, writeFileSync, mkdirSync, cpSync, existsSync, rmSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, resolve, basename } from "node:path";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";
import { createRequire } from "node:module";
import MarkdownIt from "markdown-it";
import anchor from "markdown-it-anchor";
// Matemática. O motor viveu quatro capítulos SEM renderizador nenhum: as
// fórmulas em `$...$` e `$$...$$` iam para o HTML como texto cru, e o leitor
// via literalmente "$$ \begin{cases} ... \end{cases} $$" na página. Dezessete
// blocos e mais de 550 expressões em linha, publicados assim. Não era
// configuração errada — a capacidade NUNCA existiu, e nenhum portão olhava.
//
// SEGUNDA ARMADILHA, e ela custou uma publicação: a primeira correção usou o
// `markdown-it-katex`, de 2017, que carrega um KaTeX 0.6.0 ANINHADO no próprio
// node_modules. O CSS era copiado do KaTeX do topo (0.18). Resultado: HTML de
// 2016 servido com folha de estilo de 2024 — os índices caíam abaixo da linha
// e o alinhamento colapsava, porque o sistema de `vlist`/`strut` mudou entre
// as versões. A fórmula RENDERIZAVA, e renderizava errado, que é pior do que
// não renderizar: parece conteúdo.
//
// Duas defesas, e a segunda é a que importa:
//   1. plugin mantido (`@vscode/markdown-it-katex`), com um KaTeX só;
//   2. o CSS é resolvido DO MESMO MÓDULO que renderiza (`createRequire`), e
//      não de um caminho fixo. Assim renderizador e folha de estilo não podem
//      divergir por instalação.
import katexPlugin from "@vscode/markdown-it-katex";
// Interop CJS/ESM: este pacote chega com o `default` embrulhado duas vezes
// (`{ default: { default: fn } }`). Desembrulhar de forma defensiva evita o
// `TypeError: plugin.apply is not a function`, que é o erro que aparece quando
// se passa o objeto em vez da função.
const katex = katexPlugin?.default ?? katexPlugin;
import * as esbuild from "esbuild";
import { gerarGrafo } from "./grafo.mjs";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const EN = process.env.LIVRO_LANG === "en";
// Ambientes sem Chromium (build do Vercel) geram o site sem PDFs: SEM_PDF=1.
// O link de download some junto, para não apontar para arquivo inexistente.
const COM_PDF = process.env.SEM_PDF !== "1";
const LANG = EN ? "en" : "pt";
const SAIDA = resolve(RAIZ, EN ? "docs/en" : "docs");
const A = EN ? "../assets/" : "assets/"; // assets são compartilhados na raiz de docs/

const sumario = JSON.parse(readFileSync(resolve(AQUI, EN ? "sumario.en.json" : "sumario.json"), "utf8"));
// Exercícios (spec 005): registro editorial em livro/exercicios.json. Aqui o
// motor renderiza o CARTÃO (título + enunciado + botão); os critérios de
// avaliação ficam no servidor e nunca são publicados no site.
const ARQ_EXERCICIOS = resolve(RAIZ, "livro/exercicios.json");
const EXERCICIOS = existsSync(ARQ_EXERCICIOS)
  ? JSON.parse(readFileSync(ARQ_EXERCICIOS, "utf8")).reduce((m, e) => (m[e.id] = e, m), {})
  : {};
// Bilíngue: o motor suporta PT+EN, mas a v1 deste livro sai só em PT. Quando o
// sumário do outro idioma não existe, o livro é monolíngue e o seletor de idioma
// vira um selo sem link (em vez de apontar para páginas que não foram geradas).
const ARQ_OUTRO = resolve(AQUI, EN ? "sumario.json" : "sumario.en.json");
const BILINGUE = existsSync(ARQ_OUTRO);
const sumarioOutro = BILINGUE ? JSON.parse(readFileSync(ARQ_OUTRO, "utf8")) : sumario;

// Lista linear de itens publicáveis (para prev/next); itens `externo` ficam só na navegação.
const slugDe = (arquivo) => basename(arquivo).replace(/\.md$/, "").toLowerCase();
const itens = sumario.partes.flatMap((p) => p.itens.map((i) => ({ ...i, parte: p.nome }))).filter((i) => i.arquivo);
itens.forEach((i) => (i.slug = slugDe(i.arquivo)));
const slugsPublicados = new Set(itens.map((i) => i.slug));

// Par de idioma por POSIÇÃO no sumário (os dois sumários são espelhados).
const parDe = { index: "index", sumario: "sumario" };
sumario.partes.forEach((p, pi) =>
  p.itens.forEach((i, ii) => {
    const o = sumarioOutro.partes[pi]?.itens?.[ii];
    if (i.arquivo && o?.arquivo) parDe[slugDe(i.arquivo)] = slugDe(o.arquivo);
  })
);
const hrefOutroIdioma = (slug) => (EN ? `../${parDe[slug] || "sumario"}.html` : `en/${parDe[slug] || "sumario"}.html`);

const GITHUB_BASE = "https://github.com/GHDaru/operationalresearchaibook/blob/main/";
const SITE = "https://operationalresearchaibook.vercel.app/";
const DOI = "";

// Dicionário do chrome (spec 067). O conteúdo vem do Markdown; isto é só a moldura.
const T = EN
  ? {
      htmlLang: "en",
      temaAria: "Toggle theme",
      linkCapa: "↩ cover",
      sumarioTitulo: "Contents",
      seloVivo: "Living book — see History",
      estadoArte: "revised in",
      revisao: "revised",
      minLeitura: "min read",
      dlMd: "Download this chapter's source Markdown",
      dlPdf: "Open this chapter's PDF",
      capKicker: "Ch.",
      anterior: "← previous",
      proximo: "next →",
      rodape: `Living book · generated from Markdown by our own engine · <a href="https://github.com/GHDaru/operationalresearchaibook">source on GitHub</a>`,
      bibliografiaHtml: "bibliography.html",
      verCitacao: "see in the Bibliography",
      splashDesc: "An empirical study of the discipline of building the <em>scaffolding</em> around AI agents — theory, a benchmark of real harnesses, and a hands-on build from scratch.",
      splashAlt: "Cover of Harness Engineering: a glowing amber AI core wrapped in an engineering harness with loop, tool, permission, memory and verification modules, over a dark-blue blueprint background.",
      entrarLivro: "Enter the book →",
      benchmarkBtn: "Glossário",
      guiaBtn: "Editorial Guide",
      hrefComparativo: "comparative.html",
      hrefGuia: "editorial-guide.html",
      hrefHistorico: "../historico.html",
      newsKicker: "🗞 News",
      newsPt: " · item in Portuguese",
      verRadar: "see the full Radar →",
      nestaEdicao: "This edition",
      historicoNome: "History",
      creditos: `<strong><a href="author.html">Gilsiley Henrique Darú</a></strong> — editing, direction and orchestration · <a class="splash-linkedin" href="https://www.linkedin.com/in/gilsiley-dar%C3%BA/">LinkedIn</a><br><strong>Claude (Anthropic)</strong> — research and text generation (co-authorship)`,
      atualizadoEm: "updated on",
      kickerEntrada: "Living book",
      comecar: "▶ Start from the beginning — 00",
      pdfLivro: "pdf/operations-research.pdf",
      mdLivro: "md/operations-research.md",
      pdfLivroTitulo: "Full book as PDF",
      mdLivroTitulo: "Full book as Markdown (LLM-friendly)",
      continueLendo: "Continue reading",
      retomar: "Resume ▶",
      trilha: [
        ["01-foundations.html", "Track · 1", "Foundations", "The book's vocabulary and thesis."],
        ["02-agent-loop.html", "Track · 2", "Capabilities", "The 16 components, one per chapter."],
        ["comparative.html", "Track · 3", "Benchmark", "Real harnesses, compared."],
        ["https://github.com/GHDaru/operationalresearchaibook/tree/main/harness-zero", "Track · 4", "Hands-on", "Build harness-zero, step by step."],
      ],
      partesCartao: new Set(["Opening", "Chapters by capability"]),
      pillsRotulo: "Benchmark · Apparatus · About",
      dataLocale: "en-US",
      sincOk: (ed) => `🌐 English translation · in sync with the Portuguese original (edition ${ed})`,
      sincAtras: (ed) => `⏳ The Portuguese original has changed since this translation (made at edition ${ed}) — the latest content is in the PT version`,
      lerPt: "read in PT",
      outroIdioma: "PT",
      outroIdiomaTitulo: "Ler em português",
    }
  : {
      htmlLang: "pt-BR",
      temaAria: "Alternar tema",
      linkCapa: "↩ capa",
      sumarioTitulo: "Sumário",
      seloVivo: "Livro vivo — ver Histórico",
      estadoArte: "revisado em",
      revisao: "revisão",
      minLeitura: "min de leitura",
      dlMd: "Baixar o Markdown-fonte deste capítulo",
      dlPdf: "Abrir o PDF deste capítulo",
      capKicker: "Cap.",
      anterior: "← anterior",
      proximo: "próximo →",
      rodape: `Livro vivo · gerado do Markdown pelo motor próprio · <a href="https://github.com/GHDaru/operationalresearchaibook">fonte no GitHub</a>`,
      bibliografiaHtml: "bibliografia.html",
      verCitacao: "ver na Bibliografia",
      splashDesc: "O handbook vivo de Pesquisa Operacional — modelar com intenção e entender o algoritmo o suficiente para desconfiar dele. Fundamentos, métodos, módulos aplicados e a literatura corrente.",
      splashAlt: "Capa de Pesquisa Operacional: um poliedro luminoso, em âmbar, sobre fundo azul-escuro com traços de blueprint.",
      entrarLivro: "Entrar no livro →",
      benchmarkBtn: "Glossário",
      guiaBtn: "Guia Editorial",
      hrefComparativo: "glossario.html",
      hrefGuia: "guia-editorial.html",
      hrefHistorico: "historico.html",
      newsKicker: "🗞 Novidade",
      newsPt: "",
      verRadar: "ver o Radar completo →",
      nestaEdicao: "Nesta edição",
      historicoNome: "Histórico",
      creditos: `<strong><a href="autor.html">Gilsiley Henrique Darú</a></strong> — edição, direção e orquestração · <a class="splash-linkedin" href="https://www.linkedin.com/in/gilsiley-dar%C3%BA/">LinkedIn</a><br><strong>Claude (Anthropic)</strong> — pesquisa e geração de texto (co-autoria)`,
      atualizadoEm: "atualizado em",
      kickerEntrada: "Livro vivo",
      comecar: "▶ Começar do início — 00",
      pdfLivro: "pdf/pesquisa-operacional.pdf",
      mdLivro: "md/pesquisa-operacional.md",
      pdfLivroTitulo: "Livro completo em PDF",
      mdLivroTitulo: "Livro completo em Markdown (bom para LLMs)",
      continueLendo: "Continue lendo",
      retomar: "Retomar ▶",
      trilha: [
        ["00-introducao.html", "Comece por aqui", "Introdução", "Para quem é, como se estuda, e o que o handbook exige de si mesmo."],
        ["mapa-do-handbook.html", "O destino", "Mapa do handbook", "As vagas declaradas, em três camadas: núcleo, aplicados e fronteira."],
        ["radar.html", "Como se atualiza", "Radar científico", "Artigo lido vira linha datada — com o que ele muda no livro."],
        ["guia-editorial.html", "Como se escreve", "Guia Editorial", "O esqueleto de capítulo, os exercícios e a curadoria de vídeo."],
      ],
      partesCartao: new Set(["Abertura", "Parte I — Fundamentos", "Parte II — Programação Linear"]),
      pillsRotulo: "Aparato · Sobre",
      dataLocale: "pt-BR",
      sincOk: null,
      sincAtras: null,
      lerPt: "",
      outroIdioma: "EN",
      outroIdiomaTitulo: "Read in English",
    };

// Selo de maturidade do capítulo (ADR 0013, D2).
//
// O leitor precisa saber, ANTES de investir a leitura, em que estado o capítulo
// está. Um handbook que cresce por lote tem, por construção, capítulos em
// estados diferentes ao mesmo tempo — e disfarçar isso seria a versão editorial
// do falso verde que os portões deste repositório existem para impedir.
//
// A escada é cumulativa: 🔵 é 🟡 mais experimento que regenera cada número; ✅ é
// 🔵 mais revisão em contexto fresco. O selo é declarado no `sumario.json` e
// verificado por `verifica-capitulos.mjs` — não é adjetivo de prosa.
const MATURIDADE = {
  v0: { emoji: "🟡", rotulo: "v0",
        explica: "Esqueleto completo: 3 objetivos, 3 exercícios, \"quando não serve\" e origem com procedência. Ainda sem número medido próprio." },
  medido: { emoji: "🔵", rotulo: "medido",
            explica: "Todo número deste capítulo se regenera rodando um experimento do po-zero. Ainda sem revisão independente." },
  verificado: { emoji: "✅", rotulo: "verificado",
                explica: "Medido, revisto em contexto fresco por quem não escreveu, e com os portões provados quebrando." },
};

// Chat-companion (feature 017): URL do backend + espelho leve do registro de
// capacidades (fonte-de-verdade do gating é o backend; aqui é só exibição).
const COMPANION_BACKEND = sumario.companion_backend || "";
const COMPANION_CAPS = [
  { chave: "tutor", rotulo: "Tutor do handbook", libera: 0 },
  { chave: "busca_livro", rotulo: "Busca no livro", libera: 0 },
  { chave: "mapa", rotulo: "Mapa do handbook", libera: 0 },
  { chave: "exercicios", rotulo: "Exercícios", libera: 1 },
  { chave: "o_que_e_po", rotulo: "O que é (e o que não é) PO", libera: 1 },
  { chave: "ciclo_modelagem", rotulo: "O ciclo de modelagem", libera: 2 },
  { chave: "anatomia_modelo", rotulo: "Anatomia de um modelo", libera: 3 },
  { chave: "classificacao", rotulo: "Classificação e escolha de método", libera: 4 },
  { chave: "complexidade", rotulo: "Complexidade para quem modela", libera: 5 },
  { chave: "ferramentas", rotulo: "Ferramentas de trabalho", libera: 6 },
  { chave: "formulacao", rotulo: "Formulação de modelos", libera: 7 },
  { chave: "geometria", rotulo: "Geometria e método gráfico", libera: 8 },
  { chave: "simplex", rotulo: "Simplex de quadro", libera: 9 },
  { chave: "casos_especiais", rotulo: "Casos especiais e degenerescência", libera: 10 },
  { chave: "simplex_revisado", rotulo: "Simplex revisado", libera: 11 },
  { chave: "dualidade", rotulo: "Dualidade e preço-sombra", libera: 12 },
  { chave: "sensibilidade", rotulo: "Análise de sensibilidade", libera: 13 },
  { chave: "pontos_interiores", rotulo: "Pontos interiores", libera: 14 },
  { chave: "modelagem_aplicada", rotulo: "Padrões de modelagem", libera: 15 },
  { chave: "convexidade", rotulo: "Convexidade", libera: 38 },
  { chave: "leitura_critica", rotulo: "Leitura crítica de artigo", libera: 77 },
];
const capituloDe = (titulo) => parseInt((String(titulo).match(/^\s*(\d+)/) || [])[1], 10) || 0;
function companionSnippet(chapter) {
  // Sem backend configurado (`companion_backend` no sumário), o widget não é
  // injetado: um botão de chat que não responde é pior do que nenhum botão.
  // Basta preencher a URL no sumário para o tutor aparecer em todas as páginas.
  if (!COMPANION_BACKEND) return "";
  const cfg = JSON.stringify({ backend: COMPANION_BACKEND, chapter, mode: "progressivo", lang: LANG, capabilities: COMPANION_CAPS });
  return `<script>window.COMPANION=${cfg.replace(/</g, "\\u003c")}</script>
<link rel="stylesheet" href="${A}companion.css">
<script src="${A}companion.js" defer></script>`;
}

// Cartão de exercício: <div data-exercicio="cap02.ex01"></div> no Markdown vira
// um bloco com título, enunciado e o botão que entrega o exercício ao tutor.
// Progressive enhancement: sem JS o cartão continua legível; só o botão some.
const ROTULO_TIPO = {
  traduzir: "Traduzir", implicito: "Encontrar o implícito",
  "achar-erro": "Achar o erro", "contexto-proprio": "No seu contexto",
};

function cartaoExercicio(id) {
  const ex = EXERCICIOS[id];
  if (!ex) throw new Error(`exercício desconhecido no Markdown: ${id}`);
  const v = ex.variante ? `<span class="exerc-v">${ex.variante}</span>` : "";
  const t = ex.tipo ? `<span class="exerc-tipo">${ROTULO_TIPO[ex.tipo] || ex.tipo}</span>` : "";
  // O `erro_provavel` e os `criterios` NUNCA são publicados: são a rubrica com
  // que o tutor avalia, e o leitor não deve poder lê-la antes de responder.
  return `<li class="exerc" data-exercicio="${id}" data-titulo="${(ex.titulo || "").replace(/"/g, "&quot;")}">
  <p class="exerc-k">${v}${t}<span class="exerc-selo" hidden></span></p>
  <h4 class="exerc-t">${md.renderInline(ex.titulo || "")}</h4>
  <div class="exerc-e">${md.render(ex.enunciado || "")}</div>
  <button class="exerc-bt" type="button" hidden>Praticar no tutor →</button>
</li>`;
}

// Bateria: a série inteira de um capítulo, na ordem das variantes. O contrato
// vem antes — ele calibra a expectativa (tempo, o que fazer se travar) e é o
// que impede o leitor de ler a bateria como prova.
function bateria(serie) {
  const itens = Object.values(EXERCICIOS)
    .filter((e) => (e.serie || "") === serie)
    .sort((a, b) => String(a.variante || "").localeCompare(String(b.variante || "")));
  if (!itens.length) throw new Error(`bateria sem exercícios: ${serie}`);
  const min = itens.length * 10;
  return `<section class="bateria" aria-label="Bateria de exercícios">
  <p class="bateria-k">Bateria de exercícios · ${itens.length} tarefas</p>
  <p class="bateria-c">Cada tarefa treina uma coisa diferente, e a dificuldade sobe.
  Reserve algo como ${min} minutos. Se travar por mais de dez numa delas, registre o que
  você tentou e siga — o tutor conduz a partir do que você escreveu, e travar também
  informa. A devolutiva compara o seu <em>raciocínio</em> com o do capítulo, não as suas
  palavras com um gabarito.</p>
  <ol class="bateria-l">${itens.map((e) => cartaoExercicio(e.id)).join("\n")}</ol>
</section>`;
}

// linkify: false de propósito — num livro técnico, "AGENTS.md"/"app.py" no texto
// não devem virar links. Links reais já são explícitos no Markdown.
const md = new MarkdownIt({ html: true, linkify: false, typographer: false }).use(katex, {
  // Renderiza o que entende e marca em vermelho o que não entende, em vez de
  // derrubar o build por uma chave desbalanceada. Quem reprova é o portão
  // `verifica-matematica.mjs` — e ele olha o HTML, que é onde o leitor olha.
  throwOnError: false,
}).use(anchor, {
  permalink: anchor.permalink.ariaHidden({ symbol: "#", placement: "after" }),
  slugify: (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, ""),
});

// Reescrita de links internos: .md publicado -> .html local; .html passa
// intacto (links cross-idioma como ../historico.html); resto -> GitHub.
const defaultLinkOpen = md.renderer.rules.link_open || ((t, i, o, e, s) => s.renderToken(t, i, o));
md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
  const href = tokens[idx].attrGet("href");
  if (href && !/^https?:|^#|^mailto:|^\/\//.test(href) && !/\.html(#|$)/.test(href)) {
    const [alvo, hash] = href.split("#");
    const ancora = hash ? "#" + hash : "";
    const slug = basename(alvo).replace(/\.md$/i, "").toLowerCase();
    if (/\.md$/i.test(alvo) && slugsPublicados.has(slug)) {
      tokens[idx].attrSet("href", slug + ".html" + ancora);
    } else {
      const repoRel = path.posix.normalize(path.posix.join(env.srcDir || ".", alvo)).replace(/^(\.\.\/)+/, "");
      tokens[idx].attrSet("href", GITHUB_BASE + repoRel + ancora);
    }
  }
  return defaultLinkOpen(tokens, idx, options, env, self);
};

// Datação (PT e EN): o selo do livro vivo.
const RE_CAPTURA = /(?:Conteúdo revisado em|Content revised in)/;
function extrairData(markdown) {
  const m = markdown.match(new RegExp("^>\\s*\\*\\*(" + RE_CAPTURA.source + "[^*]+)\\*\\*([^\\n]*)", "m"));
  return m ? (m[1] + m[2]).replace(/\[.*?\]\(.*?\)/g, "").replace(/·\s*$/, "").trim() : null;
}
function extrairDatas(markdown) {
  const cap = (markdown.match(new RegExp(RE_CAPTURA.source + "\\s+(\\d{4}-\\d{2}(?:-\\d{2})?)")) || [])[1] || null;
  const rev = (markdown.match(/(?:última revisão|last revised)\s+(\d{4}-\d{2}-\d{2})/) || [])[1] || null;
  return { cap, rev };
}

// Selo de sincronia (spec 067): lê o cabeçalho i18n da fonte EN e compara o
// hash com o fonte PT ATUAL. Sem cabeçalho -> sem selo (páginas PT).
function seloDeSincronia(markdown, slug) {
  const m = markdown.match(/^<!--\s*i18n\s+fonte:(\S+)\s+edicao:(\S+)\s+hash:([0-9a-f]{8})\s*-->/);
  if (!m) return "";
  const [, fonte, edicao, hash] = m;
  let atual = "";
  try {
    atual = createHash("md5").update(readFileSync(resolve(RAIZ, fonte))).digest("hex").slice(0, 8);
  } catch {}
  const emDia = atual && atual === hash;
  const alvoPt = `../${parDe[slug] || "sumario"}.html`;
  return emDia
    ? `<div class="sinc sinc-ok">${T.sincOk(edicao)}</div>`
    : `<div class="sinc sinc-atras">${T.sincAtras(edicao)} — <a href="${alvoPt}">${T.lerPt}</a></div>`;
}

// Carga estimada de leitura (Sweller): ~200 palavras/min, sem blocos de código.
function tempoDeLeitura(markdown) {
  const semCodigo = markdown.replace(/```[\s\S]*?```/g, " ");
  const palavras = (semCodigo.match(/\S+/g) || []).length;
  return Math.max(1, Math.round(palavras / 200));
}

// Callouts pedagógicos (PT/EN).
const TIPOS = [
  { re: /objetivos de aprendizagem|learning objectives/i, cls: "callout-objetivos" },
  { re: /^verifica|^check your understanding/i, cls: "callout-verificacao" },
  { re: /mão na massa|hands-on/i, cls: "callout-pratica" },
  { re: /o que roubar|what to steal/i, cls: "callout-roubar" },
  { re: /^apêndice|^appendix/i, cls: "callout-apendice" },
];
function marcarCallouts(html) {
  return html.replace(/<h2([^>]*)>([\s\S]*?)<\/h2>/g, (full, attrs, titulo) => {
    const limpo = titulo.replace(/<[^>]+>/g, "").trim();
    const tipo = TIPOS.find((t) => t.re.test(limpo));
    return tipo ? `<h2${attrs} data-callout="${tipo.cls}">${titulo}</h2>` : full;
  });
}

// Siglas "abertas" (spec 023) — fonte única; o glossário mirroreia.
// Siglas "abertas" — fonte única; o glossário espelha (livro/glossario.md).
// Regra: só entram siglas cuja forma é inequívoca em prosa portuguesa. Siglas de
// duas letras ambíguas (SA, TS, AG, CP, PI, PD) ficam de fora de propósito: o
// motor casa por palavra inteira e as marcaria em falsos positivos.
const SIGLAS = {
  PO: "Pesquisa Operacional", PL: "Programação Linear",
  LP: "Linear Programming", MILP: "Mixed Integer Linear Programming",
  MINLP: "Mixed Integer Nonlinear Programming", KKT: "Karush-Kuhn-Tucker",
  VRP: "Vehicle Routing Problem", TSP: "Travelling Salesman Problem",
  GRASP: "Greedy Randomized Adaptive Search Procedure",
  LNS: "Large Neighborhood Search", ALNS: "Adaptive Large Neighborhood Search",
  VNS: "Variable Neighborhood Search", ILS: "Iterated Local Search",
  ACO: "Ant Colony Optimization", PSO: "Particle Swarm Optimization",
  MDP: "Markov Decision Process", DEA: "Data Envelopment Analysis",
  AHP: "Analytic Hierarchy Process",
  TOPSIS: "Technique for Order of Preference by Similarity to Ideal Solution",
  EOQ: "Economic Order Quantity", CPM: "Critical Path Method",
  PERT: "Program Evaluation and Review Technique",
  ML4CO: "Machine Learning for Combinatorial Optimization",
  ML: "Machine Learning", RL: "Reinforcement Learning",
  LLM: "Large Language Model", RAG: "Retrieval-Augmented Generation",
  AMPL: "A Mathematical Programming Language", CBC: "Coin-or Branch and Cut",
  HiGHS: "High performance software for linear optimization",
  API: "Application Programming Interface", DOI: "Digital Object Identifier",
  ISBN: "International Standard Book Number", ORCID: "Open Researcher and Contributor ID",
  ADR: "Architecture Decision Record", DoD: "Definition of Done",
  CPU: "Central Processing Unit — unidade central de processamento",
  CI: "Continuous Integration — integração contínua",
  GB: "gigabyte", JSON: "JavaScript Object Notation",
};
const RE_SIGLAS = new RegExp("\\b(" + Object.keys(SIGLAS).sort((a, b) => b.length - a.length).join("|") + ")\\b", "g");
const TAGS_PROT = /^(pre|code|a|abbr|h[1-6]|script|style)$/i;
function ligarCitacoes(texto) {
  return texto.replace(/arXiv\s+(\d{4}\.\d{4,5})/g,
    (m, id) => `<a class="cita" href="${T.bibliografiaHtml}" title="${T.verCitacao}">arXiv ${id}</a>`);
}

// C08 LeituraExecutiva (spec 043) — PT/EN.
function marcarLeituraExec(html) {
  return html.replace(/(<h3[^>]*>[\s\S]*?<\/h3>)([\s\S]*?)(?=<h[1-3][\s>]|$)/g, (full, h3, resto) => {
    const limpo = h3.replace(/<[^>]+>/g, "").trim();
    if (!/^(leitura executiva|executive summary)/i.test(limpo)) return full;
    return `<div class="leitura-exec">${h3}${resto}</div>`;
  });
}

function abrirSiglas(html) {
  const re = /<\/?([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>/g;
  const sub = (t) => ligarCitacoes(t).replace(RE_SIGLAS, (s) => `<abbr title="${SIGLAS[s]}">${s}</abbr>`);
  let out = "", last = 0, m, prot = 0;
  while ((m = re.exec(html))) {
    const txt = html.slice(last, m.index);
    out += prot > 0 ? txt : sub(txt);
    const tag = m[1].toLowerCase();
    if (TAGS_PROT.test(tag) && !m[0].endsWith("/>")) prot += m[0][1] === "/" ? -1 : 1;
    if (prot < 0) prot = 0;
    out += m[0];
    last = re.lastIndex;
  }
  return out + (prot > 0 ? html.slice(last) : sub(html.slice(last)));
}

// "02 — Loop do Agente" -> { num: "02", texto: "Loop do Agente" }.
const dividirTitulo = (t) => {
  const p = t.split("—");
  if (p.length < 2) return { num: "", texto: t.trim() };
  return { num: /^\s*\d+\s*$/.test(p[0]) ? p[0].trim() : "", texto: p.slice(1).join("—").trim() };
};

// Seletor de idioma (spec 067): pill PT·EN presente em todas as páginas.
function pillIdioma(slug) {
  const atual = EN ? "EN" : "PT";
  if (!BILINGUE) return `<nav class="lang-pill" aria-label="Idioma"><span class="lang-atual">${atual}</span></nav>`;
  const alvo = hrefOutroIdioma(slug);
  const outro = T.outroIdioma;
  return `<nav class="lang-pill" aria-label="Idioma / Language"><span class="lang-atual">${atual}</span><a href="${alvo}" title="${T.outroIdiomaTitulo}" data-lang-alvo="${EN ? "pt" : "en"}">${outro}</a></nav>`;
}
function hreflangs(slug) {
  if (!BILINGUE) return `<link rel="alternate" hreflang="pt-BR" href="${SITE}${slug}.html">`;
  const aqui = EN ? `en/${slug}.html` : `${slug}.html`;
  const la = EN ? `${parDe[slug] || "sumario"}.html` : `en/${parDe[slug] || "sumario"}.html`;
  const pt = EN ? la : aqui, en = EN ? aqui : la;
  return `<link rel="alternate" hreflang="pt-BR" href="${SITE}${pt}">
<link rel="alternate" hreflang="en" href="${SITE}${en}">
<link rel="alternate" hreflang="x-default" href="${SITE}${pt}">`;
}

function pagina({ tituloLivro, tituloPagina, corpo, navLateral, prev, next, data, ehIndex, chapter = 0, slug = "", hero = null, sinc = "" }) {
  const navBtn = (item, dir) => {
    if (!item) return `<span></span>`;
    const { num, texto } = dividirTitulo(item.titulo);
    const badge = num ? `<span class="pag-badge">${num}</span>` : "";
    const rotulo = dir === "prev" ? T.anterior : T.proximo;
    return `<a class="pagcard${dir === "next" ? " next" : ""}" href="${item.slug}.html">${badge}<span class="pag-tx"><span class="pag-dir">${rotulo}</span><span class="pag-tt">${texto}</span></span></a>`;
  };
  const selo = data ? `<div class="selo-data" title="${T.seloVivo}">🕒 ${data}</div>` : "";
  return `<!doctype html>
<html lang="${T.htmlLang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${tituloPagina} · ${tituloLivro}</title>
<meta name="description" content="${sumario.subtitulo}">
<meta property="og:type" content="website">
<meta property="og:title" content="${tituloLivro}">
<meta property="og:description" content="${sumario.subtitulo}">
<meta property="og:image" content="${SITE}assets/capa-social.png">
<meta name="twitter:card" content="summary_large_image">
${hreflangs(slug)}
<link rel="icon" type="image/svg+xml" href="${A}favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="${A}favicon-32.png">
<link rel="apple-touch-icon" href="${A}apple-touch-icon.png">
<link rel="stylesheet" href="${A}katex.min.css">
<link rel="stylesheet" href="${A}estilo.css">
</head><body${ehIndex ? ' class="pagina-index"' : hero ? ' class="pagina-capitulo"' : ""} data-slug="${slug}" data-lang="${LANG}" data-titulo="${tituloPagina.replace(/"/g, "&quot;")}">
<button id="alt-tema" aria-label="${T.temaAria}">◐</button>
${pillIdioma(slug)}
<div class="layout">
  <aside class="sidebar">
    <a class="marca" href="sumario.html">${tituloLivro}</a>
    <a class="link-capa" href="index.html">${T.linkCapa}</a>
    ${navLateral}
  </aside>
  <main class="conteudo">
    ${sinc}
    ${hero || selo}
    <article class="markdown">${corpo}</article>
    <nav class="pagcards">${navBtn(prev, "prev")}${navBtn(next, "next")}</nav>
    <footer class="rodape">${T.rodape}</footer>
  </main>
</div>
<script src="${A}app.js"></script>
<script src="${A}viz.js" defer></script>
<script src="${A}uso.js" defer></script>
<script src="${A}grafo.js" defer></script>
${companionSnippet(chapter)}
</body></html>`;
}

// Versão do livro: fonte única = a última edição declarada em HISTORICO.md (PT, canônico).
function versaoDoLivro() {
  try {
    const hist = readFileSync(resolve(RAIZ, "livro/HISTORICO.md"), "utf8");
    const m = hist.match(/^###\s+Edição\s+(\d+)\.(\d+)/m);
    if (m) return `v${m[1]}.${m[2]}.0`;
  } catch {}
  return "v0.0.0";
}

function dataDaUltimaModificacao() {
  let d;
  try {
    const iso = execSync("git log -1 --format=%cI", { cwd: RAIZ, stdio: ["ignore", "pipe", "ignore"] })
      .toString()
      .trim();
    d = iso ? new Date(iso) : new Date();
  } catch {
    d = new Date();
  }
  return new Intl.DateTimeFormat(T.dataLocale, { dateStyle: "long" }).format(d);
}

// Jornal vivo (specs 061/062): fontes operacionais são PT; na edição EN o
// conteúdo do item permanece PT com marcação honesta (decisão da spec 067).
function noticiaDoRadar() {
  try {
    const radar = readFileSync(resolve(RAIZ, "radar/RADAR.md"), "utf8"); // ausente até haver jornal vivo
    for (const linha of radar.split("\n")) {
      const cels = linha.split("|").map((c) => c.trim());
      if (cels.length < 7 || !/^\d{4}-\d{2}-\d{2}$/.test(cels[1])) continue;
      if (cels[2].includes("(inicial)")) continue;
      const impacto = (cels[4].match(/[ABC]/) || [])[0] || "";
      return { data: cels[1], itemHtml: md.renderInline(cels[2]), impacto };
    }
  } catch {}
  return null;
}
function ultimaEdicao() {
  try {
    const hist = readFileSync(resolve(RAIZ, "livro/HISTORICO.md"), "utf8");
    const m = hist.match(/^###\s+Edição\s+(\d+\.\d+)\s+—\s+(\d{4}-\d{2}-\d{2})\s+·\s+(.+)$/m);
    if (m) return { versao: `v${m[1]}.0`, data: m[2], titulo: m[3].replace(/\s*\(spec \d+\)\s*$/, "") };
  } catch {}
  return null;
}
const noticia = noticiaDoRadar();
const edicao = ultimaEdicao();
const impactoRotulo = (i) => (EN ? `impact ${i}` : `impacto ${i}`);

// Tela-capa (splash) full-screen: porta de entrada do site, sem sidebar.
function paginaSplash() {
  const versao = versaoDoLivro();
  const atualizado = dataDaUltimaModificacao();
  return `<!doctype html>
<html lang="${T.htmlLang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${sumario.titulo}</title>
<meta name="description" content="${sumario.subtitulo}">
<meta property="og:type" content="website">
<meta property="og:title" content="${sumario.titulo}">
<meta property="og:description" content="${sumario.subtitulo}">
<meta property="og:image" content="${SITE}assets/capa-social.png">
<meta name="twitter:card" content="summary_large_image">
${hreflangs("index")}
<link rel="icon" type="image/svg+xml" href="${A}favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="${A}favicon-32.png">
<link rel="apple-touch-icon" href="${A}apple-touch-icon.png">
<link rel="stylesheet" href="${A}katex.min.css">
<link rel="stylesheet" href="${A}estilo.css">
</head><body class="splash-body" data-lang="${LANG}">
${pillIdioma("index")}
<main class="splash">
  <div class="splash-arte">
    <img src="${A}capa.svg" width="1024" height="1536" loading="eager"
      alt="${T.splashAlt}">
  </div>
  <div class="splash-texto">
    <h1>${sumario.titulo}</h1>
    <p class="splash-sub">${sumario.subtitulo}</p>
    <p class="splash-desc">${T.splashDesc}</p>
    <div class="splash-ctas">
      <a class="btn btn-primario btn-grande" href="sumario.html">${T.entrarLivro}</a>
      <a class="btn btn-escuro" href="${T.hrefComparativo}">${T.benchmarkBtn}</a>
      <a class="btn btn-escuro" href="${T.hrefGuia}">${T.guiaBtn}</a>
    </div>
    ${noticia
      ? `<div class="splash-news"><span class="splash-news-k">${T.newsKicker} · ${noticia.data}${noticia.impacto ? ` · <b class="splash-news-imp">${impactoRotulo(noticia.impacto)}</b>` : ""}${T.newsPt}</span><p>${noticia.itemHtml}</p><a class="splash-news-mais" href="${GITHUB_BASE}radar/RADAR.md">${T.verRadar}</a></div>`
      : ""}
    ${edicao
      ? `<p class="splash-vedicao">📖 ${T.nestaEdicao} (<b>${edicao.versao}</b> · ${edicao.data}): ${edicao.titulo} — <a href="${T.hrefHistorico}">${T.historicoNome}</a></p>`
      : ""}
    <p class="splash-creditos">${T.creditos}</p>
    <p class="splash-versao"><span class="splash-versao-num">${versao}</span> · ${T.atualizadoEm} ${atualizado}</p>
    ${DOI ? `<p class="splash-doi"><a href="https://doi.org/${DOI}">DOI: ${DOI}</a></p>` : ""}
  </div>
</main>
<script src="${A}app.js"></script>
${companionSnippet(0)}
</body></html>`;
}

function montarNavLateral(atualSlug) {
  return sumario.partes
    .map(
      (p) =>
        `<div class="nav-parte">${p.nome}</div><ul>` +
        p.itens
          .map((i) => {
            if (!i.arquivo) return `<li><a href="${i.externo}">${i.titulo}</a></li>`;
            const s = slugDe(i.arquivo);
            const ativo = s === atualSlug ? ' class="ativo"' : "";
            return `<li><a${ativo} href="${s}.html">${i.titulo}</a></li>`;
          })
          .join("") +
        `</ul>`
    )
    .join("");
}

// --- build ---
if (existsSync(SAIDA)) rmSync(SAIDA, { recursive: true, force: true });
mkdirSync(SAIDA, { recursive: true });

if (!EN) {
  mkdirSync(resolve(SAIDA, "assets"), { recursive: true });
  // O CSS vem do MESMO katex que o plugin usa — resolvido, não hardcoded.
  // Sem isso, uma instalação que aninhe outra versão volta a servir HTML de
  // uma versão com a folha de estilo de outra, e a fórmula sai deformada.
  const DIST_KATEX = dirname(createRequire(import.meta.url).resolve("katex"));
  cpSync(resolve(DIST_KATEX, "katex.min.css"), resolve(SAIDA, "assets/katex.min.css"));
  cpSync(resolve(DIST_KATEX, "fonts"), resolve(SAIDA, "assets/fonts"), { recursive: true });
  cpSync(resolve(AQUI, "tema/estilo.css"), resolve(SAIDA, "assets/estilo.css"));
  cpSync(resolve(AQUI, "tema/app.js"), resolve(SAIDA, "assets/app.js"));
  cpSync(resolve(AQUI, "tema/capa.svg"), resolve(SAIDA, "assets/capa.svg"));
  cpSync(resolve(AQUI, "tema/capa-social.png"), resolve(SAIDA, "assets/capa-social.png"));
  cpSync(resolve(AQUI, "tema/autor.png"), resolve(SAIDA, "assets/autor.png"));
  cpSync(resolve(AQUI, "tema/companion.css"), resolve(SAIDA, "assets/companion.css"));
  cpSync(resolve(AQUI, "tema/companion.js"), resolve(SAIDA, "assets/companion.js"));
  cpSync(resolve(AQUI, "tema/uso.js"), resolve(SAIDA, "assets/uso.js"));
  cpSync(resolve(AQUI, "tema/grafo.js"), resolve(SAIDA, "assets/grafo.js"));
  cpSync(resolve(AQUI, "tema/favicon.svg"), resolve(SAIDA, "assets/favicon.svg"));
  cpSync(resolve(AQUI, "tema/favicon-32.png"), resolve(SAIDA, "assets/favicon-32.png"));
  cpSync(resolve(AQUI, "tema/apple-touch-icon.png"), resolve(SAIDA, "assets/apple-touch-icon.png"));
  writeFileSync(resolve(SAIDA, ".nojekyll"), "");

  // Bundle das ilhas de visualização React (P2). Dados embutidos em build-time.
  await esbuild.build({
    entryPoints: [resolve(AQUI, "viz/index.jsx")],
    bundle: true,
    minify: true,
    format: "iife",
    loader: { ".json": "json" },
    jsx: "automatic",
    outfile: resolve(SAIDA, "assets/viz.js"),
    logLevel: "warning",
  });
}

let gerados = 0;
for (let k = 0; k < itens.length; k++) {
  const item = itens[k];
  const caminho = resolve(RAIZ, item.arquivo);
  if (!existsSync(caminho)) {
    console.warn(`  aviso: ausente, pulando -> ${item.arquivo}`);
    continue;
  }
  const bruto = readFileSync(caminho, "utf8");
  const data = extrairData(bruto);
  const sinc = EN ? seloDeSincronia(bruto, item.slug) : "";
  let corpo = marcarCallouts(md.render(bruto, { srcDir: dirname(item.arquivo) }));
  corpo = marcarLeituraExec(corpo); // C08 (spec 043)
  // Cartões de exercício (spec 005). Falha o build se o id não existir no
  // registro — é o portão que impede exercício fantasma no livro publicado.
  corpo = corpo.replace(/<div data-exercicio="([^"]+)"><\/div>/g, (_, id) => cartaoExercicio(id));
  corpo = corpo.replace(/<div data-bateria="([^"]+)"><\/div>/g, (_, serie) => bateria(serie));
  if (EN) corpo = corpo.replace(/(src|href)="assets\//g, '$1="../assets/'); // assets compartilhados na raiz
  if (EN) corpo = corpo.replace('<div data-viz="grafo-livro">', '<div data-viz="grafo-livro" data-src="../assets/grafo.en.json">');

  // C01 CabeçalhoDeCapítulo (spec 043, variante B): só páginas numeradas.
  let hero = null;
  const { num, texto } = dividirTitulo(item.titulo);
  if (num) {
    const { cap, rev } = extrairDatas(bruto);
    const mat = MATURIDADE[item.maturidade];
    const chips = [
      mat ? `<span class="cap-maturidade" title="${mat.explica}">${mat.emoji} ${mat.rotulo}</span>` : "",
      cap ? `<span title="${T.seloVivo}">🕒 ${T.estadoArte} ${cap}</span>` : "",
      rev ? `<span>${T.revisao} ${rev}</span>` : "",
      `<span>📖 ~${tempoDeLeitura(bruto)} ${T.minLeitura}</span>`,
      `<a class="cap-dl" href="md/${item.slug}.md" download title="${T.dlMd}">⬇ md</a>`,
      COM_PDF ? `<a class="cap-dl" href="pdf/${item.slug}.pdf" title="${T.dlPdf}">⬇ pdf</a>` : "",
    ].join("");
    hero = `<header class="cap-hero"><div class="cap-num" aria-hidden="true">${num}</div>
<div class="cap-kicker">${item.parte} · ${T.capKicker} ${num}</div>
<h1>${texto}</h1>
${item.teaser ? `<p class="cap-teaser">${item.teaser}</p>` : ""}
<div class="cap-meta">${chips}</div></header>`;
    corpo = corpo.replace(/<h1[^>]*>[\s\S]*?<\/h1>\s*/, "");
    corpo = corpo.replace(new RegExp("<blockquote>\\s*<p><strong>" + RE_CAPTURA.source + "[\\s\\S]*?<\\/blockquote>\\s*"), "");
  }

  if (item.slug !== "glossario" && item.slug !== "glossary") corpo = abrirSiglas(corpo);
  const html = pagina({
    tituloLivro: sumario.titulo,
    tituloPagina: item.titulo,
    corpo,
    navLateral: montarNavLateral(item.slug),
    prev: k === 0 ? { slug: "sumario", titulo: T.sumarioTitulo } : itens[k - 1],
    next: itens[k + 1],
    data,
    chapter: capituloDe(item.titulo),
    slug: item.slug,
    hero,
    sinc,
  });
  writeFileSync(resolve(SAIDA, `${item.slug}.html`), html);
  gerados++;
}

// Downloads (spec 045): fontes .md publicados + consolidado (por idioma).
mkdirSync(resolve(SAIDA, "md"), { recursive: true });
{
  const partesMd = [];
  for (const item of itens) {
    const caminho = resolve(RAIZ, item.arquivo);
    if (!existsSync(caminho)) continue;
    const bruto = readFileSync(caminho, "utf8");
    writeFileSync(resolve(SAIDA, "md", `${item.slug}.md`), bruto);
    partesMd.push(bruto.trim());
  }
  const cabecalho = `# ${sumario.titulo}\n\n> ${sumario.subtitulo}\n>\n> ${versaoDoLivro()}${DOI ? ` · DOI ${DOI}` : ""} · fonte: https://github.com/GHDaru/operationalresearchaibook · site: ${SITE}\n\n---\n\n`;
  writeFileSync(resolve(SAIDA, T.mdLivro), cabecalho + partesMd.join("\n\n---\n\n") + "\n");
}

// Knowledge Graph (spec 057): derivado do conteúdo PT a cada build. Na passada
// EN, os nós de capítulo são remapeados para rótulos/URLs EN (grafo.en.json).
if (!EN) {
  const grafo = gerarGrafo(itens, RAIZ, versaoDoLivro());
  writeFileSync(resolve(SAIDA, "assets/grafo.json"), JSON.stringify(grafo));
  console.log(`✓ Grafo do livro: ${grafo.nos.length} nós, ${grafo.arestas.length} arestas`);
} else {
  try {
    const grafo = JSON.parse(readFileSync(resolve(RAIZ, "docs/assets/grafo.json"), "utf8"));
    const tituloEnDe = {};
    itens.forEach((i) => (tituloEnDe[parDe[i.slug]] = i)); // slug PT -> item EN
    for (const n of grafo.nos) {
      if (n.tipo !== "capitulo") continue;
      const ptSlug = (n.url || "").replace(/\.html$/, "");
      const itemEn = tituloEnDe[ptSlug];
      if (itemEn) {
        n.url = `${itemEn.slug}.html`;
        n.rotulo = dividirTitulo(itemEn.titulo).num ? `${dividirTitulo(itemEn.titulo).num} ${dividirTitulo(itemEn.titulo).texto}` : itemEn.titulo;
      }
    }
    writeFileSync(resolve(RAIZ, "docs/assets/grafo.en.json"), JSON.stringify(grafo));
  } catch (e) {
    console.warn("  aviso: grafo.en.json não gerado:", e.message);
  }
}

// index = tela-capa (splash); porta de entrada (por idioma).
writeFileSync(resolve(SAIDA, "index.html"), paginaSplash());

// sumario.html = a EXPERIÊNCIA DE ENTRADA (spec 021), por idioma.
// O cartão aceita item SEM arquivo (`externo`). É o que permite ao livro publicar
// fora da ordem do mapa sem enganar o leitor: uma vaga declarada aparece como
// cartão marcado, apontando para o Mapa do handbook, em vez de sumir da parte —
// o que faria a lacuna parecer descuido em vez de plano.
const cartaoEnt = (i) => {
  const { num, texto } = dividirTitulo(i.titulo);
  const href = i.arquivo ? `${slugDe(i.arquivo)}.html` : i.externo;
  const classe = i.arquivo ? "ent-card" : "ent-card ent-card-vaga";
  return `<a class="${classe}" href="${href}">${num ? `<span class="ent-badge">${num}</span>` : ""}<span class="ent-ct">${texto}</span>${i.teaser ? `<span class="ent-cd">${i.teaser}</span>` : ""}</a>`;
};
const pillEnt = (i) =>
  i.arquivo
    ? `<a class="ent-pill" href="${slugDe(i.arquivo)}.html">${dividirTitulo(i.titulo).texto}</a>`
    : `<a class="ent-pill" href="${i.externo}">${dividirTitulo(i.titulo).texto}</a>`;
const blocosCartao = sumario.partes
  .filter((p) => T.partesCartao.has(p.nome))
  .map((p) => `<div class="ent-parte"><span>${p.nome}</span><i></i></div><div class="ent-grid">${p.itens.map(cartaoEnt).join("")}</div>`)
  .join("");
const pillsEnt = sumario.partes.filter((p) => !T.partesCartao.has(p.nome)).flatMap((p) => p.itens).map(pillEnt).join("");

// News da entrada (spec 061) — fontes PT; chrome no idioma da página.
const blocoNews = (noticia
  ? `<div class="ent-news"><span class="ent-news-k">${EN ? "🗞 Living-book Radar" : "🗞 Radar do livro vivo"} · ${noticia.data}${noticia.impacto ? ` · ${impactoRotulo(noticia.impacto)}` : ""}${T.newsPt}</span><p>${noticia.itemHtml}</p><a class="ent-news-mais" href="${GITHUB_BASE}radar/RADAR.md">${T.verRadar}</a></div>`
  : "") + (edicao
  ? `<p class="ent-vedicao">📖 ${T.nestaEdicao} (<b>${edicao.versao}</b> · ${edicao.data}): ${edicao.titulo} — <a href="${T.hrefHistorico}">${T.historicoNome}</a></p>`
  : "");

const trilhaHtml = T.trilha
  .map(([href, n, b, s]) => `<a class="ent-step" href="${href}"><span class="ent-step-n">${n}</span><b>${b}</b><span>${s}</span></a>`)
  .join("\n    ");

const corpoSumario = `<section class="entrada">
  <div class="ent-hero">
    <img class="ent-capa" src="${A}capa.svg" width="1024" height="1536" loading="eager" alt="${T.splashAlt}">
    <div class="ent-hero-txt">
      <div class="ent-kicker">${T.kickerEntrada} · ${versaoDoLivro()}${DOI ? ` · DOI ${DOI}` : ""}</div>
      <h1 class="ent-titulo">${sumario.titulo}</h1>
      <p class="ent-sub">${sumario.subtitulo}</p>
      <div class="ent-ctas">
        <a class="ent-btn ent-btn-a" href="${itens[0].slug}.html">${T.comecar}</a>
        <a class="ent-btn" href="${T.hrefComparativo}">${T.benchmarkBtn}</a>
        <a class="ent-btn" href="${T.hrefGuia}">${T.guiaBtn}</a>
        ${COM_PDF ? `<a class="ent-btn" href="${T.pdfLivro}" title="${T.pdfLivroTitulo}">⬇ PDF</a>` : ""}
        <a class="ent-btn" href="${T.mdLivro}" download title="${T.mdLivroTitulo}">⬇ Markdown</a>
      </div>
    </div>
  </div>
  ${blocoNews}
  <a class="ent-retomar" id="ent-retomar" href="#" hidden>
    <span class="ent-ret-l"><span class="ent-ret-lab">${T.continueLendo}</span><span class="ent-ret-cap" id="ent-ret-cap"></span></span>
    <span class="ent-btn ent-btn-a">${T.retomar}</span>
  </a>
  <div class="ent-trilha">
    ${trilhaHtml}
  </div>
  ${blocosCartao}
  <div class="ent-parte"><span>${T.pillsRotulo}</span><i></i></div>
  <div class="ent-pills">${pillsEnt}</div>
</section>`;
writeFileSync(
  resolve(SAIDA, "sumario.html"),
  pagina({
    tituloLivro: sumario.titulo,
    tituloPagina: T.sumarioTitulo,
    corpo: corpoSumario,
    navLateral: montarNavLateral("sumario"),
    prev: null,
    next: itens[0],
    data: null,
    ehIndex: true,
    slug: "sumario",
  })
);

// Portão de qualidade (T402): links internos .html apontam para páginas
// existentes NO MESMO idioma; "../" cruza para o outro idioma (validado lá).
const paginas = new Set(itens.map((i) => `${i.slug}.html`).concat("index.html", "sumario.html"));
const quebrados = [];
for (const i of [...itens, { slug: "index" }, { slug: "sumario" }]) {
  const arq = resolve(SAIDA, `${i.slug}.html`);
  if (!existsSync(arq)) continue;
  const html = readFileSync(arq, "utf8");
  for (const m of html.matchAll(/href="([^"]+)"/g)) {
    const href = m[1];
    if (/^https?:|^#|^mailto:|^\/\//.test(href)) continue;
    if (!/\.html(#|$)/.test(href)) continue;
    if (href.includes("../") || href.startsWith("en/")) continue; // cruza idiomas
    const alvo = basename(href.split("#")[0]);
    if (!paginas.has(alvo)) quebrados.push(`${i.slug}.html → ${href}`);
  }
}
if (quebrados.length) {
  console.error(`✗ ${quebrados.length} link(s) interno(s) quebrado(s):`);
  quebrados.forEach((q) => console.error("   " + q));
  process.exit(1);
}

console.log(`✓ Livro gerado [${LANG}]: ${gerados} páginas + capa em ${EN ? "docs/en/" : "docs/"} (links internos OK)`);
