// Portão da PROCEDÊNCIA — o corpo não pode afirmar o que a tabela nega.
//
// POR QUE ESTE ARQUIVO EXISTE. O defeito apareceu três vezes, em três rodadas,
// sempre igual: a tabela "Procedência" do capítulo marca uma afirmação como `⏳`
// (atribuição corrente, não confirmada) ou `❌` (procurada e não encontrada), e o
// corpo do mesmo capítulo a enuncia como fato.
//
//   · capítulo 12 — "o minimax, publicado por von Neumann em 1928"
//   · capítulo 14 — "o método do elipsoide perdia feio para o Simplex"
//   · capítulo 09 — "a sugestão veio de T. S. Motzkin, numa conversa"
//
// Os três foram pegos por leitura humana, e os três só depois de publicados.
// Nenhum dos onze portões via, porque nenhum deles lia a RELAÇÃO entre duas
// partes do mesmo arquivo. A constituição é explícita — fonte `⏳` **não
// sustenta afirmação** — e uma regra que só existe em prosa envelhece.
//
// COMO ELE MEDE, e a escolha é deliberadamente conservadora.
//
// Para cada linha `⏳`/`❌` da tabela de Procedência, extraem-se os termos que
// carregam a afirmação: **nomes próprios** e **anos**. Se um desses termos
// aparece no corpo, exige-se que ao menos uma ocorrência esteja PERTO de uma
// marca de ressalva — um `⏳` no texto. É a forma que as três correções tomaram:
// uma caixa de ressalva ao lado da afirmação.
//
// O portão é leniente de propósito: **uma** ressalva perto basta. Ele não julga
// se a prosa está bem hedgeada — julga se a ressalva EXISTE. Portão que tenta
// julgar nuance de linguagem produz falso vermelho crônico, e falso vermelho
// crônico é o que ensina a desligar portão.
//
// ---------------------------------------------------------------------------
// O QUE ESTE PORTÃO **NÃO** PEGA, medido e declarado em vez de descoberto depois.
//
// Ele pega a forma **grosseira**: um termo cuja afirmação está `⏳` e que aparece
// no corpo sem ressalva nenhuma por perto. Foi o estado dos capítulos 08 e 14.
//
// Ele **não** pega o termo hedgeado num lugar e afirmado em outro — que é
// exatamente o caso original do capítulo 12, onde "von Neumann" aparecia numa
// caixa de ressalva e, alguns parágrafos adiante, como fato. Testado: removendo
// a ressalva do 12, este portão continua verde, porque a outra ressalva da mesma
// seção cai dentro da janela.
//
// A régua ESTRITA — exigir ressalva perto de TODA ocorrência — foi medida contra
// o corpus corrigido e acusou 4 casos, entre eles "Karmarkar" num capítulo que
// trata de Karmarkar do início ao fim. Ela troca um buraco por um falso vermelho
// crônico, e falso vermelho crônico desliga portão.
//
// **Conclusão honesta: proximidade não decide se uma frase afirma.** O portão
// cobre o caso grosseiro e o resto continua sendo leitura humana — com a
// diferença de que o padrão agora tem nome, aparece na instrução de toda revisão
// em contexto fresco, e reincidiu quatro vezes documentadas.
import { readFileSync, existsSync } from "node:fs";
import { dirname, resolve, basename } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const sumario = JSON.parse(readFileSync(resolve(AQUI, "sumario.json"), "utf8"));
const itens = sumario.partes.flatMap((p) => p.itens).filter((i) => i.arquivo);

// Janela em caracteres. Calibrada: uma caixa de ressalva tem 3 a 6 linhas de ~95
// colunas, e a afirmação que ela cobre costuma vir no parágrafo imediatamente
// antes ou depois. 900 cobre esse arranjo com folga e não atravessa uma seção
// inteira.
const JANELA = 900;

// Termos que carregam afirmação: nome próprio (inclusive com iniciais, como
// "T. C. Koopmans") e ano de quatro dígitos. Palavras de início de frase e
// termos de estrutura ficam de fora — senão o portão persegue ruído.
const PARADAS = new Set([
  "Programação", "Linear", "Pesquisa", "Operacional", "Este", "Esse", "Aquele",
  "Simplex", "Handbook", "Parte", "Capítulo", "Procurada", "Procurado", "Atribuição", "Data",
  "Metadados", "Repercussão", "Identificador", "Conteúdo", "Registrada", "Registrado", "Tese",
]);

