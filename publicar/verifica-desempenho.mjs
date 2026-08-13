// Portão do DESEMPENHO — nenhuma comparação de velocidade sem cronômetro.
//
// POR QUE ESTE ARQUIVO EXISTE. O guia editorial é literal: *"Nenhum número sem
// procedência. Nem 'cerca de 10× mais rápido'"*. A regra vivia só em prosa, e
// numa única rodada o defeito apareceu **três** vezes:
//
//   · capítulo 16 — "métodos que resolvem em segundos o que o modelo genérico
//     resolve em minutos", na mesma página que declarava "nenhum número novo —
//     este capítulo é de vocabulário";
//   · capítulo 21 e o gabarito de `cap21.exB` — "em instâncias grandes a
//     diferença é de minutos para horas", sem nenhuma medição de tempo no
//     `po-zero`;
//   · capítulo 17 — "sai em milissegundos", escrito **na mesma rodada em que os
//     dois primeiros foram corrigidos**, por quem os corrigiu.
//
// O terceiro é o que justifica o portão. Os dois primeiros dá para atribuir a
// desatenção; o terceiro mostra que a frase de velocidade é uma tentação de
// escrita, não um lapso — ela deixa o texto mais convincente exatamente onde ele
// tem menos direito de convencer. Disciplina não segura isso. Instrumento segura.
//
// COMO ELE MEDE. Procura no corpo dos capítulos e nos exercícios as construções
// que comparam TEMPO — "em segundos", "de minutos para horas", "10× mais
// rápido", "milissegundos". Achou uma, exige que perto dela haja **ou** uma
// declaração de que a medição existe (ponteiro para o `po-zero`, para a suíte de
// testes, ou a palavra "medido"), **ou** uma renúncia explícita — "não
// cronometrou", "não publica número".
//
// O QUE ELE **NÃO** PEGA, declarado em vez de descoberto depois.
//
// Ele lê proximidade, não sentido. Um capítulo que diga "medido" a respeito de
// outra coisa, dentro da janela, passa — é o mesmo limite do portão de
// procedência, e pela mesma razão: portão que tenta julgar nuance de linguagem
// produz falso vermelho crônico, e falso vermelho crônico é o que ensina a
// desligar portão.
//
// Ele também não pega a comparação de velocidade escrita sem palavra de tempo
// ("o método especializado é muito superior"). Essa continua sendo leitura
// humana — com a diferença de que o padrão agora tem nome e reincidiu três vezes
// documentadas.
import { readFileSync, existsSync } from "node:fs";
import { dirname, resolve, basename } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const sumario = JSON.parse(readFileSync(resolve(AQUI, "sumario.json"), "utf8"));
const itens = sumario.partes.flatMap((p) => p.itens).filter((i) => i.arquivo);

// O ESCOPO É O PARÁGRAFO, e não uma janela de caracteres — segunda lição desta
// rodada, também aprendida por teste que falhou.
//
// Com a janela de 900 caracteres do portão de procedência, dois dos três
// defeitos reintroduzidos passaram: no capítulo 21, um "Medido nesta página:
// custo 9" a setecentos caracteres de distância autorizava "de minutos para
// horas". Medição de OUTRA coisa, por perto, não é procedência desta.
//
// A regra que sobrou é a que um leitor aplicaria: **a medição tem de estar no
// mesmo parágrafo da afirmação**. Quem publica um tempo cita ali mesmo de onde
// ele saiu. É mais estrito que o portão de procedência, e pode ser, porque
// afirmação de tempo é rara — três em todo o corpus.
const PARAGRAFO = /\n\s*\n/;

// As construções que afirmam DESEMPENHO — e a calibração contra o corpus
// estreitou as três, porque a primeira versão perseguia toda palavra de tempo e
// acusava "em dia de pico", "converter para horas" e "o número de horas que um
// pesquisador tem". Nenhuma delas é afirmação de velocidade de método.
//
// O que sobrou são as formas em que o tempo é PREDICADO DE UM MÉTODO:
//   1. verbo (ou substantivo) de resolução seguido de unidade de tempo —
//      "resolve em segundos", "roda em milissegundos", "resposta em segundos";
//   2. a escalada de duas unidades — "de minutos para horas";
//   3. a razão explícita — "10× mais rápido", "ordens de grandeza mais lento".
const RESOLVER = "(?:resolv\\w*|rod\\w*|sai|saem|responde\\w*|resposta|retorna\\w*|"
  + "termin\\w*|converg\\w*|lev\\w*|dur\\w*|calcul\\w*|solu[çc][ãa]o)";
