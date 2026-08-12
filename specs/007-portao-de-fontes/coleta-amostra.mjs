// Coleta os títulos registrados das entradas com DOI, para calibrar o limiar.
// Roda uma vez, com rede, e grava `amostra-titulos.json`. A calibração depois
// roda offline sobre esse arquivo — o experimento fica reexecutável.
//
// POR QUE `curl` E NÃO `fetch`. O `fetch` nativo do Node não honra a variável
// de proxy do ambiente; a conexão cai no proxy sem a semântica de CONNECT e
// volta `403 Host not in allowlist`. O `curl` usa o mesmo proxy e o mesmo
// pacote de certificados, e passa. Nada de TLS foi afrouxado — só trocamos de
// cliente. Em ambiente sem proxy os dois funcionam, então a escolha não custa
// portabilidade.
import { readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

function busca(url) {
  try {
    return JSON.parse(execFileSync("curl", [
      "-sS", "--max-time", "25", "--fail",
      "-H", "User-Agent: handbook-po/0.1 (verificacao de bibliografia)",
      url,
    ], { encoding: "utf8" }));
  } catch { return null; }
}

const AQUI = dirname(fileURLToPath(import.meta.url));
const BIB = resolve(AQUI, "..", "..", "livro", "bibliografia.md");

// Só o que está DECLARADO como DOI: `DOI [10.x/y](https://doi.org/10.x/y)`.
// Uma varredura ingênua por /10\.\d{4,9}\// pegaria também a linha 130, que é um
// link do Springer cujo caminho contém um DOI mas que a entrada NÃO declara como
// tal. Confundir os dois inventaria uma referência que o handbook não fez.
const RE_ENTRADA = /^(✓ᵐ|✓|⏳|❌|📖)\s+(.+?)(?=\n(?:✓ᵐ|✓|⏳|❌|📖|##|>|---|$))/gms;
const RE_DOI = /DOI\s*\[([^\]]+)\]/;

// ARMADILHA REAL, e ela derrubou a primeira versão desta coleta. Uma alternância
// única — /"([^"]+)"|\*\*\*([^*]+)\*\*\*|\*([^*]{12,})\*/ — casa o NOME DO AUTOR
// em negrito, não o título: em `**DANTZIG, George B.** "The Diet Problem"`, o
// terceiro ramo encontra uma posição de casamento mais à esquerda (o segundo
// asterisco do negrito) e vence, porque o regex escolhe pela POSIÇÃO antes de
// escolher pelo ramo. Resultado: doze títulos "declarados" que eram doze nomes
// de autor, e uma calibração sem sentido.
//
// A correção é ordem explícita, não alternância: tenta o título entre aspas no
// corpo inteiro; só então o itálico triplo (as entradas de fronteira, que não
// têm autor); e nunca um ramo capaz de casar negrito.
const EXTRATORES = [
  /"([^"]{8,})"/,            // "Título do artigo"
  /\*\*\*([^*]{8,})\*\*\*/,  // ***Título*** — entradas sem autor
];
function extraiTitulo(corpo) {
  for (const re of EXTRATORES) {
    const m = corpo.match(re);
    if (m) return m[1].replace(/\s+/g, " ").trim();
  }
  return "";
}

const texto = readFileSync(BIB, "utf8");
const entradas = [];
for (const m of texto.matchAll(RE_ENTRADA)) {
  const corpo = m[2];
  const doi = corpo.match(RE_DOI)?.[1]?.trim();
  if (!doi) continue;
  entradas.push({ selo: m[1], doi, titulo_declarado: extraiTitulo(corpo) });
}

console.log(`entradas com DOI declarado: ${entradas.length}`);

for (const e of entradas) {
  let reg = null, via = null;
  const cr = busca(`https://api.crossref.org/works/${encodeURIComponent(e.doi)}`);
  if (cr?.message?.title?.[0]) { reg = cr.message.title[0]; via = "crossref"; }
  if (!reg) {
    const oa = busca(`https://api.openalex.org/works/doi:${encodeURIComponent(e.doi)}`);
    if (oa?.title) { reg = oa.title; via = "openalex"; }
  }
  e.titulo_registrado = reg || null;
  e.via = via;
  console.log(`  ${reg ? "✓" : "✗"} ${e.doi}  ${via || "não resolveu"}`);
}

writeFileSync(resolve(AQUI, "amostra-titulos.json"), JSON.stringify({
  coletado_em: new Date().toISOString().slice(0, 10),
  entradas,
}, null, 2) + "\n");
console.log(`\nresolvidas: ${entradas.filter((e) => e.titulo_registrado).length}/${entradas.length}`);
