// Verificação por página do template visual (spec 043; ADR 0005) — por idioma.
// Uso: node verifica-capitulos.mjs                (PT, docs/)
//      LIVRO_LANG=en node verifica-capitulos.mjs  (EN, docs/en/ — após o build EN)
// Qualquer falha encerra com exit 1 (portão de qualidade).

import { readFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, resolve, basename } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const EN = process.env.LIVRO_LANG === "en";
const COM_PDF = process.env.SEM_PDF !== "1";
const DOCS = resolve(RAIZ, EN ? "docs/en" : "docs");

const sumario = JSON.parse(readFileSync(resolve(AQUI, EN ? "sumario.en.json" : "sumario.json"), "utf8"));
const itens = sumario.partes.flatMap((p) => p.itens.map((i) => ({ ...i, parte: p.nome }))).filter((i) => i.arquivo);
const slugDe = (arquivo) => basename(arquivo).replace(/\.md$/, "").toLowerCase();

const RE_CAPTURA = EN ? /Content revised in/ : /Conteúdo revisado em/;
const RE_LEITURA = EN ? /^###\s+Executive summary/m : /^###\s+Leitura executiva/m;
const MIN_LEITURA = EN ? "min read" : "min de leitura";
const MD_LIVRO = EN ? "operations-research.md" : "pesquisa-operacional.md";
const PDF_LIVRO = EN ? "operations-research.pdf" : "pesquisa-operacional.pdf";

const RE_ORIGEM = /^##\s+De onde isto veio/m;

// DUAS listas, com significados diferentes — e misturá-las seria disfarçar
// escopo de dívida, que é o oposto do que estes portões existem para fazer.

// (a) Não é capítulo de método. O Princípio XII simplesmente não se aplica:
//     não há método cuja origem contar. Isto NÃO é dívida.
const NAO_E_CAPITULO_DE_METODO = new Set([
  "00-introducao",   // abertura do livro: para quem é, como se estuda
]);

// (b) É capítulo de método, publicado ANTES de o Princípio XII existir
//     (constituição 1.1.0, 2026-08-09). Isto É dívida, e é retroativa de
//     propósito: fingir que o princípio nasce só para o futuro seria
//     conveniente e desonesto.
//
//     **A lista está vazia, e isso é um estado que vale defender.** Os
//     capítulos 07 e 08 nasceram devendo e a dívida foi quitada no mesmo dia
//     (edição 0.9). Uma entrada nova aqui é sempre aceitável — o que não é
//     aceitável é ela ficar.
const SEM_ORIGEM_DECLARADO = new Set([]);
const isentoDeOrigem = (slug) => NAO_E_CAPITULO_DE_METODO.has(slug) || SEM_ORIGEM_DECLARADO.has(slug);

const falhas = [];
let capitulos = 0, aparato = 0;

for (const item of itens) {
  const slug = slugDe(item.arquivo);
  const arq = resolve(DOCS, `${slug}.html`);
  const fonte = resolve(RAIZ, item.arquivo);
  if (!existsSync(arq) || !existsSync(fonte)) { falhas.push(`${slug}: página ou fonte ausente`); continue; }
  const html = readFileSync(arq, "utf8");
  const md = readFileSync(fonte, "utf8");
  const num = (item.titulo.match(/^\s*(\d+)\s*—/) || [])[1];
  const erro = (m) => falhas.push(`${slug}: ${m}`);

  if (num) {
    capitulos++;
    if (!html.includes('class="cap-hero"')) erro("sem C01 (.cap-hero)");
    if (!html.includes(`<div class="cap-num" aria-hidden="true">${num}</div>`)) erro(`badge do número ${num} ausente`);
    if (!html.includes('class="cap-kicker"')) erro("kicker ausente");
    if (!html.includes(MIN_LEITURA)) erro("tempo de leitura ausente");
    if (RE_CAPTURA.test(md) && !html.toLowerCase().includes(EN ? "revised in" : "revisado em")) erro("datação não absorvida no C01");
    const h1s = (html.match(/<h1[\s>]/g) || []).length;
    if (h1s !== 1) erro(`esperado 1 <h1>, encontrado ${h1s}`);
    if (new RegExp("<blockquote>\\s*<p><strong>" + RE_CAPTURA.source).test(html)) erro("blockquote de datação sobrou no corpo");
    if (RE_LEITURA.test(md) && !html.includes('class="leitura-exec"')) erro("C08 não aplicado");
    if (!html.includes(`href="md/${slug}.md"`)) erro("link de download .md ausente");
    if (COM_PDF && !html.includes(`href="pdf/${slug}.pdf"`)) erro("link de download .pdf ausente");
    if (!existsSync(resolve(DOCS, "md", `${slug}.md`))) erro("md/*.md não copiado");
    if (existsSync(resolve(DOCS, "pdf")) && !existsSync(resolve(DOCS, "pdf", `${slug}.pdf`))) erro("pdf/*.pdf ausente");

    // Princípio XII — nenhum método cai do céu (constituição 1.1.0, ADR 0006).
    //
    // O capítulo de método conta o problema histórico concreto que forçou
    // alguém a inventar o método. Sem isso, o livro entrega procedimento — e
    // procedimento se decora.
    //
    // A dívida é declarada aqui, em código, e não em prosa: o que está na lista
    // é conhecido e tem prazo; o que não está e faltar, falha o build.
    if (!EN && !RE_ORIGEM.test(md) && !isentoDeOrigem(slug))
      erro("sem a seção \"De onde isto veio\" — Princípio XII (ou declare a dívida em SEM_ORIGEM_DECLARADO)");
    if (!EN && RE_ORIGEM.test(md) && SEM_ORIGEM_DECLARADO.has(slug))
      erro("ganhou a seção de origem e continua na lista de dívida — tire-o de SEM_ORIGEM_DECLARADO");
  } else {
    aparato++;
    if (html.includes('class="cap-hero"')) erro("página do aparato ganhou C01 indevidamente");
    if (new RegExp("^>\\s*\\*\\*" + RE_CAPTURA.source, "m").test(md) && !html.includes('class="selo-data"')) erro("selo de datação (C02) sumiu");
  }
  if (!html.includes('class="pagcards"')) erro("sem N02 (.pagcards)");
  if (!html.includes('class="lang-pill"')) erro("sem seletor de idioma (spec 067)");

  // Selo de sincronia (spec 067): toda página EN precisa do cabeçalho i18n
  // e o selo deve refletir o estado REAL (hash da fonte PT).
  if (EN) {
    const m = md.match(/^<!--\s*i18n\s+fonte:(\S+)\s+edicao:(\S+)\s+hash:([0-9a-f]{8})\s*-->/);
    if (!m) { erro("fonte EN sem cabeçalho i18n"); continue; }
    if (!existsSync(resolve(RAIZ, m[1]))) { erro(`cabeçalho i18n aponta fonte inexistente: ${m[1]}`); continue; }
    const atual = createHash("md5").update(readFileSync(resolve(RAIZ, m[1]))).digest("hex").slice(0, 8);
    const emDia = atual === m[3];
    if (emDia && !html.includes("sinc-ok")) erro("tradução em dia sem selo sinc-ok");
    if (!emDia && !html.includes("sinc-atras")) erro("tradução atrasada sem selo sinc-atras");
  }
}

