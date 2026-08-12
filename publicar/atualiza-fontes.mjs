// O gerador do travamento de fontes. RODA COM REDE, sob demanda: `npm run fontes`.
//
// Não roda no build e não roda em integração contínua (CI, Continuous
// Integration). A razão é de incentivo, não de técnica: se o gerador rodasse no
// CI, o reparo natural diante de um build vermelho viraria "regerar o travamento
// até ficar verde" — que esvazia o portão pela porta dos fundos, do mesmo jeito
// que uma lista de exceções esvaziaria pela porta da frente. Ver ADR 0009, D8.
//
// TRÊS PERGUNTAS, TRÊS AUTORIDADES (ADR 0009, D2):
//   1. existe?          → doi.org/api/handles      — o registro, não um índice
//   2. de quem é?       → api.crossref.org/prefixes — só para a mensagem de erro
//   3. que trabalho é?  → Crossref /works → OpenAlex /works/doi:
//
// A primeira é a que importa. Crossref e OpenAlex são índices de METADADOS, com
// cobertura parcial por construção: um DOI da DataCite ou da mEDRA legitimamente
// não está lá. Perguntar existência a eles produz falso negativo por desenho.
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { leBibliografia, CHAVES_TRAVAMENTO } from "./fontes-comum.mjs";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const BIB = resolve(RAIZ, "livro/bibliografia.md");
const TRAVAMENTO = resolve(RAIZ, "livro/fontes.lock.json");
const REPOR = process.argv.includes("--repor");

if (process.env.CI) {
  console.error("✗ o gerador não roda em integração contínua (ADR 0009, D8).");
  console.error("  Regerar travamento até o build ficar verde é o mesmo buraco que uma allowlist.");
  process.exit(1);
}

