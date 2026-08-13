// Portão de consistência de ótimo.
//
// Existe por causa de um defeito real. O `cap07.exC` afirmava, em rubrica, que
// um certo modelo tinha ótimo em (200, 0) — e não tinha: o ótimo verdadeiro era
// (137,5; 125), com lucro 7,8% maior. A revisão pegou à mão. Nenhum portão pegou,
// porque nenhum portão sabia resolver um modelo.
//
// O padrão por trás do defeito é mais incômodo do que ele: das duas baterias
// publicadas, a única sem verificação executável foi a única com erro de fato.
// O trabalho, então, não era corrigir aquele exercício — era tirar do humano a
// responsabilidade de conferir aritmética.
//
// O que este portão faz: para todo exercício que carregue um campo `modelo`,
// enumera os vértices em **aritmética exata** (racionais sobre BigInt, sem
// ponto flutuante em lugar nenhum) e confere se o ótimo declarado na rubrica é
// mesmo o ótimo do modelo declarado no enunciado.
//
// O que ele NÃO faz: adivinhar o modelo a partir da prosa. Ele confere o que
// foi declarado contra o que foi declarado — se o enunciado disser uma coisa e
// o campo `modelo` disser outra, isso é leitura humana, e está dito na spec.
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const RAIZ = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const exercicios = JSON.parse(readFileSync(resolve(RAIZ, "livro/exercicios.json"), "utf8"));

/* ---------- racionais exatos sobre BigInt ---------- */

const abs = (a) => (a < 0n ? -a : a);
const mdc = (a, b) => { a = abs(a); b = abs(b); while (b) [a, b] = [b, a % b]; return a; };

function rat(n, d = 1n) {
  n = BigInt(n); d = BigInt(d);
  if (d === 0n) throw new Error("denominador zero");
  if (d < 0n) { n = -n; d = -d; }
  const g = mdc(n, d) || 1n;
  return { n: n / g, d: d / g };
}
// Um número do JSON entra como decimal exato: 1.5 vira 3/2, e nunca 1.4999…
function daEntrada(v) {
  const s = String(v).trim();
  const m = s.match(/^(-?)(\d+)(?:\.(\d+))?$/);
  if (!m) throw new Error(`número não reconhecido: ${s}`);
  const [, sinal, inteiro, frac = ""] = m;
  return rat(BigInt(sinal + inteiro + frac), 10n ** BigInt(frac.length));
}
const soma = (a, b) => rat(a.n * b.d + b.n * a.d, a.d * b.d);
const sub = (a, b) => rat(a.n * b.d - b.n * a.d, a.d * b.d);
const mul = (a, b) => rat(a.n * b.n, a.d * b.d);
const div = (a, b) => rat(a.n * b.d, a.d * b.n);
const cmp = (a, b) => { const e = a.n * b.d - b.n * a.d; return e < 0n ? -1 : e > 0n ? 1 : 0; };
const ehZero = (a) => a.n === 0n;
const ZERO = rat(0n);
const texto = (a) => (a.d === 1n ? String(a.n) : `${a.n}/${a.d}`);

/* ---------- o modelo ---------- */

// Toda restrição vira a forma canônica  a·x ≤ b  (uma igualdade vira duas),
// inclusive as de não-negatividade — que entram como restrições de verdade,
// exatamente como na etapa 02 do po-zero. É isso que faz um vértice sobre um
// eixo ser encontrado sem caso especial.
function canonizar(modelo) {
  const rs = [];
  for (const [a1, a2, sinal, b] of modelo.restricoes) {
    const A = [daEntrada(a1), daEntrada(a2)], B = daEntrada(b);
    if (sinal === "<=" || sinal === "=") rs.push({ a: A, b: B });
    if (sinal === ">=" || sinal === "=") rs.push({ a: A.map((v) => sub(ZERO, v)), b: sub(ZERO, B) });
    if (!["<=", ">=", "="].includes(sinal)) throw new Error(`sinal inválido: ${sinal}`);
  }
  rs.push({ a: [rat(-1n), ZERO], b: ZERO });
  rs.push({ a: [ZERO, rat(-1n)], b: ZERO });
  return rs;
}

const viavel = (rs, p) => rs.every((r) => cmp(soma(mul(r.a[0], p[0]), mul(r.a[1], p[1])), r.b) <= 0);
const avaliar = (c, p) => soma(mul(c[0], p[0]), mul(c[1], p[1]));