const UNIDADE = "(?:milissegundos?|segundos?|minutos?|horas?)";
//
// E há um discriminador que a calibração revelou, limpo o bastante para virar
// regra: **unidade nua é retórica; unidade quantificada é dado.** "Roda em
// milissegundos" afirma uma propriedade geral do método e não tem como ser
// conferido. "Roda em 40 minutos" descreve *aquela* instância de *aquela*
// história — é dado de enunciado, e o leitor sabe exatamente do que se fala.
// Os três defeitos documentados usam a forma nua; os seis falsos vermelhos da
// primeira calibração usavam a forma quantificada, todos eles.
const AFIRMACOES = [
  new RegExp(`\\b${RESOLVER}(?:\\s+\\w+){0,3}\\s+em\\s+(?:poucos?\\s+|alguns?\\s+)?${UNIDADE}\\b`, "gi"),
  new RegExp(`\\bde\\s+${UNIDADE}\\s+(?:para|a)\\s+${UNIDADE}\\b`, "gi"),
  /\b\d+\s*(?:×|x|vezes)\s+mais\s+(?:r[áa]pid|lent)/gi,
  /\bordens?\s+de\s+grandeza\s+mais\s+(?:r[áa]pid|lent)/gi,
];

// Fala de outro não é afirmação do livro. O handbook marca citação com
// `*"…"*` — o resumo de artigo do capítulo 77, a frase do gerente no 02, o
// relato do consultor no 01. Julgar a frase de um personagem pelo padrão de
// evidência do livro seria proibir o livro de citar o que ele critica: é
// exatamente o que o capítulo 77 faz com "40× mais rápido", e ele existe para
// ensinar o leitor a desconfiar dessa frase.
const CITACAO = /"[^"]{0,300}"|“[^”]{0,300}”/g;

// A MEDIÇÃO TEM DE ESTAR NA MESMA FRASE — terceiro aperto, e o último.
//
// Com escopo de parágrafo, o defeito do capítulo 16 ainda passava: a Leitura
// executiva é um parágrafo longo, e um "o que esta Parte de fato mede", escrito
// sobre outra coisa, autorizava "resolvem em segundos" trinta linhas adiante.
//
// Frase é o escopo certo porque é o escopo da própria regra: quem publica um
// tempo diz, ali, de onde ele saiu. A RENÚNCIA continua sendo procurada no
// parágrafo — ela não autoriza nada, só muda a mensagem de erro para a mais
// útil ("você declarou que não cronometrou e publicou assim mesmo").
function frase(texto, i) {
  const antes = texto.lastIndexOf(". ", i);
  const depois = texto.indexOf(". ", i);
  return texto.slice(antes < 0 ? 0 : antes, depois < 0 ? texto.length : depois);
}

