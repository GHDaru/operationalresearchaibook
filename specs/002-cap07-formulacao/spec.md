# Spec 002 — Capítulo 07: Formulação de modelos lineares

**Rodada:** 002 · **Raia:** plena · **Branch:** `claude/handbook-pesquisa-operacional-ucbbpu`
· **Data:** 2026-08-06 · **Status:** aguardando aprovação do autor

## O quê

Escrever o **capítulo 07 — Formulação de modelos lineares**, primeiro capítulo de método do
handbook e abertura da Parte II (Programação Linear), com tudo o que a Definition of Done
(DoD) de capítulo exige: exercícios que corrigem, vídeo curado e a etapa correspondente do
`po-zero`.

## Por quê

É **o capítulo mais praticado do livro**, e o único cuja ausência trava todos os outros: sem
saber traduzir uma situação em variáveis, objetivo e restrições, não há o que resolver por
Simplex, dualidade ou *branch-and-bound*.

Ele também é o capítulo onde o handbook se separa dos dois livros-base. Ambos tratam
formulação como preâmbulo dos algoritmos; aqui ela é **a habilidade central**, e o algoritmo
vem depois — coerente com o Princípio II da constituição, *modelar antes de resolver*.

Por fim, é a rodada que **fecha três dívidas** declaradas na edição 0.1: nenhum capítulo de
método publicado (Princípio I), `po-zero` sem etapas (Princípio IV), e a máquina de exercícios
nunca exercitada de ponta a ponta.

## Escopo

### Entra

- **`livro/capitulos/07-formulacao.md`**, no esqueleto obrigatório do
  [Guia Editorial §2](../../livro/GUIA-EDITORIAL.md).
- **4 exercícios** em `livro/exercicios.json` (série `cap07`, variantes A–D), cobrindo os
  gêneros que importam em Pesquisa Operacional (PO): formular, diagnosticar, interpretar e —
  na variante D — formular sobre o **próprio problema do leitor**.
- **1 vídeo curado**, com autor, duração e a frase "o que ele resolve".
- **`po-zero/etapa-01-formulacao/`** — o primeiro caso modelado, resolvido em PuLP com HiGHS,
  com `experimento.py` que regenera os números citados no capítulo.
- **Capacidade nova no tutor** (`formulacao`), espelhada nos dois lados do portão.
- Registro: `livro/HISTORICO.md`, `livro/videoteca.md` e, se algum artigo for usado,
  `radar/RADAR.md` + `livro/bibliografia.md`.

### Não entra

- Resolução gráfica e geometria da região viável — **capítulo 08**, rodada seguinte.
- Qualquer coisa sobre o Simplex. O capítulo termina no modelo escrito e resolvido **por
  chamada ao solver**, deliberadamente tratado como caixa-preta.
- Variáveis inteiras ou binárias — Parte IV. Aqui aparecem só como "quando não serve".

## Objetivos de aprendizagem (proposta)

Vão para o capítulo e **cada exercício rastreia a um deles**:

- **O1.** *Distinguir*, numa situação descrita em prosa, o que é variável de decisão, o que é
  parâmetro, o que é objetivo e o que é restrição.
- **O2.** *Formular* um modelo linear completo, com unidades coerentes dos dois lados de cada
  restrição.
- **O3.** *Diagnosticar* erros clássicos de formulação a partir do modelo e da sua saída.
- **O4.** *Avaliar* quando a formulação linear não serve, e o que assume dali em diante.

## Decisões de conteúdo

1. **O capítulo começa por um erro.** O *worked example* de abertura é um modelo que maximiza
   **receita** em vez de margem de contribuição — erro real, comum, e cuja saída parece
   plausível. É o que instala a desconfiança que o handbook quer treinar.
2. **A pergunta-âncora é "o que quem decide pode escolher?".** Ela separa variável de
   parâmetro e resolve, sozinha, a maioria dos erros de formulação de iniciante.
3. **Unidades são tratadas como ferramenta de verificação**, não como formalismo. Restrição com
   unidades incoerentes dos dois lados é o erro mais barato de pegar e o mais caro de deixar
   passar.