// POR QUE `curl` E NÃO `fetch`. Diagnosticado nesta rodada: o `fetch` nativo do
// Node não honra a variável de proxy do ambiente; a conexão cai no proxy sem a
// semântica de CONNECT e volta `403 Host not in allowlist`. O `curl` usa o mesmo
// proxy e o mesmo pacote de certificados, e passa. Nenhuma verificação de TLS
// foi afrouxada e nenhuma variável foi removida — trocou-se de cliente.
function busca(url) {
  try {
    const txt = execFileSync("curl", [
      "-sS", "--max-time", "25", "--fail",
      "-H", "User-Agent: handbook-po/0.1 (verificacao de bibliografia)",
      url,
    ], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
    return { ok: true, dados: JSON.parse(txt) };
  } catch (e) {
    // `--fail` devolve 22 em erro HTTP. Qualquer outro código é falha de
    // transporte — e a distinção entre "não encontrei" e "não consegui
    // perguntar" é o que impede o falso verde (ADR 0009, D5.1).
    return { ok: false, transporte: e.status !== 22 };
  }
}

function existe(doi) {
  const r = busca(`https://doi.org/api/handles/${encodeURI(doi)}`);
  if (!r.ok) return r.transporte ? "indeterminado" : "indeterminado";
  if (r.dados?.responseCode === 1) return "sim";
  if (r.dados?.responseCode === 100) return "nao";
  return "indeterminado";
}

function registrante(doi) {
  const pre = doi.split("/")[0];
  const r = busca(`https://api.crossref.org/prefixes/${pre}`);
  return { prefixo: pre, registrante: r.ok ? (r.dados?.message?.name || null) : null };
}

// Devolve `{ md }` quando obteve metadados, `{ ausente: true }` quando os dois
// índices responderam e nenhum conhece o DOI, e `{ indeterminado: true }`
// quando NÃO FOI POSSÍVEL PERGUNTAR.
//
// A distinção existia em `busca()` e era descartada aqui — e foi assim que a
// revisão independente deixou o portão verde tendo verificado nada: com os dois
// índices fora do ar, as doze entradas viravam `registrado-sem-metadados`, com
// título e ano NULOS, e nada abortava. Era o bloqueio B3 do plano voltando pela
// única porta que as três defesas não cobriam.
function metadados(doi) {
  let houveTransporte = false;
  const cr = busca(`https://api.crossref.org/works/${encodeURI(doi)}`);
  if (cr.transporte) houveTransporte = true;
  if (cr.ok && cr.dados?.message) {
    const m = cr.dados.message;
    return { md: {
      fonte: "crossref",
      titulo: m.title?.[0] || null,
      primeiro_autor: m.author?.[0]?.family || null,
      autores: (m.author || []).map((a) => a.family).filter(Boolean),
      ano: m.issued?.["date-parts"]?.[0]?.[0] ?? null,
      container: m["container-title"]?.[0] || null,
    } };
  }
  const oa = busca(`https://api.openalex.org/works/doi:${encodeURI(doi)}`);
  if (oa.transporte) houveTransporte = true;
  if (oa.ok && oa.dados?.title) {
    const d = oa.dados;
    const fam = (d.authorships || []).map((a) => {
      const n = a.author?.display_name || "";
      return n.split(/\s+/).pop();
    }).filter(Boolean);
    return { md: {
      fonte: "openalex",
      titulo: d.title,
      primeiro_autor: fam[0] || null,
      autores: fam,
      ano: d.publication_year ?? null,
      container: d.primary_location?.source?.display_name || null,
    } };
  }
  return houveTransporte ? { indeterminado: true } : { ausente: true };
}

// --- canários (ADR 0009, D5.2) ---------------------------------------------
// Antes de escrever qualquer coisa, prova que o caminho de rede FUNCIONA. Sem
// isso, uma queda de serviço marcaria as doze entradas como inexistentes e a
// rodada entregaria um travamento catastroficamente errado com build verde.
const CANARIOS = ["10.1287/inte.20.4.43", "10.1002/nav.3800020406"];
console.log("canários:");
for (const c of CANARIOS) {
  const e = existe(c);
  // O canário precisa exercitar OS DOIS caminhos. Testar só a existência
  // deixava passar o cenário em que doi.org responde e os índices caem — e era
  // exatamente esse o buraco: tudo virava "registrado-sem-metadados", com
  // título e ano nulos, e o build ficava verde tendo verificado nada.
  const md = e === "sim" ? metadados(c) : null;
  const okMd = !!md?.md;
  console.log(`   ${e === "sim" && okMd ? "✓" : "✗"} ${c} → existe: ${e} · metadados: ${okMd ? md.md.fonte : "não obtidos"}`);
  if (e !== "sim" || !okMd) {
    console.error("\n✗ canário falhou: o caminho de rede não está confiável.");
    console.error("  Nada foi escrito. Tente de novo quando registro e índices responderem.");
    process.exit(1);
  }
}

const { entradas, defeitos } = leBibliografia(BIB);
if (defeitos.length) {
  console.error(`\n✗ bibliografia com ${defeitos.length} entrada(s) que não se consegue interpretar:`);
  defeitos.forEach((d) => console.error("   " + d));
  process.exit(1);
}

const anterior = existsSync(TRAVAMENTO)
  ? JSON.parse(readFileSync(TRAVAMENTO, "utf8"))
  : { fontes: [] };
const porDoi = new Map((anterior.fontes || []).map((f) => [f.doi.toLowerCase(), f]));

const hoje = new Date().toISOString().slice(0, 10);
const novas = [];
let rebaixamentos = 0;
const indeterminados = [];

console.log(`\n${entradas.length} entrada(s) com DOI declarado:`);
for (const e of entradas) {
  const ex = existe(e.doi);
  const velha = porDoi.get(e.doi.toLowerCase());

  if (ex === "indeterminado") {
    // Nunca gravado (D5.1). Mantém o que já havia; se não havia nada, a entrada
    // some do travamento e o PORTÃO reprova por ausência — que é o correto:
    // ausência de resposta não pode virar aprovação.
    indeterminados.push(e.doi);
    if (velha) { novas.push(velha); console.log(`   ~ ${e.doi} indeterminado — mantido como estava`); }
    else console.log(`   ~ ${e.doi} indeterminado — sem registro anterior, ficará ausente`);
    continue;
  }

  const { prefixo, registrante: reg } = registrante(e.doi);

  if (ex === "nao") {
    if (velha && velha.estado !== "inexistente" && !REPOR) rebaixamentos++;
    novas.push({ doi: e.doi, estado: "inexistente", prefixo, registrante: reg,
      titulo: null, primeiro_autor: null, ano: null, container: null,
      fonte: "doi.org", verificado_em: hoje });
    console.log(`   ✗ ${e.doi} NÃO EXISTE no registro`);
    continue;
  }

  const r = metadados(e.doi);

  if (r.indeterminado) {
    // NÃO consegui perguntar aos índices. Isso nunca vira estado gravado, e
    // nunca rebaixa o que já estava resolvido (ADR 0009, D5.1 e D5.4).
    indeterminados.push(e.doi);
    if (velha) { novas.push(velha); console.log(`   ~ ${e.doi} índices indisponíveis — mantido como estava`); }
    else console.log(`   ~ ${e.doi} índices indisponíveis — sem registro anterior, ficará ausente`);
    continue;
  }

  if (r.ausente) {
    if (velha && velha.estado === "resolvido" && !REPOR) rebaixamentos++;
    novas.push({ doi: e.doi, estado: "registrado-sem-metadados", prefixo, registrante: reg,
      titulo: null, primeiro_autor: null, ano: null, container: null,
      fonte: "doi.org", verificado_em: hoje });
    console.log(`   ○ ${e.doi} existe, e nenhum índice gratuito o conhece`);
    continue;
  }

  const md = r.md;
  novas.push({
    doi: e.doi, estado: "resolvido", prefixo, registrante: reg,
    titulo: md.titulo, primeiro_autor: md.primeiro_autor, ano: md.ano,
    container: md.container, fonte: md.fonte, verificado_em: hoje,
  });
  console.log(`   ✓ ${e.doi} ${md.fonte}`);
}

// --- limiar de degradação em massa (ADR 0009, D5.3) ------------------------
// Doze fabricações simultâneas não acontecem. Queda de serviço acontece.
const inexistentes = novas.filter((f) => f.estado === "inexistente").length;
// Conta rebaixamento de QUALQUER tipo — para `inexistente` e para
// `registrado-sem-metadados`. A primeira versão só contava o primeiro, e por
// isso doze entradas podiam perder título e ano numa tacada sem nada abortar.
if (!REPOR && rebaixamentos > 0 && (rebaixamentos > 2 || rebaixamentos / entradas.length > 0.2)) {
  console.error(`\n✗ ${rebaixamentos} entrada(s) rebaixadas numa só execução — isso é sintoma de serviço, não de fabricação.`);
  console.error("  Nada foi escrito. Se a mudança é real, rode com --repor e leia o diff.");
  process.exit(1);
}

// Ordem estável, para que o diff seja legível e a idempotência seja verificável.
novas.sort((a, b) => a.doi.toLowerCase().localeCompare(b.doi.toLowerCase()));

const saida = {
  gerado_por: "publicar/atualiza-fontes.mjs",
  contrato: CHAVES_TRAVAMENTO,
  fontes: novas.map((f) => Object.fromEntries(CHAVES_TRAVAMENTO.map((k) => [k, f[k] ?? null]))),
};
writeFileSync(TRAVAMENTO, JSON.stringify(saida, null, 2) + "\n");

// Linha legível por máquina, para a reconferência mensal. Sem ela, um DOI que
// não pôde ser CONSULTADO era reempurrado verbatim, o diff dava vazio, e o
// workflow anunciava "confere" sobre um título que o registro nunca devolveu —
// "não consegui perguntar" virando "conferido". Apontado pela revisão.
console.log(`\nRECONFERENCIA indeterminados=${indeterminados.length}${indeterminados.length ? " :: " + indeterminados.join(",") : ""}`);
console.log(`\n✓ travamento gravado: ${novas.length} entrada(s) · ` +
  `${novas.filter((f) => f.estado === "resolvido").length} resolvidas · ` +
  `${novas.filter((f) => f.estado === "registrado-sem-metadados").length} sem metadados · ` +
  `${inexistentes} inexistentes`);