// SÓ MEDIÇÃO AUTORIZA — e esta separação é a lição mais dura desta rodada.
//
// A primeira versão do portão aceitava, como autorização, tanto a medição
// quanto a **renúncia** ("este handbook não cronometrou"). Testado contra os
// três defeitos documentados, reintroduzidos um a um: o portão ficou **verde
// nos três**. A razão é constrangedora e vale registrar: os três defeitos
// moravam ao lado das renúncias que os corrigiram, e o portão lia a renúncia
// como licença para a frase que ela existia para substituir.
//
// A semântica certa é outra. Renúncia é o que se escreve **no lugar** da
// afirmação, não ao lado dela. "Este handbook não cronometrou" **junto de** "a
// diferença é de minutos para horas" não é uma frase autorizada — é uma
// contradição, e era exatamente o estado do capítulo 21.
//
// Portanto: só ponteiro para medição autoriza. Renúncia perto de afirmação
// positiva vira falha própria, com mensagem própria.
// A MARCA DE MEDIÇÃO PRECISA DIZER **ONDE** — quarto e último aperto.
//
// Com a palavra solta "medido" valendo como autorização, o defeito do capítulo
// 16 ainda passava, e por um motivo que nenhuma regexp resolve: a frase dizia
// "garantias que o modelo genérico não oferece — a principal delas **medida** no
// capítulo 20". A palavra está lá, e é sobre a *garantia*, não sobre o tempo.
//
// Em vez de tentar adivinhar o referente, o portão passou a exigir o que a
// constituição já exige: **procedência é lugar**. "Medido em `po-zero/...`",
// "cronometrado na suíte" — um ponteiro que o leitor possa abrir. Um "medida"
// solto não é procedência de coisa nenhuma, e é justo cobrá-lo.
const MEDICAO =
  /po-zero|`pytest`|suíte de testes|cronometrad[oa]|medi[çd][oa]s?\s+(?:em|n[oa])\s+`/gi;
const RENUNCIA =
  /não (?:cronometr\w*|public\w* número|é medid|foi medid|temporiz\w*|mediu)|sem cronômetro/gi;

// A renúncia contém "cronometr", que também é marca de medição. Ela é casada
// PRIMEIRO e o trecho é retirado do texto antes de procurar medição — senão a
// negação seria lida como afirmação.
function marcas(texto) {
  const renuncias = [...texto.matchAll(RENUNCIA)].map((m) => [m.index, m.index + m[0].length]);
  let limpo = texto;
  for (const [a, b] of renuncias) limpo = limpo.slice(0, a) + " ".repeat(b - a) + limpo.slice(b);
  return { renuncias: renuncias.map(([a]) => a),
           medicoes: [...limpo.matchAll(MEDICAO)].map((m) => m.index) };
}

const falhas = [];
let conferidos = 0, afirmacoesVistas = 0;

function analisa(nome, texto) {
  for (const bloco of texto.split(PARAGRAFO)) {
    const { renuncias } = marcas(bloco);
    const citacoes = [...bloco.matchAll(CITACAO)].map((m) => [m.index, m.index + m[0].length]);
    for (const padrao of AFIRMACOES) {
      for (const m of bloco.matchAll(padrao)) {
        const i = m.index;
        if (citacoes.some(([a, b]) => i >= a && i < b)) continue;
        afirmacoesVistas++;
        if (marcas(frase(bloco, i)).medicoes.length) continue;
        const trecho = bloco.slice(Math.max(0, i - 45), i + 55).replace(/\s+/g, " ").trim();
        falhas.push(renuncias.length
          ? `${nome}: «…${trecho}…» afirma tempo NO MESMO PARÁGRAFO de uma renúncia — `
            + `o texto diz que não cronometrou e publica a comparação mesmo assim`
          : `${nome}: «…${trecho}…» compara tempo sem medição no mesmo parágrafo`);
      }
    }
  }
}

// O HISTÓRICO fica fora, e não por conveniência: ele é **append-only** por
// regra constitucional — "edição publicada não se reescreve". Um portão que
// exigisse correção nele estaria pedindo para violar a regra que sustenta o
// registro. Quando um número de edição antiga muda, a correção entra como
// edição nova, e é a edição nova que este portão vigia.
const FORA = new Set(["livro/HISTORICO.md"]);

for (const item of itens) {
  if (FORA.has(item.arquivo)) continue;
  const caminho = resolve(RAIZ, item.arquivo);
  if (!existsSync(caminho)) continue;
  conferidos++;
  const md = readFileSync(caminho, "utf8");
  // Fora de bloco de código: ali a unidade de tempo é saída de programa.
  analisa(basename(item.arquivo).replace(/\.md$/, ""), md.replace(/```[\s\S]*?```/g, ""));
}

// Os gabaritos também. O caso do capítulo 21 nasceu no capítulo e foi COPIADO
// para a rubrica de `cap21.exB` — corrigir só um lado deixaria o tutor
// ensinando o que a página deixou de afirmar.
const exercicios = JSON.parse(readFileSync(resolve(RAIZ, "livro/exercicios.json"), "utf8"));
for (const e of exercicios) {
  const texto = [e.enunciado, ...(e.criterios || []), e.erro_provavel, e.resposta_guia]
    .filter(Boolean).join("\n\n");
  analisa(e.id, texto);
}

if (falhas.length) {
  console.error(`✗ desempenho: ${falhas.length} comparação(ões) de tempo sem procedência`);
  falhas.forEach((f) => console.error("   " + f));
  console.error("   → meça no po-zero, ou declare que este handbook não cronometrou.");
  process.exit(1);
}
console.log(`✓ desempenho OK: ${conferidos} capítulos e ${exercicios.length} exercícios · `
  + `${afirmacoesVistas} afirmação(ões) de tempo, todas com medição ou renúncia por perto`);