// Knowledge Graph (spec 057) — só na passada PT (o EN remapeia o mesmo grafo).
if (!EN) {
  const gPath = resolve(DOCS, "assets/grafo.json");
  if (!existsSync(gPath)) falhas.push("assets/grafo.json ausente");
  else {
    const g = JSON.parse(readFileSync(gPath, "utf8"));
    // O que se verifica é INVARIANTE, não estado. A checagem anterior exigia
    // exatamente 15 capítulos e 10 arestas — números que descreviam o livro de
    // origem e passariam a mentir assim que ele crescesse ou encolhesse.
    //
    // Os invariantes reais do gerador são dois: (1) o grafo poda nós sem aresta,
    // logo todo nó publicado precisa aparecer em alguma aresta; (2) nenhum nó de
    // capítulo pode existir sem capítulo correspondente no sumário.
    const idsCap = new Set(itens.map((i) => (i.titulo.match(/^\s*(\d+)\s*—/) || [])[1]).filter(Boolean).map((n) => "cap-" + n));
    const emAresta = new Set(g.arestas.flatMap((a) => [a.de, a.para]));
    for (const n of g.nos) if (!emAresta.has(n.id)) falhas.push(`grafo: nó "${n.id}" sem aresta (a poda deveria tê-lo removido)`);
    for (const n of g.nos) if (n.tipo === "capitulo" && !idsCap.has(n.id)) falhas.push(`grafo: nó de capítulo "${n.id}" não existe no sumário`);
    // Com dois ou mais capítulos publicados, um grafo vazio significa extração
    // quebrada — e não livro sem relações.
    if (capitulos > 1 && !g.arestas.length) falhas.push(`grafo: nenhuma aresta com ${capitulos} capítulos publicados — extração quebrada`);
  }
} else if (!existsSync(resolve(RAIZ, "docs/assets/grafo.en.json"))) {
  falhas.push("assets/grafo.en.json ausente (remapeamento EN)");
}

// News na capa (spec 062): se as fontes do jornal parseiam, a capa noticia.
{
  const indexHtml = readFileSync(resolve(DOCS, "index.html"), "utf8");
  const radar = existsSync(resolve(RAIZ, "radar/RADAR.md")) ? readFileSync(resolve(RAIZ, "radar/RADAR.md"), "utf8") : "";
  const temNoticia = radar.split("\n").some((l) => {
    const c = l.split("|").map((x) => x.trim());
    return c.length >= 7 && /^\d{4}-\d{2}-\d{2}$/.test(c[1]) && !c[2].includes("(inicial)");
  });
  const hist = readFileSync(resolve(RAIZ, "livro/HISTORICO.md"), "utf8");
  const temEdicao = /^###\s+Edição\s+\d+\.\d+\s+—\s+\d{4}-\d{2}-\d{2}\s+·\s+.+$/m.test(hist);
  if (temNoticia && !indexHtml.includes('class="splash-news"')) falhas.push("capa: RADAR tem notícia mas index.html não tem .splash-news");
  if (temEdicao && !indexHtml.includes('class="splash-vedicao"')) falhas.push("capa: HISTORICO tem edição mas index.html não tem .splash-vedicao");
}

// Livro completo para download (spec 045), por idioma.
if (!existsSync(resolve(DOCS, "md", MD_LIVRO))) falhas.push(`consolidado md/${MD_LIVRO} ausente`);
const sum = readFileSync(resolve(DOCS, "sumario.html"), "utf8");
if ((COM_PDF && !sum.includes(`href="pdf/${PDF_LIVRO}"`)) || !sum.includes(`href="md/${MD_LIVRO}"`))
  falhas.push("entrada sem os botões de download do livro completo");

if (falhas.length) {
  console.error(`✗ verificação do template [${EN ? "en" : "pt"}]: ${falhas.length} falha(s)`);
  falhas.forEach((f) => console.error("   " + f));
  process.exit(1);
}
console.log(`✓ template verificado [${EN ? "en" : "pt"}]: ${capitulos} capítulos com C01/N02 + ${aparato} páginas de aparato OK`);
