# Guia Editorial — regras operacionais do handbook

> **Conteúdo revisado em 2026-08** · versão operacional das orientações pedagógicas. A lei
> está na [constituição](../.specify/memory/constitution.md); este guia é o que se consulta
> **enquanto escreve**.

## 1. O framework pedagógico em quatro linhas

| Framework | O que dita no handbook |
|---|---|
| **Backward Design** | Todo capítulo se projeta de trás para frente: objetivos → evidências (exercícios) → só então o conteúdo |
| **4C/ID** | Etapas do `po-zero` = tarefas inteiras; capítulos = informação de apoio; boxes no código = *just-in-time*; exercícios = treino de parte |
| **Diátaxis** | Quatro tipos de texto, nunca misturados na mesma seção: capítulo = *explanation*, `po-zero` = *tutorial*, banco e fichas = *reference*, receitas = *how-to* |
| **Carga Cognitiva** | *Worked example* antes do exercício; exercícios são "complete", não "crie do zero"; o andaime diminui capítulo a capítulo; uma ideia nova por vez |

## 2. Esqueleto de capítulo (obrigatório)

A ordem não é decorativa: ela é o Backward Design tornado sumário.

1. **Objetivos de aprendizagem** — 3 a 5, com verbos de Bloom (formular, comparar,
   implementar, avaliar), numerados `**O1.**`, `**O2.**`… Os identificadores são reais: cada
   exercício aponta para um deles, e o build falha se apontar para um que não existe.
2. **O problema** — por que este assunto existe. **Comece pelo erro que alguém comete sem
   ele**, de preferência um erro de modelagem com consequência visível.
3. **De onde isto veio** — obrigatória em capítulo de método (constituição, Princípio XII). Ver
   §2.2.
4. **A intuição** — o método em linguagem natural e, quando possível, em geometria. Nenhuma
   fórmula ainda.
5. **A matemática** — a formulação, o teorema, a demonstração quando ela ensina. Notação
   declarada antes do uso.
6. **O algoritmo** — o método passo a passo, com um exemplo pequeno percorrido à mão
   (*worked example*).
7. **O código** — a etapa do `po-zero`: implementação didática ao lado do solver de mercado,
   com os números do capítulo regeneráveis por script.
8. **Quando não serve** — obrigatório (constituição, Princípio II). Os limites do método, o
   que o degrada, e qual família de método assume dali em diante.
