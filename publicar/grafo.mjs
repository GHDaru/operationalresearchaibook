// Knowledge Graph do handbook — extração DETERMINÍSTICA, sem modelo de linguagem.
// Nós: capítulos, conceitos-chave de Pesquisa Operacional (PO) e etapas do po-zero.
// Arestas: menções reais no texto (peso = nº de ocorrências) — evidência verificável.
// Chamado pelo build.mjs a cada build ⇒ o grafo acompanha toda mudança do livro.
//
// Nós sem nenhuma aresta são PODADOS. Isso é desenho, não defeito: um grafo que
// mostra nó solto sugere relação que o texto não tem. Enquanto o handbook não
// publicar capítulos de método, o grafo é legitimamente vazio.

import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

// Conceitos-chave com página de referência no glossário. A régua para entrar
// aqui: o conceito precisa ATRAVESSAR capítulos — é isso que faz aresta. Termo
// que só existe dentro de um capítulo não é nó de grafo, é conteúdo dele.
const CONCEITOS = [
  { id: "programacao-linear", rotulo: "Programação Linear", re: /\b(?:programação\s+linear|\bPL\b)/gi },
  { id: "simplex", rotulo: "Simplex", re: /\bSimplex\b/gi },
  { id: "dualidade", rotulo: "Dualidade", re: /\b(?:dualidade|dual|problema\s+dual)\b/gi },
  { id: "preco-sombra", rotulo: "Preço-sombra", re: /\bpreços?[-\s]sombra\b/gi },
  { id: "sensibilidade", rotulo: "Análise de sensibilidade", re: /\banálise\s+de\s+sensibilidade\b/gi },
  { id: "programacao-inteira", rotulo: "Programação Inteira", re: /\b(?:programação\s+inteira|MILP|MINLP)\b/gi },
  { id: "branch-and-bound", rotulo: "Branch and Bound", re: /\bbranch[-\s]and[-\s]bound\b/gi },
  { id: "relaxacao", rotulo: "Relaxação", re: /\brelaxaç(?:ão|ões)\b/gi },
  { id: "limitante", rotulo: "Limitante", re: /\blimitantes?\b/gi },
  { id: "rede", rotulo: "Redes e fluxos", re: /\b(?:fluxo\s+(?:máximo|de\s+custo\s+mínimo)|caminho\s+mínimo|corte\s+mínimo)\b/gi },
  { id: "heuristica", rotulo: "Heurística", re: /\bheurísticas?\b/gi },
  { id: "metaheuristica", rotulo: "Metaheurística", re: /\bmeta[-\s]?heurísticas?\b/gi },
  { id: "busca-local", rotulo: "Busca local", re: /\b(?:busca\s+local|vizinhança)\b/gi },
  { id: "convexidade", rotulo: "Convexidade", re: /\bconvexid(?:ade|as?)|convexos?\b/gi },
  { id: "incerteza", rotulo: "Otimização sob incerteza", re: /\b(?:programação\s+estocástica|otimização\s+robusta|cenários?)\b/gi },
  { id: "markov", rotulo: "Cadeias de Markov", re: /\bMarkov\b/gi },
  { id: "filas", rotulo: "Teoria de filas", re: /\bteoria\s+de\s+filas\b/gi },
  { id: "programacao-dinamica", rotulo: "Programação Dinâmica", re: /\bprogramação\s+dinâmica\b/gi },
  { id: "solver", rotulo: "Solver", re: /\bsolvers?\b/gi },
  { id: "modelagem", rotulo: "Modelagem", re: /\b(?:variáveis?\s+de\s+decisão|função\s+objetivo|região\s+viável)\b/gi },
];

// Etapas do po-zero. O texto as cita como "etapa N" na seção de código.
const MAX_ETAPA = 20;
const GH = "https://github.com/GHDaru/operationalresearchaibook/tree/main/po-zero";

function contar(re, texto) {
  const m = texto.match(re);
  return m ? m.length : 0;
}

export function gerarGrafo(itens, RAIZ, versao) {
  const capitulos = itens.filter((i) => /^\s*\d+\s*—/.test(i.titulo));
  const nos = [];
  const arestas = [];
  const addAresta = (de, para, peso) => { if (peso > 0 && de !== para) arestas.push({ de, para, peso }); };

  for (const c of capitulos) {
    const num = c.titulo.match(/^\s*(\d+)/)[1];
    nos.push({ id: "cap-" + num, tipo: "capitulo", rotulo: c.titulo, url: c.slug + ".html" });
  }
  for (const co of CONCEITOS) nos.push({ id: co.id, tipo: "conceito", rotulo: co.rotulo, url: "glossario.html" });
  for (let i = 0; i <= MAX_ETAPA; i++) {
    const n = String(i).padStart(2, "0");
    nos.push({ id: "etapa-" + n, tipo: "etapa", rotulo: "etapa " + n + " · po-zero", url: GH });
  }

  for (const c of capitulos) {
    const caminho = resolve(RAIZ, c.arquivo);
    if (!existsSync(caminho)) continue;
    const num = c.titulo.match(/^\s*(\d+)/)[1];
    const id = "cap-" + num;
    // corpo sem blocos de código (código cita nomes por razões mecânicas, não conceituais)
    const texto = readFileSync(caminho, "utf8").replace(/```[\s\S]*?```/g, " ");

    // capítulo → capítulo ("cap. NN" / "capítulo NN")
    const porCap = {};
    for (const m of texto.matchAll(/\bcap(?:ítulos?|s?\.)\s*(\d{1,2})\b/gi)) {
      const alvo = String(parseInt(m[1], 10)).padStart(2, "0");
      if (alvo !== num && capitulos.some((x) => x.titulo.trim().startsWith(alvo))) porCap[alvo] = (porCap[alvo] || 0) + 1;
    }
    for (const alvo of Object.keys(porCap)) addAresta(id, "cap-" + alvo, porCap[alvo]);

    for (const co of CONCEITOS) addAresta(id, co.id, contar(co.re, texto));

    // capítulo → etapa do po-zero ("etapa N", tipicamente na seção de código)
    const porEtapa = {};
    for (const m of texto.matchAll(/\betapas?\s+(\d{1,2})\b/gi)) {
      const n = String(parseInt(m[1], 10)).padStart(2, "0");
      if (parseInt(n, 10) <= MAX_ETAPA) porEtapa[n] = (porEtapa[n] || 0) + 1;
    }
    for (const n of Object.keys(porEtapa)) addAresta(id, "etapa-" + n, porEtapa[n]);
  }

  // poda: nós sem nenhuma aresta saem (mantém o grafo honesto)
  const conectados = new Set();
  arestas.forEach((a) => { conectados.add(a.de); conectados.add(a.para); });
  const nosFinais = nos.filter((n) => conectados.has(n.id));

  return { versao, nos: nosFinais, arestas };
}
