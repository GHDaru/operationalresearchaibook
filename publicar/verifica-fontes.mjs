// Portão das fontes — o identificador deixa de ser afirmação e vira medição.
//
// Existe porque o handbook tinha um sistema de selos de procedência honesto e
// NENHUM deles verificado por máquina. O `✓` ao lado de um identificador de
// objeto digital (DOI, Digital Object Identifier) era palavra de quem escreveu.
// Um dígito trocado passava; um DOI inventado passava. E não é hipótese: na
// rodada 004 uma URL de vídeo FOI inventada e só apareceu por acidente, ao
// tentar abri-la.
//
// O QUE ESTE PORTÃO NÃO COBRE, e precisa ser dito aqui para não criar confiança
// maior do que a cobertura: 12 das 31 obras da bibliografia têm DOI — 39%. Livros,
// páginas institucionais e identificadores do arXiv continuam sendo afirmação
// humana. E o incidente que motivou tudo — URL de vídeo — CONTINUA PASSANDO. O
// item "Portão de URL externa" segue aberto no ROADMAP.
//
// Roda OFFLINE, sempre. Compara a bibliografia contra `livro/fontes.lock.json`,
// que é versionado e gerado sob demanda por `npm run fontes`. Build que depende
// de rede é build que não compila no avião — e a rede falhou duas vezes durante
// a própria rodada que escreveu isto.
//
// Ver ADR 0009 (o portão) e ADR 0010 (a semântica do selo).
import { readFileSync, existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import {
  leBibliografia, leLegenda, tituloConcorda, normaliza,
  CHAVES_TRAVAMENTO, ESTADOS, MAX_TEXTO,
} from "./fontes-comum.mjs";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const BIB = process.env.FONTES_BIB || resolve(RAIZ, "livro/bibliografia.md");
const TRAVAMENTO = process.env.FONTES_LOCK || resolve(RAIZ, "livro/fontes.lock.json");

const falhas = [];
const avisos = [];

// --- 1. a legenda declara todos os selos que o arquivo usa -----------------
const { entradas, defeitos, selosUsados } = leBibliografia(BIB);
const declarados = leLegenda(BIB);
for (const s of [...selosUsados].sort()) {
  if (!declarados.has(s)) falhas.push(`selo "${s}" é usado no arquivo e NÃO está declarado na legenda`);
}

// --- 2. falha por ignorância é falha ---------------------------------------
// Um parser que não entendeu e por isso não reclamou é o modo clássico de um
// portão mentir. Entrada que declara DOI e não se deixa interpretar é defeito.
falhas.push(...defeitos);

// --- 3. o travamento existe ------------------------------------------------
if (!existsSync(TRAVAMENTO)) {
  console.error("✗ fontes: livro/fontes.lock.json ausente — rode `npm run fontes` antes do build");
  process.exit(1);
}
const trava = JSON.parse(readFileSync(TRAVAMENTO, "utf8"));
const fontes = trava.fontes || [];
const porDoi = new Map();
for (const f of fontes) {
  const k = String(f.doi).toLowerCase();
  // Sem esta checagem o último vence em silêncio, e uma entrada boa pode ser
  // rebaixada por uma duplicata sem que nada apareça.
  if (porDoi.has(k)) falhas.push(`travamento: ${f.doi} aparece mais de uma vez`);
  porDoi.set(k, f);
}

// --- 4. Princípio X vira teste, não promessa -------------------------------
// O Crossref devolve `abstract`, `license` e `funder`. Gravar a resposta crua
// versionaria texto de terceiro, que é exatamente o que o princípio proíbe.
for (const f of fontes) {
  for (const k of Object.keys(f)) {
    if (!CHAVES_TRAVAMENTO.includes(k))
      falhas.push(`travamento: ${f.doi} tem a chave "${k}", fora do contrato (Princípio X)`);
  }
  for (const [k, v] of Object.entries(f)) {
    if (typeof v === "string" && v.length > MAX_TEXTO)
      falhas.push(`travamento: ${f.doi} tem "${k}" com ${v.length} caracteres (teto ${MAX_TEXTO}) — cheira a texto de terceiro`);
  }
  if (!ESTADOS.includes(f.estado))
    falhas.push(`travamento: ${f.doi} com estado desconhecido "${f.estado}"`);
}

// --- 5. contagem independente do parser ------------------------------------
// A2 do plano. Se o parser perder uma entrada, esta conta não bate — sem ela, o
// portão ficaria verde tendo olhado menos do que devia.
const bruto = readFileSync(BIB, "utf8");
const contagemIndependente = (bruto.match(/doi\.org\/10\.[0-9]{4}/g) || []).length;
if (contagemIndependente !== entradas.length)
  falhas.push(`contagem divergente: o arquivo tem ${contagemIndependente} ligação(ões) doi.org e o parser leu ${entradas.length} entrada(s) com DOI`);

// --- 6. cada DOI da bibliografia, contra o travamento ----------------------
let resolvidos = 0, semMetadados = 0, inexistentes = 0;
const semMetadadosLista = [];

for (const e of entradas) {
  const f = porDoi.get(e.doi.toLowerCase());   // DOI é insensível a caixa
  if (!f) {
    falhas.push(`${e.onde}: DOI ${e.doi} não está no travamento — rode \`npm run fontes\``);
    continue;
  }

  if (f.estado === "inexistente") {
    inexistentes++;
    const quem = f.registrante ? `, do registrante ${f.registrante},` : "";
    falhas.push(
      `${e.onde}: o DOI ${e.doi} NÃO EXISTE no registro.\n` +
      `      O prefixo ${f.prefixo}${quem} é real — o sufixo provavelmente foi inventado.\n` +
      `      Reparo: apague o DOI da entrada e mantenha a obra com o localizador que ela tem.`
    );
    continue;
  }

  if (f.estado === "registrado-sem-metadados") {
    semMetadados++;
    semMetadadosLista.push(`${e.doi} (${f.registrante || "registrante desconhecido"})`);
    continue;   // existe: passa. Ausência de índice não é prova de fabricação.
  }

  resolvidos++;

  // `resolvido` SIGNIFICA que há metadados. Sem esta checagem, um travamento
  // com título e ano nulos passava como "12 resolvidos" sem um aviso sequer —
  // as comparações abaixo só agem quando os dois lados são não-nulos, e
  // `null == null` virava acordo tácito. Apontado pela revisão independente.
  if (f.titulo == null || f.ano == null) {
    falhas.push(`${e.onde}: ${e.doi} está como "resolvido" no travamento e não tem ${f.titulo == null ? "título" : "ano"} — ` +
                `estado e conteúdo divergem; rode \`npm run fontes\``);
    continue;
  }

  // O trabalho declarado é o trabalho registrado? É o único teste que pega o
  // DOI DESLOCADO — DOI real, de outro artigo, colado na entrada errada.
  const t = tituloConcorda(e.titulo, f.titulo);
  if (!t.ok)
    falhas.push(`${e.onde}: título diverge do registro (${t.via})\n` +
                `      handbook: "${e.titulo}"\n      registro:  "${f.titulo}"`);

  if (e.ano != null && f.ano != null && e.ano !== f.ano)
    falhas.push(`${e.onde}: ano diverge — handbook diz ${e.ano}, registro diz ${f.ano} (DOI ${e.doi})`);

  // Autor: exigimos que o sobrenome declarado esteja ENTRE os autores
  // registrados, e não que seja o primeiro. A ordem de autoria diverge entre
  // índices com frequência suficiente para que exigir posição gerasse falso
  // vermelho — e falso vermelho crônico ensina a desligar o portão.
  if (e.primeiro_autor && f.primeiro_autor) {
    const a = normaliza(e.primeiro_autor), b = normaliza(f.primeiro_autor);
    if (a !== b && !a.includes(b) && !b.includes(a))
      avisos.push(`${e.onde}: primeiro autor difere — handbook "${e.primeiro_autor}", registro "${f.primeiro_autor}"`);
  }

  // Idade avisa, nunca reprova: reprovar por calendário quebraria o build de
  // commits antigos e trocaria determinismo por relógio.
  if (f.verificado_em) {
    const dias = (Date.now() - Date.parse(f.verificado_em)) / 86400000;
    if (dias > 180) avisos.push(`${e.doi}: verificado há ${Math.round(dias)} dias — entra na janela de revisão`);
  }
}

// Travamento com DOI que a bibliografia não tem mais: lixo, não defeito.
for (const f of fontes) {
  if (!entradas.some((e) => e.doi.toLowerCase() === String(f.doi).toLowerCase()))
    avisos.push(`travamento tem ${f.doi}, que não está mais na bibliografia — rode \`npm run fontes\``);
}

// --- saída -----------------------------------------------------------------
if (falhas.length) {
  console.error(`✗ fontes: ${falhas.length} falha(s)`);
  falhas.forEach((f) => console.error("   " + f));
  process.exit(1);
}
avisos.forEach((a) => console.log("   ⚠ " + a));
if (semMetadadosLista.length)
  console.log(`   ○ existem no registro, sem metadados em índice gratuito: ${semMetadadosLista.join(", ")}`);
console.log(
  `✓ fontes OK: ${entradas.length} DOI(s) na bibliografia · ${fontes.length} no travamento · ` +
  `${resolvidos} resolvido(s) · ${semMetadados} sem metadados · ${inexistentes} inexistente(s) — ` +
  `URL comum e arXiv seguem sem portão`
);