function vertices(rs) {
  const achados = [];
  for (let i = 0; i < rs.length; i++)
    for (let j = i + 1; j < rs.length; j++) {
      const [r, s] = [rs[i], rs[j]];
      const det = sub(mul(r.a[0], s.a[1]), mul(r.a[1], s.a[0]));
      if (ehZero(det)) continue;                       // paralelas
      const p = [
        div(sub(mul(r.b, s.a[1]), mul(r.a[1], s.b)), det),
        div(sub(mul(r.a[0], s.b), mul(r.b, s.a[0])), det),
      ];
      if (!viavel(rs, p)) continue;
      if (!achados.some((q) => cmp(q[0], p[0]) === 0 && cmp(q[1], p[1]) === 0)) achados.push(p);
    }
  return achados;
}

// Ilimitado na direção de melhora: existe raio d ≥ 0 do cone de recessão
// (A·d ≤ 0) com c·d melhorando o objetivo. Em duas dimensões o cone tem no
// máximo dois raios extremos, e eles saem do mesmo cruzamento de pares — com
// lado direito zero.
function ilimitado(rs, c, maximiza) {
  const homog = rs.map((r) => ({ a: r.a, b: ZERO }));
  const candidatos = [[rat(1n), ZERO], [ZERO, rat(1n)]];
  for (let i = 0; i < homog.length; i++)
    for (let j = i + 1; j < homog.length; j++) {
      const [r, s] = [homog[i], homog[j]];
      const det = sub(mul(r.a[0], s.a[1]), mul(r.a[1], s.a[0]));
      if (ehZero(det)) continue;
      // Direção que anda sobre a reta i: perpendicular ao normal, nos dois sentidos.
      for (const d of [[sub(ZERO, r.a[1]), r.a[0]], [r.a[1], sub(ZERO, r.a[0])],
                       [sub(ZERO, s.a[1]), s.a[0]], [s.a[1], sub(ZERO, s.a[0])]])
        if (!ehZero(d[0]) || !ehZero(d[1])) candidatos.push(d);
    }
  return candidatos.some((d) => {
    if (!homog.every((r) => cmp(soma(mul(r.a[0], d[0]), mul(r.a[1], d[1])), ZERO) <= 0)) return false;
    const g = avaliar(c, d);
    return maximiza ? cmp(g, ZERO) > 0 : cmp(g, ZERO) < 0;
  });
}

/* ---------- a conferência ---------- */

const falhas = [];
const erro = (m) => falhas.push(m);
let conferidos = 0;

function conferir(id, rotulo, modelo) {
  const onde = rotulo ? `${id} [${rotulo}]` : id;
  const maximiza = modelo.sentido === "max";
  if (!["max", "min"].includes(modelo.sentido)) return erro(`${onde}: sentido "${modelo.sentido}" inválido (max | min)`);

  const c = modelo.objetivo.map(daEntrada);
  const rs = canonizar(modelo);
  const vs = vertices(rs);
  const decl = modelo.otimo;

  if (!vs.length) {
    if (decl.status !== "inviavel") erro(`${onde}: o modelo não tem nenhum ponto viável, mas a rubrica declara um ótimo`);
    conferidos++;
    return;
  }
  if (decl.status === "inviavel") return erro(`${onde}: rubrica declara inviável, mas há ${vs.length} vértice(s) viável(is)`);

  const semTeto = ilimitado(rs, c, maximiza);
  if (decl.status === "ilimitado") {
    if (!semTeto) erro(`${onde}: rubrica declara ilimitado, mas o objetivo tem teto na região`);
    conferidos++;
    return;
  }
  if (semTeto) return erro(`${onde}: o objetivo é ilimitado na região, mas a rubrica declara ótimo finito`);

  const melhor = vs.map((p) => avaliar(c, p))
    .reduce((a, b) => (maximiza ? (cmp(b, a) > 0 ? b : a) : (cmp(b, a) < 0 ? b : a)));

  const valorDecl = daEntrada(decl.valor);
  if (cmp(valorDecl, melhor) !== 0)
    erro(`${onde}: rubrica declara ótimo ${texto(valorDecl)}, mas o ótimo do modelo é ${texto(melhor)}`);

  // Ponto declarado: precisa ser viável E atingir o ótimo.
  const pontos = decl.ponto ? [decl.ponto] : decl.segmento || [];
  for (const bruto of pontos) {
    const p = bruto.map(daEntrada);
    if (!viavel(rs, p)) { erro(`${onde}: o ponto declarado (${p.map(texto)}) viola alguma restrição do próprio modelo`); continue; }
    const v = avaliar(c, p);
    if (cmp(v, valorDecl) !== 0)
      erro(`${onde}: no ponto (${p.map(texto)}) o objetivo vale ${texto(v)}, e a rubrica declara ${texto(valorDecl)}`);
  }

  // Múltiplos ótimos: quem declara segmento precisa de dois vértices empatados,
  // e quem declara ponto único não pode ter empate escondido.
  const empatados = vs.filter((p) => cmp(avaliar(c, p), melhor) === 0);
  if (decl.segmento && empatados.length < 2)
    erro(`${onde}: rubrica declara segmento de ótimos, mas só ${empatados.length} vértice atinge o ótimo`);
  if (decl.ponto && empatados.length > 1 && !decl.multiplos_ok)
    erro(`${onde}: ${empatados.length} vértices atingem o ótimo (${empatados.map((p) => "(" + p.map(texto) + ")").join(", ")}), mas a rubrica declara um ponto único`);

  conferidos++;
}

