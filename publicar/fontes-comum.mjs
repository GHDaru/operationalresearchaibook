// Contrato compartilhado entre o portão (offline) e o gerador (com rede).
//
// É a ÚNICA fronteira entre os dois. O plano da rodada 007 congela este arquivo
// primeiro justamente por isso: se o gerador extrair o título de um jeito e o
// portão comparar de outro, o portão passa a medir a divergência entre dois
// parsers, e não entre o livro e o registro.
//
// Nada aqui toca a rede.
import { readFileSync } from "node:fs";

// ---------------------------------------------------------------------------
// Os selos. `✓ᵐ` precisa vir ANTES de `✓` na alternância: o segundo é prefixo
// do primeiro, e um regex que tentasse `✓` primeiro leria toda entrada `✓ᵐ`
// como `✓` seguido de um "ᵐ" solto no corpo — promovendo, em silêncio, a
// entrada mais frágil do sistema à mais forte.
export const SELOS = ["✓ᵐ", "✓", "⏳", "❌", "📖"];
const ALT_SELOS = SELOS.map((s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|");

// Uma entrada começa com selo no início da linha e vai até o próximo começo de
// entrada, título de seção, citação em bloco, régua — ou o fim do arquivo.
//
// ARMADILHA QUE JÁ COBROU SEU PREÇO, na primeira execução desta rodada: a
// primeira versão terminava a alternância com `\z`, que **não existe em regex
// de JavaScript**. Lá, `\z` é identity escape para a LETRA `z` literal — de modo
// que o corpo da entrada terminava no primeiro `z` minúsculo que aparecesse.
// A entrada de GILL et al. sumiu porque seu título contém "optimization", e o
// corpo foi cortado antes da linha do DOI.
//
// O portão apanhou sozinho, pela contagem independente: "o arquivo tem 12
// ligações doi.org e o parser leu 11". Foi o critério A2 pagando o próprio
// custo no primeiro uso — e é exatamente o falso verde que ele existe para
// impedir, porque sem ele o portão teria passado verde ignorando uma entrada.
//
// O fim de entrada é `(?![\s\S])`: nenhuma posição adiante.
const RE_ENTRADA = new RegExp(
  `^(${ALT_SELOS})[ \\t]+([\\s\\S]*?)(?=^(?:${ALT_SELOS})[ \\t]|^#{2,}|^> |^---|(?![\\s\\S]))`,
  "gm"
);

// DOI só conta quando DECLARADO como tal: `DOI [10.x/y](https://doi.org/10.x/y)`.
//
// Uma varredura ingênua por /10\.\d{4,9}\// pegaria também a linha do Springer
// na seção de fronteira, cujo caminho de URL contém um DOI que a entrada NÃO
// declara. Confundir os dois inventaria uma referência que o handbook não fez —
// que é, ironicamente, o defeito que este portão existe para impedir.
// Captura o RÓTULO **e** o ENDEREÇO, e o portão exige que coincidam.
//
// A primeira versão capturava só o rótulo — `DOI\s*\[([^\]]+)\]` — e o alvo do
// link nunca era comparado com nada. Uma entrada podia exibir um DOI verdadeiro
// e levar o leitor a outro: trocar só o `href` passava verde.
//
//   DOI [10.1287/inte.20.4.43](https://doi.org/10.1287/opre.66.6.6666)   → ✓ OK
//
// Numa rodada que existe para impedir identificador inventado, o identificador
// que o leitor de fato USA é o do link. Apontado pela revisão independente.
const RE_DOI = /DOI\s*\[([^\]]+)\]\(\s*https?:\/\/(?:dx\.)?doi\.org\/([^)\s]+)\s*\)/;

// Título: ordem explícita, nunca alternância única.
//
// A alternância /"([^"]+)"|\*\*\*([^*]+)\*\*\*|\*([^*]{12,})\*/ casa o NOME DO
// AUTOR em negrito, não o título: em `**DANTZIG, George B.** "The Diet
// Problem"`, o terceiro ramo encontra casamento no SEGUNDO asterisco do
// negrito, e o motor de regex escolhe pela POSIÇÃO antes de escolher pelo ramo.
// Doze títulos viraram doze nomes de autor na primeira calibração desta rodada.
const EXTRATORES_TITULO = [/"([^"]{8,})"/, /\*\*\*([^*]{8,})\*\*\*/];

// Ano: o ÚLTIMO ano de quatro dígitos que aparece ANTES do marcador "DOI [".
// Depois do marcador vem a prosa da entrada, que costuma citar outras datas.
const RE_ANO = /\b(1[89]\d{2}|20\d{2})\b/g;

// Primeiro autor: o sobrenome inicial do negrito de abertura, em caixa alta.
const RE_PRIMEIRO_AUTOR = /^\*\*([^,*;]+)[,;]/;

