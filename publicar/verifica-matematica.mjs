// Portão da matemática renderizada.
//
// Existe por causa de um defeito que ficou PUBLICADO e ninguém viu: o motor
// não tinha renderizador de matemática nenhum. As fórmulas em `$...$` e
// `$$...$$` iam para o HTML como texto cru, e o leitor via, literalmente:
//
//     $$ \begin{cases} x_1 + x_2 = 10 \ x_1 + 2x_2 = 12 \end{cases} $$
//
// Dezessete blocos e mais de 550 expressões em linha, em quatro capítulos no
// ar. Nenhum dos sete portões olhava para isso — todos verificavam ESTRUTURA
// (seções, links, exercícios, ótimos) e nenhum verificava se o que o leitor vê
// é o que o autor escreveu.
//
// A lição, que vale além deste portão: os portões deste livro nasceram olhando
// para o que se pode extrair do MARKDOWN. Este é o primeiro que olha para o
// HTML GERADO — para o artefato que chega ao leitor. Foi preciso o autor abrir
// a página e apontar.
//
// O que se verifica:
//   1. nenhum delimitador de matemática sobrou cru no HTML;
//   2. nenhuma expressão virou erro do KaTeX (que marca `class="katex-error"`);
//   3. a folha de estilo e as fontes do KaTeX foram copiadas — sem elas a
//      fórmula renderiza com métricas erradas, que é pior do que texto cru;
//   4. imprime QUANTAS expressões renderizaram, para o portão não passar por
//      mais do que é.
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const DOCS = resolve(AQUI, "..", "docs");

if (!existsSync(DOCS)) {
  console.error("✗ matemática: docs/ ausente — rode o build antes");
  process.exit(1);
}

const falhas = [];
let expressoes = 0, paginas = 0;

// Fora de <code>/<pre>, um `$$` no HTML final só pode ser delimitador que não
// foi consumido. Dentro deles é legítimo (o livro mostra código e comandos).
const semCodigo = (html) =>
  html.replace(/<pre[\s\S]*?<\/pre>/g, "").replace(/<code[\s\S]*?<\/code>/g, "");

for (const arq of readdirSync(DOCS).filter((f) => f.endsWith(".html"))) {
  const html = readFileSync(resolve(DOCS, arq), "utf8");
  paginas++;
  expressoes += (html.match(/class="katex/g) || []).length;

  const limpo = semCodigo(html);

  const crus = limpo.match(/\$\$/g) || [];
  if (crus.length)
    falhas.push(`${arq}: ${crus.length} delimitador(es) "$$" no HTML final — a fórmula não renderizou`);

  // Erro do KaTeX: a expressão existe e está malformada. Pior que não ter
  // renderizado, porque o leitor vê a mensagem de erro em vermelho.
  const erros = limpo.match(/class="katex-error"/g) || [];
  if (erros.length)
    falhas.push(`${arq}: ${erros.length} expressão(ões) com erro de sintaxe do KaTeX`);
}

// Sem a folha de estilo e as fontes, o KaTeX gera marcação correta e aparência
// errada — e "aparência errada" numa fórmula é conteúdo errado.
for (const ativo of ["assets/katex.min.css", "assets/fonts"]) {
  if (!existsSync(resolve(DOCS, ativo)))
    falhas.push(`${ativo} não foi copiado para docs/ — a fórmula sai com métricas erradas`);
}

// ACOPLAMENTO ENTRE RENDERIZADOR E FOLHA DE ESTILO — a verificação que faltava,
// e cuja ausência deixou este portão passar VERDE sobre uma página quebrada.
//
// A primeira versão conferia que o arquivo CSS existe. Existia. O que não
// existia era correspondência: o `markdown-it-katex` carregava um KaTeX 0.6.0
// aninhado, e o CSS vinha do KaTeX 0.18 do topo. Marcação de uma versão,
// estilo de outra: os índices caíam abaixo da linha e o alinhamento colapsava.
// A fórmula renderizava, e renderizava ERRADO — que é pior do que não
// renderizar, porque parece conteúdo.
//
// Agora o portão exige que toda classe estrutural que o renderizador EMITE
// esteja DEFINIDA na folha de estilo publicada. É o teste que pega divergência
// de versão sem precisar comparar números de versão.
if (existsSync(resolve(DOCS, "assets/katex.min.css"))) {
  const css = readFileSync(resolve(DOCS, "assets/katex.min.css"), "utf8");
  // SÓ classes que o KaTeX de fato ESTILIZA. `mord`, `mrel` e `mbin` aparecem
  // no HTML e não têm regra nenhuma — são semânticas, herdadas do TeX. Incluí-las
  // gerava falso vermelho, e falso vermelho crônico é o que ensina a desligar o
  // portão. Verificado classe a classe contra a folha publicada.
  const ESTRUTURAIS = ["katex-html", "vlist-t", "vlist", "strut", "base", "sizing"];
  const htmlTudo = readdirSync(DOCS).filter((f) => f.endsWith(".html"))
    .map((f) => readFileSync(resolve(DOCS, f), "utf8")).join("");
  for (const c of ESTRUTURAIS) {
    const emitida = new RegExp(`class="[^"]*\\b${c}\\b`).test(htmlTudo);
    const definida = css.includes(`.${c}`);
    if (emitida && !definida)
      falhas.push(`o renderizador emite a classe "${c}" e a folha de estilo publicada não a define — ` +
                  `marcação de uma versão do KaTeX com estilo de outra`);
  }
  // As fontes são referenciadas pelo CSS em caminho relativo; se o diretório
  // veio de outra versão, os nomes não batem e o navegador cai no fallback.
  const pedidas = [...css.matchAll(/url\(fonts\/([^)]+?)\.woff2\)/g)].map((m) => m[1]);
  const presentes = new Set(existsSync(resolve(DOCS, "assets/fonts")) ? readdirSync(resolve(DOCS, "assets/fonts")) : []);
  const faltando = [...new Set(pedidas)].filter((f) => !presentes.has(`${f}.woff2`));
  if (faltando.length)
    falhas.push(`a folha de estilo pede ${faltando.length} fonte(s) que não estão em docs/assets/fonts: ${faltando.slice(0, 3).join(", ")}`);
}

if (falhas.length) {
  console.error(`✗ matemática: ${falhas.length} falha(s)`);
  falhas.forEach((f) => console.error("   " + f));
  process.exit(1);
}
console.log(`✓ matemática OK: ${expressoes} expressão(ões) renderizada(s) em ${paginas} páginas, 0 delimitador cru`);
