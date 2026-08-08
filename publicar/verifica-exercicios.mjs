// Portão do registro de exercícios (livro/exercicios.json).
//
// Existe porque o registro é editorial — cresce a cada capítulo, escrito à mão —
// e o motor só reclamava de uma coisa: bateria declarada e vazia. O contrário
// (exercício órfão, `capacidade` inexistente, variante sem resposta-guia,
// rubrica vazando para o site publicado) passava calado.
//
// Roda DEPOIS do build, porque a última verificação lê docs/.
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const DOCS = resolve(RAIZ, "docs");

const exercicios = JSON.parse(readFileSync(resolve(RAIZ, "livro/exercicios.json"), "utf8"));
const py = readFileSync(resolve(RAIZ, "chat-companion/backend/capabilities.py"), "utf8");
const CAPACIDADES = new Map(
  [...py.matchAll(/\{"chave":\s*"([^"]+)",\s*"rotulo":\s*"[^"]*",\s*"libera":\s*(\d+)/g)]
    .map(([, chave, libera]) => [chave, Number(libera)])
);

const falhas = [];
const erro = (m) => falhas.push(m);
// Registro vazio só é aceitável enquanto o livro não publicou nenhum capítulo
// numerado além da abertura (capítulo 00). Publicado o primeiro capítulo de
// método, o portão volta a exigir registro — sem que ninguém precise lembrar de
// reativá-lo. A condição é derivada do sumário, não de uma data ou de um
// comentário pedindo boa vontade.
const sumarioPub = JSON.parse(readFileSync(resolve(AQUI, "sumario.json"), "utf8"));
const CAPS_NUMERADOS = sumarioPub.partes.flatMap((p) => p.itens)
  .map((i) => (i.titulo || "").match(/^\s*(\d+)\s*—/))
  .filter(Boolean).map((m) => Number(m[1])).filter((n) => n > 0);
if (!exercicios.length && CAPS_NUMERADOS.length)
  erro(`registro vazio, mas o sumário publica ${CAPS_NUMERADOS.length} capítulo(s) numerado(s) — Princípio I exige prática`);
if (!CAPACIDADES.size) erro("não consegui ler capabilities.py — o portão não está medindo nada");

// 1. Cada exercício, isolado.
const OBRIGATORIOS = ["id", "capitulo", "serie", "variante", "tipo", "capacidade", "titulo", "enunciado", "objetivo"];
const vistos = new Set();
for (const e of exercicios) {
  const id = e.id || "(sem id)";
  for (const campo of OBRIGATORIOS)
    if (e[campo] === undefined || e[campo] === null || e[campo] === "") erro(`${id}: campo obrigatório ausente: ${campo}`);
  if (vistos.has(e.id)) erro(`${id}: id duplicado`);
  vistos.add(e.id);

  // O id não é decorativo: o tutor casa o exercício em foco com o que a PÁGINA
  // declarou, e a bateria é montada por `serie`. Divergência aqui quebra os dois.
  // A–Z, e não A–D. O limite de quatro veio do livro de origem, onde uma bateria
  // era o MESMO exercício em quatro variantes. Aqui uma bateria é um banco de
  // treino: o capítulo de método gráfico pede dez, cinco de resolução e cinco de
  // modelagem. O limite era estado do outro livro, não invariante deste.
  const m = String(e.id || "").match(/^cap(\d{2})\.ex([A-Z])$/);
  if (!m) erro(`${id}: id fora do padrão capNN.exX (X em A–Z)`);
  else {
    if (Number(m[1]) !== e.capitulo) erro(`${id}: capítulo ${e.capitulo} não bate com o id`);
    if (e.serie !== `cap${m[1]}`) erro(`${id}: série "${e.serie}" não bate com o id`);
    if (e.variante !== m[2]) erro(`${id}: variante "${e.variante}" não bate com o id`);
  }

  const n = Array.isArray(e.criterios) ? e.criterios.length : 0;
  if (n < 3 || n > 5) erro(`${id}: ${n} critério(s) de aceite — o contrato é de 3 a 5`);

  // A resposta-guia é o que permite ao tutor julgar equivalência de raciocínio.
  // Quando o CONTEXTO é do leitor — ele traz o próprio problema — não há guia
  // possível, e declarar uma seria mentira. Antes isso era amarrado à letra "D"
  // do identificador, o que confundia POSIÇÃO na bateria com NATUREZA do
  // exercício: bastava um banco com dez itens para a regra virar arbitrária.
  // Agora quem declara é o campo `contexto`.
  const ctx = e.contexto || "livro";
  if (!["livro", "leitor"].includes(ctx)) erro(`${id}: contexto "${ctx}" inválido (livro | leitor)`);
  if (ctx === "livro" && !e.resposta_guia) erro(`${id}: contexto "livro" exige resposta_guia`);
  if (ctx === "leitor" && e.resposta_guia) erro(`${id}: contexto "leitor" não pode ter resposta_guia (o problema é do leitor)`);

  if (!CAPACIDADES.has(e.capacidade)) erro(`${id}: capacidade "${e.capacidade}" não existe em capabilities.py`);
  else if (CAPACIDADES.get(e.capacidade) > e.capitulo)
    erro(`${id}: capacidade "${e.capacidade}" só libera no cap. ${CAPACIDADES.get(e.capacidade)}, mas o exercício é do cap. ${e.capitulo}`);
}

