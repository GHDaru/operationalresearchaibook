// Calibração do limiar de similaridade de título — o experimento que o plano
// devia ter trazido e não trouxe.
//
// O plano afirmava limiar 0,70 "o mesmo que o guia externo documenta". Isso é
// citação de terceiro sem fonte nomeável, num handbook cuja rodada inteira
// existe para eliminar números sem procedência. O guardião barrou, e com razão.
//
// Aqui o número é MEDIDO nesta bibliografia: para cada título declarado, calcula
// a similaridade contra (a) o título que a base pública devolveu — o caso
// legítimo, que precisa PASSAR — e (b) os títulos das outras entradas — o caso
// impostor, que precisa REPROVAR. O limiar defensável é qualquer valor entre o
// pior legítimo e o melhor impostor. Se essa janela não existir, a métrica é
// ruim e o limiar não salva.
//
// Roda contra o lock, offline. `--rede` regenera os dados de referência.
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..", "..");
const AMOSTRA = resolve(AQUI, "amostra-titulos.json");

// Mesma normalização que o portão vai usar. Se divergir, a calibração não vale
// para o portão — por isso os dois leem daqui.
export function normaliza(s) {
  return s
    .normalize("NFD").replace(/[̀-ͯ]/g, "")   // acento fora
    .replace(/[*_`]/g, "")                              // ênfase Markdown fora
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

// Similaridade por bigramas (Sørensen–Dice). Escolhida em vez de Levenshtein
// por uma razão prática: é insensível à ORDEM dos blocos, e diferenças
// legítimas entre o título declarado e o registrado são quase sempre de
// pontuação, subtítulo e maiúsculas — não de reordenação. Levenshtein pune
// título longo mais do que curto pelo mesmo erro absoluto.
export function similaridade(a, b) {
  const bi = (s) => {
    const g = new Map();
    for (let i = 0; i < s.length - 1; i++) g.set(s.slice(i, i + 2), (g.get(s.slice(i, i + 2)) || 0) + 1);
    return g;
  };
  const [x, y] = [bi(normaliza(a)), bi(normaliza(b))];
  const nx = [...x.values()].reduce((s, v) => s + v, 0);
  const ny = [...y.values()].reduce((s, v) => s + v, 0);
  if (!nx || !ny) return normaliza(a) === normaliza(b) ? 1 : 0;
  let comum = 0;
  for (const [g, n] of x) comum += Math.min(n, y.get(g) || 0);
  return (2 * comum) / (nx + ny);
}

// A DIVERGÊNCIA LEGÍTIMA TEM FORMA, e a primeira calibração mostrou qual.
//
// O único par legítimo que pontuou baixo (0,517) foi Spielman & Teng: o handbook
// declara "Smoothed Analysis of Algorithms: Why the Simplex Algorithm Usually
// Takes Polynomial Time" e o Crossref registra "Smoothed analysis of
// algorithms" — o registro CORTOU o subtítulo. Enquanto isso, o melhor impostor
// (0,560) foi "Origins of the simplex method" contra "New Finite Pivoting Rules
// for the Simplex Method": títulos diferentes que compartilham um jargão.
//
// Nenhum limiar separa os dois, porque a métrica de bigramas não distingue
// "é o mesmo título, truncado" de "são títulos diferentes sobre o mesmo tema".
// Distinguir isso é trabalho de OUTRO critério: contenção. Truncamento produz
// contenção; jargão compartilhado, não.
const MIN_CONTENCAO = 15; // aquém disso, contenção é coincidência
export function concorda(declarado, registrado, limiar) {
  const [a, b] = [normaliza(declarado), normaliza(registrado)];
  if (!a || !b) return { ok: false, via: "titulo ausente", s: 0 };
  const [curto, longo] = a.length <= b.length ? [a, b] : [b, a];
  if (curto.length >= MIN_CONTENCAO && longo.startsWith(curto))
    return { ok: true, via: "contencao (subtitulo cortado no registro)", s: 1 };
  const s = similaridade(a, b);
  return { ok: s >= limiar, via: `similaridade ${s.toFixed(3)}`, s };
}

if (process.argv.includes("--calibrar")) {
  if (!existsSync(AMOSTRA)) {
    console.error("✗ amostra ausente — rode a coleta com --rede primeiro");
    process.exit(1);
  }
  const amostra = JSON.parse(readFileSync(AMOSTRA, "utf8"));
  const pares = amostra.entradas.filter((e) => e.titulo_registrado);

  // Pontua com a regra composta: contenção vale 1, senão bigramas.
  const pontua = (x, y) => concorda(x, y, 0).s;

  const legitimos = pares.map((e) => ({
    doi: e.doi,
    s: pontua(e.titulo_declarado, e.titulo_registrado),
  })).sort((a, b) => a.s - b.s);

  // Impostores: todo título declarado contra todo título registrado que NÃO é o
  // seu. É o teste que importa — um limiar que aceita impostor não filtra nada.
  const impostores = [];
  for (const a of pares) for (const b of pares) {
    if (a.doi === b.doi) continue;
    impostores.push({ par: `${a.doi} × ${b.doi}`, s: pontua(a.titulo_declarado, b.titulo_registrado) });
  }
  impostores.sort((a, b) => b.s - a.s);

  const piorLegitimo = legitimos[0];
  const melhorImpostor = impostores[0];

  console.log(`amostra: ${pares.length} pares legítimos, ${impostores.length} pares impostores\n`);
  console.log("cinco piores legítimos (precisam PASSAR):");
  legitimos.slice(0, 5).forEach((l) => console.log(`   ${l.s.toFixed(3)}  ${l.doi}`));
  console.log("\ncinco melhores impostores (precisam REPROVAR):");
  impostores.slice(0, 5).forEach((i) => console.log(`   ${i.s.toFixed(3)}  ${i.par}`));

  const janela = piorLegitimo.s - melhorImpostor.s;
  console.log(`\npior legítimo   ${piorLegitimo.s.toFixed(3)}  (${piorLegitimo.doi})`);
  console.log(`melhor impostor ${melhorImpostor.s.toFixed(3)}  (${melhorImpostor.par})`);
  console.log(`janela          ${janela.toFixed(3)}`);

  if (janela <= 0) {
    console.error("\n✗ NÃO HÁ LIMIAR DEFENSÁVEL: um impostor pontua acima do pior legítimo.");
    console.error("  A métrica não separa esta bibliografia. Trocar de métrica, não de número.");
    process.exit(1);
  }
  // O limiar fica no meio da janela: máxima folga dos dois lados.
  const sugerido = Math.round(((piorLegitimo.s + melhorImpostor.s) / 2) * 100) / 100;
  console.log(`\n✓ limiar defensável: qualquer valor em (${melhorImpostor.s.toFixed(3)}, ${piorLegitimo.s.toFixed(3)}]`);
  console.log(`  sugerido (meio da janela): ${sugerido}`);
  writeFileSync(resolve(AQUI, "calibracao.json"), JSON.stringify({
    medido_em: amostra.coletado_em,
    pares_legitimos: pares.length,
    pares_impostores: impostores.length,
    pior_legitimo: piorLegitimo,
    melhor_impostor: melhorImpostor,
    janela,
    limiar_sugerido: sugerido,
  }, null, 2) + "\n");
}
