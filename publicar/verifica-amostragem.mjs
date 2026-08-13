// Portão da AMOSTRAGEM — faixa de amostra pequena não é medida de incerteza.
//
// POR QUE ESTE ARQUIVO EXISTE, e a resposta é uma reincidência documentada.
//
// Mínimo e máximo são **estatísticas de ordem**: crescem com o número de
// amostras e não convergem. Publicar "entre X e Y, em N sementes" é publicar
// **o tamanho de N**, não a incerteza — com mais sementes quase sempre aparece
// um valor fora da faixa anterior.
//
// O handbook aprendeu isso na Parte I: a tabela de perturbação foi publicada
// com o máximo de 20 sementes, e o valor mudou de 47 para 63 ao passar para
// 200. A lição virou comentário em `po-zero/parte-I-fundamentos/complexidade.py`
// — *"mínimo/máximo NÃO são publicados"* — e ficou por ali.
//
// Na Parte III ela reincidiu **duas edições depois**. A correção que passou a
// declarar "até onde o dígito carrega" publicou a faixa de **seis** sementes;
// uma revisão independente achou, com dez, um valor abaixo do mínimo publicado;
// com dezesseis a faixa abriu de novo.
//
// A lição não é sobre estatística, é sobre onde as regras moram. **Comentário
// não é portão.** As regras deste repositório que sobreviveram foram as que
// viraram instrumento; as que ficaram em prosa reincidiram. Esta é a terceira
// desta rodada a mudar de categoria.
//
// COMO ELE MEDE. Procura, no corpo dos capítulos, um parágrafo que fale de
// **sementes** ou de **amostras** e publique uma faixa numérica ("de 24,43 a
// 24,51", "entre 81% e 83%"). Achou, exige no mesmo parágrafo uma medida de
// dispersão que estabilize — desvio-padrão, erro-padrão ou intervalo de
// confiança.
//
// O QUE ELE **NÃO** PEGA, declarado em vez de descoberto depois. Ele não sabe
// se a faixa veio de simulação ou de um dado do enunciado — usa a vizinhança de
// "semente"/"amostra" como aproximação, e uma faixa de simulação escrita longe
// dessas palavras passa. Cobre a forma em que o defeito apareceu duas vezes; o
// resto continua sendo leitura humana.
import { readFileSync, existsSync } from "node:fs";
import { dirname, resolve, basename } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const sumario = JSON.parse(readFileSync(resolve(AQUI, "sumario.json"), "utf8"));
const itens = sumario.partes.flatMap((p) => p.itens).filter((i) => i.arquivo);

// O HISTÓRICO fica fora pela mesma razão do portão de desempenho: é append-only
// por regra constitucional, e ele registra as faixas antigas de propósito, como
// parte da narrativa da correção.
const FORA = new Set(["livro/HISTORICO.md"]);

const PARAGRAFO = /\n\s*\n/;
const AMOSTRAGEM = /\bsementes?\b|\bamostras?\b|simula(?:ção|ções|ndo|do)\b/i;
// "de 24,43 a 24,51", "entre 81,8% e 83,1%", "24,43 a 24,51"
const FAIXA = /\b\d+[.,]\d+\s*(?:a|e|até)\s*\d+[.,]\d+|\bentre\s+\d+[.,]?\d*\s*%?\s*e\s+\d+[.,]?\d*\s*%/i;
const DISPERSAO = /desvio[- ]padr[ãa]o|erro[- ]padr[ãa]o|intervalo de confian[çc]a|IC\s*95|±/i;

const falhas = [];
let conferidos = 0, paragrafosVistos = 0;

for (const item of itens) {
  if (FORA.has(item.arquivo)) continue;
  const caminho = resolve(RAIZ, item.arquivo);
  if (!existsSync(caminho)) continue;
  conferidos++;
  const slug = basename(item.arquivo).replace(/\.md$/, "");
  const md = readFileSync(caminho, "utf8").replace(/```[\s\S]*?```/g, "");

  for (const bloco of md.split(PARAGRAFO)) {
    if (!AMOSTRAGEM.test(bloco)) continue;
    const faixa = bloco.match(FAIXA);
    if (!faixa) continue;
    paragrafosVistos++;
    if (DISPERSAO.test(bloco)) continue;
    const trecho = bloco.replace(/\s+/g, " ").trim().slice(0, 110);
    falhas.push(`${slug}: «…${trecho}…» publica faixa («${faixa[0]}») num parágrafo `
      + `de amostragem, sem desvio-padrão nem intervalo de confiança`);
  }
}

if (falhas.length) {
  console.error(`✗ amostragem: ${falhas.length} faixa(s) publicada(s) como se fossem incerteza`);
  falhas.forEach((f) => console.error("   " + f));
  console.error("   → mínimo e máximo crescem com o número de amostras. Publique dispersão.");
  process.exit(1);
}
console.log(`✓ amostragem OK: ${conferidos} capítulos · ${paragrafosVistos} faixa(s) `
  + `em parágrafo de amostragem, todas com medida de dispersão junto`);