const falhas = [];
let conferidos = 0, linhasVigiadas = 0, termosVigiados = 0, mistas = 0;

for (const item of itens) {
  const slug = basename(item.arquivo).replace(/\.md$/, "");
  const caminho = resolve(RAIZ, item.arquivo);
  if (!existsSync(caminho)) continue;
  const md = readFileSync(caminho, "utf8");

  // A tabela de Procedência: linhas `| afirmação | estado |` cujo estado tem ⏳ ou ❌.
  const linhas = [...md.matchAll(/^\|\s*([^|\n]+?)\s*\|\s*([^|\n]*[⏳❌][^|\n]*)\s*\|\s*$/gm)];
  if (!linhas.length) continue;
  conferidos++;

  // O corpo é tudo fora das tabelas — é lá que a afirmação vira prosa.
  const corpo = md.split("\n").filter((l) => !l.trimStart().startsWith("|")).join("\n");
  // Posições de toda ressalva no corpo — o glifo `⏳` **e** a ressalva em prosa.
  //
  // CALIBRADO CONTRA O CORPUS, e a calibração mudou a regra. A primeira versão
  // exigia o glifo, e acusou o capítulo 10 por dizer *"costuma ser atribuída a
  // Beale (1955)"* — que é exatamente o hedge que a constituição pede, escrito
  // em português em vez de em símbolo. Exigir o glifo seria exigir uma convenção
  // de formatação, não honestidade; e um portão que persegue formatação treina
  // quem escreve a satisfazê-lo em vez de a pensar.
  //
  // O que o portão passou a procurar é a MARCA DE ATRIBUIÇÃO — a construção pela
  // qual o texto diz "isto é o que se conta, não o que eu verifiquei".
  const ressalvas = [...corpo.matchAll(
    /⏳|atribu[íiy]|corrente|costuma|relat[ao]|não (?:afirma|confirm|localiz|mediu|foi confirmad)|se conta|a literatura|literatura (?:didática|atribui|relata|descreve)|não é afirmad|sem identificador|pode ser verdadeir/gi
  )].map((m) => m.index);

  for (const [afirmacao, estado] of linhas.map((m) => [m[1], m[2]])) {
    // LINHA DE ESTADO MISTO fica fora do alcance deste portão, e a limitação é
    // declarada em vez de descoberta depois. O capítulo 10 traz
    // `✓ᵐ metadados; ⏳ enunciado exato e prova de terminação`: a data e a
    // autoria ESTÃO conferidas, e só o conteúdo não. O portão não sabe dizer a
    // que metade da célula cada termo da afirmação pertence — e chutar produziria
    // o falso vermelho que ele existe para não produzir.
    //
    // Consequência aceita: célula mista depende de leitura humana. Consequência
    // recusada: acusar um capítulo por afirmar o que ele de fato conferiu.
    if (/✓/.test(estado)) { mistas++; continue; }
    linhasVigiadas++;
    const termos = new Set();
    for (const m of afirmacao.matchAll(/\b(1[89]\d{2}|20\d{2})\b/g)) termos.add(m[1]);
    for (const m of afirmacao.matchAll(/\b([A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]{3,})\b/g))
      if (!PARADAS.has(m[1])) termos.add(m[1]);

    for (const termo of termos) {
      const ocorrencias = [...corpo.matchAll(new RegExp(`\\b${termo}\\b`, "g"))].map((m) => m.index);
      if (!ocorrencias.length) continue;          // não afirmado no corpo: conforme
      termosVigiados++;
      const perto = ocorrencias.some((o) => ressalvas.some((r) => Math.abs(r - o) <= JANELA));
      if (!perto)
        falhas.push(`${slug}: "${termo}" aparece no corpo sem nenhuma ressalva ⏳ por perto, `
          + `e a Procedência marca «${afirmacao.slice(0, 70)}…» como não confirmada`);
    }
  }
}

if (falhas.length) {
  console.error(`✗ procedência: ${falhas.length} afirmação(ões) sem ressalva perto`);
  falhas.forEach((f) => console.error("   " + f));
  process.exit(1);
}
console.log(`✓ procedência OK: ${conferidos} capítulos, ${linhasVigiadas} linha(s) ⏳/❌, `
  + `${termosVigiados} termo(s) do corpo com ressalva por perto · ${mistas} linha(s) de estado misto fora do alcance`);