export function normaliza(s) {
  return (s || "")
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[*_`]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

// Similaridade de Sørensen–Dice sobre bigramas. Escolhida em vez de distância
// de edição porque as diferenças legítimas entre o título declarado e o
// registrado são de pontuação e caixa, não de reordenação — e a distância de
// edição pune título longo mais do que curto pelo mesmo erro absoluto.
export function similaridade(a, b) {
  const bi = (s) => {
    const g = new Map();
    for (let i = 0; i < s.length - 1; i++) {
      const k = s.slice(i, i + 2);
      g.set(k, (g.get(k) || 0) + 1);
    }
    return g;
  };
  const [x, y] = [bi(a), bi(b)];
  const nx = [...x.values()].reduce((s, v) => s + v, 0);
  const ny = [...y.values()].reduce((s, v) => s + v, 0);
  if (!nx || !ny) return a === b ? 1 : 0;
  let comum = 0;
  for (const [g, n] of x) comum += Math.min(n, y.get(g) || 0);
  return (2 * comum) / (nx + ny);
}

// Limiar MEDIDO nesta bibliografia, não citado de terceiro. O experimento está
// em specs/007-portao-de-fontes/: 12 pares legítimos em 1,000, melhor impostor
// em 0,560, janela de 0,440. O número é o meio da janela.
export const LIMIAR_TITULO = 0.78;
const MIN_CONTENCAO = 15;

// A divergência legítima tem FORMA: o registro corta o subtítulo. Spielman &
// Teng é declarado com o subtítulo inteiro e registrado como "Smoothed analysis
// of algorithms" — 0,517 por bigramas, ABAIXO do melhor impostor (0,560, dois
// títulos diferentes que compartilham "simplex method"). Nenhum limiar único
// separa os dois. Truncamento produz contenção; jargão compartilhado, não.
export function tituloConcorda(declarado, registrado) {
  const [a, b] = [normaliza(declarado), normaliza(registrado)];
  if (!a || !b) return { ok: false, via: "título ausente", s: 0 };
  const [curto, longo] = a.length <= b.length ? [a, b] : [b, a];
  if (curto.length >= MIN_CONTENCAO && longo.startsWith(curto))
    return { ok: true, via: "contenção (subtítulo cortado no registro)", s: 1 };
  const s = similaridade(a, b);
  return { ok: s >= LIMIAR_TITULO, via: `similaridade ${s.toFixed(3)}`, s };
}

// ---------------------------------------------------------------------------
// O parser.
//
// REGRA DE OURO, e ela é o que separa este portão de um portão decorativo:
// entrada que declara DOI e cujo título, ano ou autor não se consegue extrair
// vira DEFEITO, nunca omissão silenciosa. Falha por ignorância é falha. Um
// parser que "não viu nada" e por isso passa verde é o modo clássico de um
// portão mentir sem que ninguém perceba.
export function leBibliografia(caminho) {
  const texto = readFileSync(caminho, "utf8");
  const entradas = [];
  const defeitos = [];
  const selosUsados = new Set();

  for (const m of texto.matchAll(RE_ENTRADA)) {
    const selo = m[1];
    const corpo = m[2];
    selosUsados.add(selo);

    const casa = corpo.match(RE_DOI);
    if (!casa) {
      // Entrada sem DOI é legítima (ADR 0010, D4). Mas entrada que MENCIONA
      // "DOI [" e não casa o formato completo é defeito, não ausência — falhar
      // alto em vez de ignorar em silêncio.
      if (/DOI\s*\[/.test(corpo)) {
        const l = texto.slice(0, m.index).split("\n").length;
        defeitos.push(`bibliografia.md:${l}: entrada com "DOI [" que não casa o formato \`DOI [x](https://doi.org/x)\``);
      }
      continue;
    }
    const doi = casa[1].trim();
    const alvo = decodeURIComponent(casa[2].trim());

    const linha = texto.slice(0, m.index).split("\n").length;
    const onde = `bibliografia.md:${linha}`;

    // O rótulo e o endereço têm de ser o mesmo identificador. DOI é insensível
    // a caixa por especificação, então a comparação também é.
    if (doi.toLowerCase() !== alvo.toLowerCase())
      defeitos.push(`${onde}: o texto do link diz ${doi} e o endereço leva a ${alvo} — o leitor clica no segundo`);

    let titulo = "";
    for (const re of EXTRATORES_TITULO) {
      const t = corpo.match(re);
      if (t) { titulo = t[1].replace(/\s+/g, " ").trim(); break; }
    }

    const antesDoDoi = corpo.slice(0, corpo.indexOf("DOI"));
    const anos = [...antesDoDoi.matchAll(RE_ANO)].map((a) => Number(a[1]));
    const ano = anos.length ? anos[anos.length - 1] : null;

    const autor = corpo.match(RE_PRIMEIRO_AUTOR)?.[1]?.trim() || null;

    if (!titulo) defeitos.push(`${onde}: entrada com DOI ${doi} e título não extraível`);
    if (!ano) defeitos.push(`${onde}: entrada com DOI ${doi} e ano não extraível`);

    entradas.push({ selo, doi, titulo, ano, primeiro_autor: autor, onde });
  }

  return { entradas, defeitos, selosUsados };
}

// A legenda declarada no cabeçalho do arquivo — a tabela `| selo | significa |`.
export function leLegenda(caminho) {
  const texto = readFileSync(caminho, "utf8");
  const declarados = new Set();
  for (const m of texto.matchAll(/^\|\s*(✓ᵐ|✓|⏳|❌|📖)\s*\|/gm)) declarados.add(m[1]);
  return declarados;
}

// ---------------------------------------------------------------------------
// O contrato do travamento. Lista FECHADA — Princípio X vira teste, não promessa.
export const CHAVES_TRAVAMENTO = [
  "doi", "estado", "prefixo", "registrante", "titulo",
  "primeiro_autor", "ano", "container", "fonte", "verificado_em",
];
export const ESTADOS = ["resolvido", "registrado-sem-metadados", "inexistente"];
export const MAX_TEXTO = 300;