9. **Fundamentos científicos** — 2 a 4 artigos *traduzidos para decisões* ("o resultado X
   significa que, na prática, você deve Y"); ponteiro para a [bibliografia](bibliografia.md) e
   para o [Radar](../radar/RADAR.md).
10. **Pratique** — os exercícios (mínimo 3). Ver §4.
11. **Assista** — os vídeos curados (mínimo 1). Ver §5.
12. **Síntese + "o que levar"** — leitura executiva e as ideias exportáveis para o trabalho do
    leitor.
13. **Verificação** — 2 a 3 perguntas abertas que testam exatamente os objetivos do item 1.

Capítulos da camada de **fronteira** acrescentam **O estado da arte**, com a *cláusula de
expiração* explícita (constituição, Princípio V).

### 2.1 Cabeçalho obrigatório

```markdown
# 09 — O método Simplex

> **Conteúdo revisado em 2026-08** · última revisão 2026-08-20 · [histórico](HISTORICO.md)
```

O selo diz ao leitor se o conteúdo está fresco — o que a data de um evento citado no corpo não
faz.

### 2.2 A seção "De onde isto veio" (Princípio XII)

Obrigatória em capítulo de método. Não é caixa de curiosidade: é a seção que dá ao leitor um
**motivo para não pular para a fórmula**.

O que ela precisa entregar, nesta ordem:

| Elemento | A pergunta que responde |
|---|---|
| **O aperto** | Quem estava preso, em quê, quando. Um problema do mundo, com data e gente |
| **O que se fazia antes** | Contra o quê o método compete. Sem isto, não dá para medir o salto |
| **A virada** | Qual foi a ideia que destravou — em linguagem natural, sem notação |
| **A ideia reaproveitável** | O padrão de raciocínio que serve **fora** deste algoritmo |
| **O nome** | Se o nome tem origem, ela é contada |

Regras de escrita:

- **História é afirmação.** Data, autoria e atribuição exigem fonte, e fonte não confirmada na
  primária é marcada `⏳` e **não sustenta afirmação** (Princípio III). Este é o terreno mais
  fácil do livro para inventar, porque história inventada soa bem.
- **Distinga o que é documentado do que é atribuição corrente.** "A literatura didática atribui
  a X" não é a mesma frase que "X publicou em 19NN", e as duas não podem parecer iguais.
- **Corte o que não muda nada.** Se o parágrafo sai sem o leitor perder compreensão ou
  julgamento, ele é enfeite. O teste é o do `combater-amontoado`.
- **Sem heroísmo.** O gênio solitário é uma história ruim e geralmente falsa: métodos nascem de
  instituições, encomendas e restrições materiais, e é isso que ensina.

## 3. Regras de escrita permanentes

- **Intuição → matemática → código**, nessa ordem. Uma fórmula que aparece antes da intuição é
  carga cognitiva pura (constituição, Princípio II).
- **Nenhum número sem procedência.** Nem "cerca de 10× mais rápido", nem "converge em poucas
  iterações". Ou mede com um script do `po-zero`, ou cita, ou não afirma.
- **Toda comparação de algoritmos declara** instâncias, *baseline*, critério de parada,
  máquina, semente e versão de solver. Sem isso não é resultado, é anedota.
- **Todo método declara quando não serve.** Um capítulo que só elogia o próprio método está
  incompleto.
- **Uma ideia nova por seção.** Se a seção precisa de duas, são duas seções.
- **Notação antes do uso.** Símbolo novo é apresentado onde aparece pela primeira vez, e
  entra no [glossário](glossario.md) se atravessar capítulos.
- Termos técnicos consagrados sem tradução forçada (*branch and bound*, *big-M*, *solver*,
  *scheduling*, *benchmark*); traduzidos quando a prática já traduziu (restrição, viabilidade,
  dualidade, folga).
- Tabelas para fatos enumeráveis; explicação vive na prosa, não nas células.

## 4. Como se escreve um exercício

A mecânica está em [`BANCO-DE-EXERCICIOS.md`](BANCO-DE-EXERCICIOS.md). As regras editoriais:

- **Todo exercício rastreia até um objetivo** do capítulo. Sem isso, o build falha.
- **A devolutiva é obrigatória e explica o conceito** — não apenas nomeia a resposta certa.
  Escreva-a pensando em quem errou, não em quem acertou.
- **Aponte a âncora da seção** que resolve a dúvida. É o gesto mais útil do livro.
- **Errar é parte do ciclo**: o gabarito só é revelado na segunda tentativa. Escreva o
  enunciado sabendo que o leitor vai tentar de novo.
- **Distratores plausíveis.** Uma alternativa errada que ninguém marcaria não ensina nada. As
  melhores capturam um **mal-entendido real de modelagem** — confundir restrição com objetivo,
  ler preço-sombra fora da faixa de validade, tratar variável inteira como contínua
  arredondada.
- Ordem de dificuldade dentro do capítulo: reconhecimento → formulação → julgamento.
- Exercício de código é sempre ***completion problem***: complete a lacuna, não escreva do
  zero. Criar do zero é trabalho da etapa do `po-zero`.

### 4.1 O exercício típico de PO

Em Pesquisa Operacional (PO) o exercício mais valioso quase nunca é "calcule". É um destes:

| Tipo | O que treina |
|---|---|
| **Formular** | Dada a situação em prosa, escrever variáveis, objetivo e restrições |
| **Diagnosticar o modelo** | Dado um modelo errado e sua saída, achar o erro de formulação |
| **Ler a saída** | Dada a solução do solver, dizer o que ela autoriza a decidir — e o que não |
| **Escolher o método** | Dada a instância, dizer qual família serve e por quê |
| **Julgar um resultado** | Dado um trecho de artigo, dizer se a comparação sustenta a conclusão |

## 5. Como se escolhe um vídeo

- **Um vídeo entra por aquilo que o texto não faz bem.** Geometria animada, o ritmo de uma
  derivação no quadro, o som de alguém pensando em voz alta. Se o vídeo só repete o capítulo,
  ele não entra — repetição não é reforço, é ruído.
- Declare **autor, duração e o que ele resolve**. O campo de justificativa é obrigatório.
- **Gratuito e estável.** Vídeo atrás de *paywall* não entra: custo zero é requisito.
- **Reconfira os links na janela trimestral.** Link morto é dívida do livro, não do leitor.
- **Fachada por padrão.** O player só pede o vídeo ao servidor de origem depois do clique.
- A curadoria e as fontes autorizadas estão na [Videoteca](videoteca.md).

## 6. Como um artigo científico entra no livro

Pela porta do [Radar](../radar/RADAR.md), nunca por menção solta (constituição, Princípio VI).

1. **Ler e fichar** — o artigo vira uma linha datada no Radar, com veredito e o que ele muda.
2. **Traduzir para decisão** — a seção "Fundamentos científicos" do capítulo não resume o
   artigo; diz o que o leitor deve **fazer diferente** por causa dele.
3. **Verificar a fonte** — DOI ou URL conferido. Fonte não confirmada é marcada `⏳` e **não
   sustenta afirmação**.
4. **Sincronizar** — a entrada correspondente entra na [bibliografia](bibliografia.md).

Artigo que muda uma recomendação publicada **dispara revisão do capítulo**, sem esperar a
janela trimestral.

## 7. Datação, histórico e expiração

1. Todo capítulo declara a data de captura no cabeçalho.
2. Distinguem-se três datas: do **evento** (imutável), da **captura** (quando fotografamos) e
   do **experimento** (quando o número foi medido, com a versão da biblioteca e do solver).
3. Toda edição atualiza o [`HISTORICO.md`](HISTORICO.md), com a versão do modelo de IA usada.
4. Capítulo da camada de fronteira declara **cláusula de expiração**.

Regra de escrita associada: quando uma afirmação for sensível ao tempo ("hoje", "ainda não",
"o consenso atual"), ela está implicitamente sob a data de captura do cabeçalho. Evite
absolutos atemporais ("nunca", "sempre") — exceto os que de fato não expiram, que em PO
costumam ser teoremas.

## 8. Revisão em duas camadas

Antes do *copyedit* de superfície, um passo de **revisão *developmental***: re-ver estrutura e
sentido. O argumento fecha? A ordem serve ao leitor? Há redundância ou lacuna? Os exercícios
testam mesmo os objetivos declarados, ou testam o que foi fácil de perguntar?

"Escrever é reescrever." Nenhum trecho novo é publicado sem esse passo — e **quem escreveu não
revisa** (Maestro, Princípio II): a revisão final passa por agente em contexto fresco.

## 9. Siglas e glossário (política)

- **Toda sigla é apresentada por extenso na 1ª ocorrência** de cada documento — "*Mixed
  Integer Linear Programming* (MILP)" — e dali em diante o texto pode usar só a sigla. A
  contagem reinicia a cada documento.
- O motor reforça isso: envolve automaticamente cada sigla conhecida em `<abbr>`, de modo que
  passar o mouse revela o significado em qualquer ocorrência. O mapa vive em
  `publicar/build.mjs` e é espelhado no [glossário](glossario.md).
- Ao introduzir uma sigla nova, adicione-a **nos dois lugares**.

## 10. Fluxo repetível para um contribuidor

1. **Abrir o tema** — pesquisa dupla (científica + prática de indústria), verificada por busca
   cruzada; registrar lacunas honestamente.
2. **Definir os objetivos primeiro** e, logo em seguida, **os exercícios** — antes de escrever
   o corpo. Se você não consegue escrever o exercício, o objetivo está vago.
3. **Reunir a evidência** — rodar o experimento no `po-zero`; anotar semente, versões e
   números.
4. **Escrever** — no esqueleto da §2, um tipo de texto por seção.
5. **Revisar (developmental)** — §8.
6. **Verificar fontes** — nenhuma URL ou DOI inventado; não confirmado marcado `⏳`;
   sincronizar bibliografia e Radar.
7. **Gate de build** — `npm run build` (em `publicar/`) verde.
8. **Datar** — selo no capítulo e entrada no `HISTORICO.md`.

## 11. Cadência do livro vivo

- **Janela trimestral**: reconferir vídeos, reexecutar os experimentos do `po-zero` com as
  versões correntes de biblioteca e solver, atualizar as datas de revisão.
- **Gatilho extraordinário**: qualquer evento que invalide uma recomendação publicada — um
  resultado replicado que derruba uma prática, um solver que muda de comportamento, uma
  biblioteca descontinuada — dispara revisão pontual do capítulo afetado.
- **Gatilho por telemetria**: exercício com taxa de acerto muito baixa e volume relevante é
  sinal de que **o texto** está mal escrito. Ele entra na fila de revisão.