4. **O solver é caixa-preta neste capítulo, e isso é dito ao leitor** — com a promessa
   explícita de que os capítulos 08 a 11 abrem a caixa. Prometer e cumprir é o que separa
   sequência didática de omissão.

## Critérios de aceite

| # | Critério | Como verificar |
|---|---|---|
| A1 | O capítulo existe e está no sumário publicado | `livro/capitulos/07-formulacao.md` presente e declarado em `publicar/sumario.json` |
| A2 | Cabeçalho com selo de datação | Primeiro *blockquote* no padrão do Guia Editorial §2.1 |
| A3 | Todas as seções obrigatórias do esqueleto, **inclusive "quando não serve"** | Inspeção contra o Guia Editorial §2 |
| A4 | 4 exercícios na série `cap07`, cada um com 3 a 5 critérios | `verifica-exercicios.mjs` verde |
| A5 | Todo exercício aponta para um objetivo **que existe** no capítulo | Portão do build |
| A6 | Variante D sem `resposta_guia`; A, B e C com | `verifica-exercicios.mjs` verde |
| A7 | Rubrica **não publicada** no site, no Markdown baixável nem no grafo | `verifica-exercicios.mjs` verde |
| A8 | O capítulo monta a bateria | `<div data-bateria="cap07">` presente |
| A9 | Ao menos 1 vídeo, com autor, duração e justificativa | Inspeção + entrada no índice da videoteca |
| A10 | `po-zero/etapa-01-formulacao/experimento.py` roda do zero e **reproduz** `resultados.json` | Executar duas vezes e comparar |
| A11 | `resultados.json` declara versões de Python, bibliotecas e solver | Inspeção do arquivo |
| A12 | **Todo número citado no capítulo** vem do experimento | Conferência número a número contra `resultados.json` |
| A13 | Espelho de capacidades em sincronia | `verifica-espelho.mjs` verde |
| A14 | Build inteiro verde | `cd publicar && npm run build` sai 0 |
| A15 | Testes do backend verdes | `python -m pytest -q` sai 0 |
| A16 | Nenhuma sigla nasce nua no capítulo | Inspeção da primeira ocorrência de cada uma |
| A17 | Histórico atualizado com a edição | Entrada nova em `livro/HISTORICO.md` |

## Pontos a esclarecer com o autor (*clarify*)

Três decisões que mudam o resultado e que não cabe a mim tomar:

1. **O domínio do exemplo condutor.** O capítulo inteiro se apoia num caso único, retomado da
   abertura ao `po-zero`. Ele deve sair da sua prática (planejamento e cadeia de suprimentos) ou
   de um domínio neutro de fábrica? Um caso reconhecível pela sua turma vale mais do que um
   genérico — mas só você sabe qual é.
2. **O livro passa a publicar fora de ordem.** Com o capítulo 07 no ar e as vagas 01 a 06
   ainda vazias, o sumário salta de 00 para 07. Proponho um **marcador visível de vaga
   declarada** na navegação, para o leitor entender que é ordem do mapa e não conteúdo
   faltando por descuido. Confirma?
3. **O vídeo.** A primeira escolha é o canal do João Sarubbi, cujo uso está autorizado. Não
   consigo inventariar o canal daqui (o YouTube bloqueia a leitura automatizada). **Você indica
   o vídeo de formulação/modelagem**, ou prefere que eu proponha uma alternativa aberta —
   DCC035/UFMG — e você troque depois?

## Riscos

| Risco | Mitigação |
|---|---|
| O capítulo virar uma lista de exemplos sem espinha | O caso condutor é **um só**, retomado em todas as seções; exemplos adicionais entram como exercício, não como texto |
| Exercício de formulação ser difícil de avaliar por rubrica | Os critérios são escritos sobre **fatos verificáveis** do modelo (unidade declarada, objetivo em margem, uma restrição por recurso), não sobre "qualidade da modelagem" |
| A etapa do `po-zero` crescer além do capítulo | Contrato de etapa do [`po-zero/README.md`](../../po-zero/README.md): roda em minutos, instância pequena, versões declaradas |
| Primeira vez que a máquina de exercícios roda de ponta a ponta | É risco assumido e é **parte do valor desta rodada**: descobrir o que quebra com um capítulo real, e não com nove |