// 2. Nenhum exercício órfão: toda série precisa de um <div data-bateria> que a
//    monte. (O inverso — bateria declarada e vazia — build.mjs já barra.)
const capitulos = resolve(RAIZ, "livro/capitulos");
const arquivosCap = readdirSync(capitulos).filter((f) => f.endsWith(".md"));
const marcadores = new Set(
  arquivosCap.flatMap((f) => [...readFileSync(resolve(capitulos, f), "utf8").matchAll(/data-bateria="([^"]+)"/g)].map((m) => m[1]))
);
for (const serie of new Set(exercicios.map((e) => e.serie)))
  if (!marcadores.has(serie)) erro(`série "${serie}" tem exercício mas nenhum capítulo a monta (data-bateria ausente)`);

// 2b. Todo exercício rastreia a um objetivo QUE EXISTE no capítulo que o monta.
//
//     A constituição (Princípio I) exige o rastreio, e o Guia Editorial diz que
//     "o build falha se apontar para um que não existe". Até aqui isso era prosa:
//     nada media. Um objetivo escrito errado — ou renumerado no capítulo e
//     esquecido no registro — passava calado, e o leitor recebia devolutiva
//     apontando para um objetivo inexistente.
const capituloDaSerie = new Map();
for (const f of arquivosCap) {
  const texto = readFileSync(resolve(capitulos, f), "utf8");
  for (const m of texto.matchAll(/data-bateria="([^"]+)"/g)) capituloDaSerie.set(m[1], { arq: f, texto });
}
for (const e of exercicios) {
  const cap = capituloDaSerie.get(e.serie);
  if (!cap) continue; // já reportado acima
  if (!/^O\d+$/.test(String(e.objetivo || ""))) {
    erro(`${e.id}: objetivo "${e.objetivo}" fora do padrão ON (O1, O2, …)`);
    continue;
  }
  // O capítulo declara os objetivos como "**O1.**" na seção de objetivos.
  if (!new RegExp(`\\*\\*${e.objetivo}\\.\\*\\*`).test(cap.texto))
    erro(`${e.id}: objetivo "${e.objetivo}" não é declarado em ${cap.arq}`);
}

// 3. Princípio I (não-negociável): capítulo numerado sem prática com devolutiva
//    está incompleto. A dívida atual é declarada aqui, em código, e não em prosa:
//    o que está na lista é conhecido; o que não está e aparecer, falha o build.
const SEM_BATERIA_DECLARADO = new Set([
  "00-introducao",       // abertura — a interação prevista é "ponto de conversa", ainda não construída
]);
const paginas = [{ dir: resolve(RAIZ, "livro"), arq: "00-introducao.md" },
                 ...arquivosCap.map((f) => ({ dir: capitulos, arq: f }))];
for (const { dir, arq } of paginas) {
  const slug = arq.replace(/\.md$/, "");
  const temBateria = /data-bateria="/.test(readFileSync(resolve(dir, arq), "utf8"));
  if (!temBateria && !SEM_BATERIA_DECLARADO.has(slug))
    erro(`${slug}: capítulo sem bateria — Princípio I exige prática com devolutiva (ou declare a dívida em SEM_BATERIA_DECLARADO)`);
  if (temBateria && SEM_BATERIA_DECLARADO.has(slug))
    erro(`${slug}: ganhou bateria e continua na lista de dívida — tire-o de SEM_BATERIA_DECLARADO`);
}

// 4. O tutor não avalia por este arquivo: avalia pela cópia que `build_corpus.py`
//    empacota no backend. Se as duas divergirem, o site publica o enunciado X e o
//    tutor corrige pelo enunciado Y — com todos os portões verdes.
{
  const empacotado = resolve(RAIZ, "chat-companion/backend/exercicios.json");
  if (!existsSync(empacotado)) erro("chat-companion/backend/exercicios.json ausente — rode build_corpus.py");
  else if (readFileSync(empacotado, "utf8").trim() !== readFileSync(resolve(RAIZ, "livro/exercicios.json"), "utf8").trim())
    erro("o registro empacotado no backend divergiu de livro/exercicios.json — rode build_corpus.py");
}

// 5. A rubrica não pode ser publicada. O leitor não deve poder ler o critério,
//    o erro esperado ou a resposta antes de responder — nem no HTML, nem no .md
//    baixável, nem no grafo.
//
//    A comparação é feita sobre uma forma normalizada dos dois lados: o registro
//    é texto cru e o site é HTML escapado, então `"de política"` vira
//    `&quot;de política&quot;` na página e um `includes()` ingênuo não casaria —
//    18% dos campos da rubrica têm aspas nos primeiros caracteres, e para todos
//    eles o portão diria "não publicada" com a rubrica publicada.
const desescapar = (s) => s
  .replace(/&(amp|lt|gt|quot|#39|apos|nbsp|#x27);/g, (_, e) =>
    ({ amp: "&", lt: "<", gt: ">", quot: '"', "#39": "'", apos: "'", nbsp: " ", "#x27": "'" }[e]))
  .replace(/&amp;/g, "&");
// Só letras e dígitos: imune a escape, a aspas curvas e a quebra de linha.
const normalizar = (s) => desescapar(String(s)).toLowerCase().normalize("NFD")
  .replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "");
if (existsSync(DOCS)) {
  const arquivos = [];
  const varrer = (dir) => {
    for (const d of readdirSync(dir, { withFileTypes: true })) {
      const p = resolve(dir, d.name);
      if (d.isDirectory()) varrer(p);
      else if (/\.(html|md|json)$/.test(d.name)) arquivos.push(p);
    }
  };
  varrer(DOCS);
  // Tamanho da agulha, calibrado contra o corpus publicado: com 24 caracteres
  // alfanuméricos (≈5 palavras) o portão acusa 5 falsos positivos — o
  // `erro_provavel` de um exercício costuma abrir com a mesma frase que o
  // capítulo publica de propósito em "Erros comuns". Com 40 (≈8 palavras),
  // zero falsos positivos e 302 dos 306 campos cobertos; os 4 mais curtos
  // entram inteiros. O que se procura é a rubrica RENDERIZADA na página, e
  // nesse caso o campo inteiro aparece — agulha curta não acrescenta detecção,
  // só ruído.
  const AGULHA = 40;
  const segredos = exercicios.flatMap((e) =>
    [...(e.criterios || []).map((c) => ["critério", c]), ["erro_provavel", e.erro_provavel], ["resposta_guia", e.resposta_guia]]
      .filter(([, v]) => v)
      .map(([campo, v]) => ({ id: e.id, campo, agulha: normalizar(v).slice(0, AGULHA) }))
      .filter((s) => s.agulha.length >= 20)
  );
  if (segredos.length < exercicios.length * 4) erro(`só ${segredos.length} campos de rubrica sob vigilância — esperado ao menos ${exercicios.length * 4}`);
  for (const arq of arquivos) {
    const conteudo = normalizar(readFileSync(arq, "utf8"));
    for (const s of segredos)
      if (conteudo.includes(s.agulha)) erro(`rubrica vazou em docs/${arq.slice(DOCS.length + 1)}: ${s.id} (${s.campo})`);
  }
} else {
  erro("docs/ não existe — rode o build antes deste portão");
}

if (falhas.length) {
  console.error(`✗ registro de exercícios: ${falhas.length} falha(s)`);
  falhas.forEach((f) => console.error("   " + f));
  process.exit(1);
}
console.log(`✓ registro de exercícios OK: ${exercicios.length} exercícios em ${new Set(exercicios.map((e) => e.serie)).size} baterias, rubrica não publicada`);