for (const e of exercicios) {
  if (!e.modelo) continue;
  const lista = Array.isArray(e.modelo) ? e.modelo : [e.modelo];
  for (const m of lista) {
    try { conferir(e.id, m.rotulo, m); }
    catch (err) { erro(`${e.id}: modelo malformado — ${err.message}`); }
  }
}

// A cobertura é o outro metade do portão. Sem isto, bastaria omitir o campo
// `modelo` para o exercício voltar a passar sem ninguém conferir nada — que é
// exatamente o estado em que o defeito do cap07.exC nasceu.
// A régua era `/[óo]tim/i`, e num livro sobre OTIMIZAÇÃO isso é um falso
// vermelho esperando a hora: "código otimizado", "o solver otimiza", "problema
// de otimização" — nenhum deles afirma um ótimo, e todos disparavam o portão.
// O primeiro caso apareceu no `cap77.exB`, cuja rubrica fala de código otimizado
// num exercício que não tem modelo nenhum, por não ser de modelagem.
//
// Falso vermelho crônico é o que ensina a desligar portão, então a régua foi
// estreitada para o SUBSTANTIVO — ótimo, ótima, ótimos, ótimas — que é o que de
// fato afirma um valor. Medido antes de trocar, sobre o registro inteiro:
// exatamente um exercício sai da vigilância (o falso positivo) e nenhum outro é
// solto. "otimizado" não casa porque depois de `otim` vem `i`, e não `o`/`a`.
const AFIRMA_OTIMO = /[óo]tim[oa]s?\b/i;
const SEM_MODELO_DECLARADO = new Set([
  // Exercícios cuja rubrica fala de "ótimo" sem afirmar um valor calculável a
  // partir de um modelo de duas variáveis. Cada entrada precisa de justificativa.
  //
  // O capítulo 38 é o primeiro caso legítimo, e é instrutivo: ele trata de
  // CONVEXIDADE, e o motor deste portão só sabe resolver o que é convexo por
  // construção — enumera vértices de uma interseção de semiespaços. Um exercício
  // sobre região NÃO convexa é, por definição, o que ele não consegue conferir.
  "cap38.exA", // decide convexidade de conjuntos; a única menção a "ótimo" é ao
               // teorema (ótimo local é global). Não afirma valor nenhum.
  "cap38.exB", // a região é uma UNIÃO ("fornecedor A ou B"), que não se escreve
               // como conjunção de desigualdades — o enumerador de vértices não
               // a representa. Os números 22 e 30 são conferidos onde podem ser:
               // po-zero/etapa-06-convexidade, com teste que lê esta rubrica.
  "cap38.exC", // cenário de consultoria sem modelo numérico; "ótimo" aparece só
               // na discussão do que a palavra `Optimal` significa num relatório.
  "cap01.exA", // classifica quatro PEDIDOS em prosa como sendo ou não de PO. Não
               // há modelo nenhum — nem podia haver, porque o exercício é sobre
               // reconhecer que dois deles NÃO são problemas de otimização. A
               // única menção a "ótima" é a expressão "a escala ótima", usada
               // para descrever um risco de leitura.
  "cap11.exE", // relatório hipotético de dois solvers num modelo de mistura que o
               // exercício NÃO especifica — de propósito, porque o assunto é a
               // inferência "mesmo valor, logo mesma solução", e não o modelo. Os
               // números que ele cita (erro relativo, base igual) são conferidos
               // em po-zero/etapa-05-parte2/test_revisado.py.
  "cap03.exC", // modelo de TRÊS variáveis (caminhões, quilômetros, terceirizações),
               // fora do alcance deste enumerador, que é de duas. A rubrica afirma
               // um comportamento — que o Simplex cola `k` em 120.000 —, e a
               // afirmação NÃO fica solta: está medida em aritmética exata em
               // po-zero/etapa-01-formulacao/test_anatomia.py, que resolve o
               // modelo pelo Simplex da etapa 03 e ainda confere que a rubrica
               // continua dizendo o que foi medido.
  "cap04.exB", // não há modelo: são quatro TRAVESSIAS de eixo descritas em prosa
               // ("o modelo ganhou uma restrição de integralidade"), e a rubrica
               // fala de "ótimo" para dizer qual GARANTIA cada travessia destrói.
               // Não afirma valor nenhum, e não poderia — nenhum dos quatro casos
               // traz números.
  "cap04.exC", // três relatórios hipotéticos (PL em 3s, inteiro com gap de 1,8%,
               // heurística de roteirização). A rubrica discute o que a palavra
               // "ótimo" autoriza prometer em cada um; os únicos números são o
               // gap e os tempos, que são DADOS do enunciado, não resultados de
               // um modelo que este portão pudesse resolver.
  "cap05.exB", // decisão de projeto sobre uma instância de 400 binárias que o
               // exercício NÃO especifica — de propósito, porque o assunto é a
               // ORDEM de trabalho (rodar o exato, ler o gap, só então decidir),
               // e não a solução. A palavra "ótimo" aparece na frase que o
               // relatório NÃO pode dizer. Nada a conferir.
  "cap16.exC", // julga se a LENTE de rede serve em quatro pedidos escritos em
               // prosa. Não há modelo numérico em nenhum deles; "ótimo" aparece
               // só na discussão do que o solver devolve quando a estrutura de
               // rede se perde.
  "cap17.exA", // caminho mínimo numa malha de SEIS nós — grafo, não modelo de
               // duas variáveis. Os números (11, e a ordem de fechamento) são
               // conferidos em po-zero/parte-III-redes/test_redes.py, que resolve
               // a mesma malha em aritmética exata.
  "cap17.exB", // a instância em que Dijkstra erra, também um grafo. Os dois
               // números que a rubrica afirma — 6 e 4 — são medidos na mesma
               // suíte, e o capítulo 17 os publica com teste que o lê.
  "cap18.exB", // compara guloso e ótimo num grafo de CINCO cidades — dez arestas,
               // não duas variáveis. Os quatro números (17, 32, 28, 14,3%) são
               // medidos em po-zero/parte-III-redes, e o 17 é conferido por um
               // segundo caminho: enumeração de todas as árvores geradoras.
  "cap18.exC", // classifica quatro decisões de projeto de rede escritas em prosa.
               // Não há modelo numérico; "ótimo" aparece na discussão de qual
               // problema tem guloso ótimo e qual não tem.
  "cap19.exA", // rede de fluxo com sete nós. O fluxo máximo (15) e a capacidade
               // do corte (15) são medidos na mesma suíte, e o capítulo 19 os
               // publica com teste que o lê.
]);
for (const e of exercicios) {
  const rubrica = [e.resposta_guia || "", ...(e.criterios || [])].join(" ");
  if (!AFIRMA_OTIMO.test(rubrica)) continue;
  if (e.modelo || SEM_MODELO_DECLARADO.has(e.id)) continue;
  erro(`${e.id}: a rubrica afirma um ótimo e não há campo "modelo" para conferi-lo — declare o modelo ou justifique em SEM_MODELO_DECLARADO`);
}

if (falhas.length) {
  console.error(`✗ consistência de ótimo: ${falhas.length} falha(s)`);
  falhas.forEach((f) => console.error("   " + f));
  process.exit(1);
}
console.log(`✓ consistência de ótimo OK: ${conferidos} modelo(s) resolvido(s) em aritmética exata`);
