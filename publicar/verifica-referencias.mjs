// Portão das referências de capítulo na PROSA.
//
// Existe por causa de um erro real. A renumeração da edição 0.7 remapeou os
// números com uma substituição ancorada na palavra-chave ("capítulo NN"), de
// modo que o SEGUNDO número de toda referência composta — "capítulos 06 a 09",
// "caps. 08 e 12" — nunca foi visto. Resultado publicado: "capítulos 06–05" na
// leitura executiva da introdução, "capítulos 10 e 08" na bibliografia e
// "(caps. 08 e 08)" na rubrica do exercício final do livro.
//
// O build valida LINKS. Estas referências são prosa: para ele, texto comum.
// O critério de aceite que dizia cobri-las media um proxy.
//
// O que dá para verificar mecanicamente: o número existe? o intervalo sobe? o
// par repete o mesmo capítulo? O que NÃO dá: se a referência aponta para o
// capítulo semanticamente certo. Isso continua sendo leitura humana — e por
// isso o portão imprime o que verificou, para não passar por mais do que é.
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const falhasIniciais = [];

// O universo de capítulos que existem é o MAPA, não o sumário publicado.
//
// A primeira versão deste portão media o sumário — e isso confundia "publicado"
// com "existe". Neste handbook os dois são coisas diferentes de propósito: o
// mapa declara 77 vagas em três camadas, e o livro cresce publicando-as fora de
// ordem (ADR 0004). Um capítulo de método que diz "ciclagem é assunto do
// capítulo 10" está fazendo o trabalho que o mapa existe para permitir — dizer
// ao leitor ONDE a resposta vai morar. Barrar isso empurraria o texto a fingir
// que a lacuna não tem endereço.
//
// O que continua sendo defeito, e o portão continua pegando: número que não
// está no mapa (dedo trocado, remapeamento parcial), par repetido e intervalo
// decrescente.
const mapa = readFileSync(resolve(RAIZ, "livro/mapa-do-handbook.md"), "utf8");
const CAPITULOS = new Set(
  [...mapa.matchAll(/^\|[^|\n]*\|\s*(\d{2})\s+—\s/gm)].map((m) => Number(m[1]))
);
// Os já publicados, para o portão poder DIZER quantas referências apontam para
// vaga ainda não escrita — em vez de deixar o número invisível.
const sumario = JSON.parse(readFileSync(resolve(AQUI, "sumario.json"), "utf8"));
const PUBLICADOS = new Set(
  sumario.partes.flatMap((p) => p.itens)
    .map((i) => (i.titulo || "").match(/^\s*(\d+)\s*—/))
    .filter(Boolean).map((m) => Number(m[1]))
);
if (CAPITULOS.size < PUBLICADOS.size)
  falhasIniciais.push("o mapa declara menos capítulos do que o sumário publica — um dos dois está errado");

// O HISTORICO registra edições anteriores à renumeração e traz nota dizendo
// isso; seus números são de época e não devem ser conferidos contra o sumário
// de hoje. As specs e estudos antigos, pelo mesmo motivo, ficam fora.
const FONTES = [
  { dir: resolve(RAIZ, "livro"), arquivos: ["00-introducao.md", "bibliografia.md", "glossario.md", "GUIA-EDITORIAL.md", "exercicios.json"] },
  { dir: resolve(RAIZ, "livro/capitulos"), arquivos: null },
];

// "capítulo 07", "caps. 06 e 10", "capítulos 06 a 09", "capítulos 01–04".
// O acento vem em NFD no repositório: casar por classe negada, não por "í".
const RE = /cap[^\s]{0,6}tulos?\s+(\d{1,2})(?:\s*(?:[eaà]|–|—|-)\s*(\d{1,2}))?|caps?\.\s*(\d{1,2})(?:\s*(?:[eaà]|–|—|-)\s*(\d{1,2}))?/gi;

const falhas = [...falhasIniciais];
let refs = 0, compostas = 0, paraVaga = 0;

for (const { dir, arquivos } of FONTES) {
  const lista = arquivos || readdirSync(dir).filter((f) => f.endsWith(".md"));
  for (const arq of lista) {
    const caminho = resolve(dir, arq);
    if (!existsSync(caminho)) { falhas.push(`${arq}: fonte declarada não existe`); continue; }
    const linhas = readFileSync(caminho, "utf8").split("\n");
    linhas.forEach((linha, i) => {
      for (const m of linha.matchAll(RE)) {
        const a = Number(m[1] ?? m[3]);
        const b = m[2] ?? m[4] ? Number(m[2] ?? m[4]) : null;
        const onde = `${arq}:${i + 1}`;
        const texto = m[0].replace(/\s+/g, " ");
        refs++;
        if (!CAPITULOS.has(a)) falhas.push(`${onde}: "${texto}" — capítulo ${String(a).padStart(2, "0")} não existe no mapa do handbook`);
        else if (!PUBLICADOS.has(a)) paraVaga++;
        if (b === null) continue;
        compostas++;
        if (!CAPITULOS.has(b)) falhas.push(`${onde}: "${texto}" — capítulo ${String(b).padStart(2, "0")} não existe no mapa do handbook`);
        else if (!PUBLICADOS.has(b)) paraVaga++;
        if (b === a) falhas.push(`${onde}: "${texto}" — o par cita o mesmo capítulo duas vezes (sintoma clássico de remapeamento parcial)`);
        if (b < a) falhas.push(`${onde}: "${texto}" — intervalo/par em ordem decrescente`);
      }
    });
  }
}

if (falhas.length) {
  console.error(`✗ referências de capítulo: ${falhas.length} falha(s)`);
  falhas.forEach((f) => console.error("   " + f));
  process.exit(1);
}
console.log(`✓ referências de capítulo OK: ${refs} referências (${compostas} compostas) apontam para capítulos do mapa; ${paraVaga} para vaga ainda não publicada — a aderência semântica é leitura humana`);
