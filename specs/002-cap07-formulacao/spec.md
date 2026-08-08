# Spec 002 — Capítulo 07: Formulação de modelos lineares

**Rodada:** 002 · **Raia:** plena · **Branch:** `claude/handbook-pesquisa-operacional-ucbbpu`
· **Versão:** 2 · **Data:** 2026-08-06 · **Status:** revisada, aguardando aprovação do autor

> **Por que há uma versão 2.** A versão 1 desta spec listava, em *clarify*, a pergunta "qual o
> domínio do exemplo condutor?". O capítulo foi implementado **antes** de ela ser respondida —
> os gates de aprovação da spec e do plano foram encurtados, e o capítulo nasceu com um exemplo
> genérico de marcenaria. O autor então forneceu o exemplo que usa em sala. Esta versão o
> incorpora, e o capítulo será **refeito** em cima dela.
>
> O registro fica: o processo não é cerimônia. O gate existia exatamente para isso.

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

## O exemplo condutor: montagem de computadores (MRP inverso)

O exemplo é do autor, usado em sala. Ele substitui a marcenaria da versão 1 e passa a ser o
caso único do capítulo, da abertura ao `po-zero`.

**A situação.** Último dia do mês numa montadora. Tudo que entrar no estoque é vendido — a
demanda não é restrição. Dois produtos:

| Produto | Lucro | CPU | Memória |
|---|---|---|---|
| **Tipo 1** | R$ 100 | 1 | 16 GB = **1 pente** |
| **Tipo 2** | R$ 150 | 1 | 32 GB = **2 pentes** |

É *MRP inverso*: em vez de partir da demanda e explodir a lista de materiais para saber o que
comprar, parte-se do **estoque que existe** e pergunta-se o que dá para montar.

### A narrativa em três etapas

A força do exemplo está na ordem em que ele é revelado. Cada etapa instala uma ideia e deixa
uma pergunta aberta.

**Etapa 1 — sem restrição nenhuma.** Quanto se ganha? *Infinito.* O modelo é **ilimitado**, e a
lição chega antes de qualquer fórmula: **um sistema sem restrição não é um sistema modelável**.
Todo sistema real tem pelo menos uma — ponte natural com a Teoria das Restrições, e um começo
mais honesto do que apresentar restrições como burocracia do método.

**Etapa 2 — só a CPU.** 10 CPUs em estoque, memória infinita. Cada máquina usa exatamente uma
CPU, então a intuição responde na hora: **10 do Tipo 2, R$ 1.500**. E está certo.

Aqui vem a pergunta que sustenta o resto da Parte II: *você tem certeza? Como prova?* A
intuição acertou — mas não sabe dizer **por quê**, nem daria a resposta certa num caso um pouco
maior. A pergunta fica **em suspenso, declarada como promessa**: a geometria mostra por que
basta olhar os vértices, e a dualidade entrega o certificado.

**Etapa 3 — entra a memória.** 12 pentes de 16 GB. Agora o aluno propõe um plano que respeite
as duas restrições, e só depois se confere.

$$
\begin{aligned}
\text{maximizar} \quad & 100\,x_1 + 150\,x_2 \\
\text{sujeito a} \quad & x_1 + x_2 \le 10 && \text{(CPUs)} \\
& x_1 + 2\,x_2 \le 12 && \text{(pentes de 16 GB)} \\
& x_1,\, x_2 \ge 0
\end{aligned}
$$

### Por que este exemplo é bom: as duas intuições se contradizem, e as duas erram

| Plano | CPUs | Pentes | Lucro |
|---|---|---|---|
| 10 do Tipo 1 | 10/10 | 10/12 | R$ 1.000 |
| 6 do Tipo 2 | 6/10 | 12/12 | R$ 900 |
| **8 do Tipo 1 + 2 do Tipo 2** | **10/10** | **12/12** | **R$ 1.100** |

E as duas heurísticas gulosas que o aluno naturalmente inventa **apontam para lados opostos**:

- **Lucro por CPU** — Tipo 2 (R$ 150) contra Tipo 1 (R$ 100) → *"faça o Tipo 2"*. Dá R$ 900.
- **Lucro por pente** — Tipo 1 (R$ 100) contra Tipo 2 (R$ 75) → *"faça o Tipo 1"*. Dá R$ 1.000.

Nenhuma das duas chega em R$ 1.100. **O ótimo é uma mistura, e nenhuma regra de bolso o
encontra.** É a demonstração mais barata que existe de por que o método precisa existir — e ela
cabe em dois produtos e duas restrições.

> Números conferidos com HiGHS antes de entrarem nesta spec. Viram `po-zero/etapa-01-formulacao`
> na implementação, com `resultados.json` regenerável.

## Decisões de conteúdo

1. **O capítulo segue a narrativa em três etapas**, não a exposição direta do modelo. O
   ilimitado vem primeiro, de propósito.
2. **A pergunta "como provar?" é declarada como promessa**, com o capítulo dizendo qual capítulo
   futuro a paga. Prometer e cumprir é o que separa sequência didática de omissão.
3. **As duas heurísticas gulosas são apresentadas e refutadas com números.** É o coração do
   capítulo, e substitui o erro receita-versus-margem da versão 1.
4. **A pergunta-âncora continua sendo "o que quem decide pode escolher?"** — ela é o que separa
   variável de parâmetro, e o exemplo a exercita bem (o estoque é dado, a montagem é escolha).
5. **O solver segue caixa-preta neste capítulo**, com a dívida dita ao leitor.

## O que muda em relação ao que já está implementado

| Artefato | O que acontece |
|---|---|
| `livro/capitulos/07-formulacao.md` | **Reescrito** em cima do novo exemplo condutor |
| `po-zero/etapa-01-formulacao/` | Instância e modelos **refeitos**: três etapas (ilimitado, uma restrição, duas), mais as duas heurísticas gulosas para refutação numérica |
| `cap07.exA` a `exD` | **Mantidos.** Usam padaria e metalúrgica de propósito: exercitar em contexto diferente do exemplo condutor é transferência, não inconsistência |
| Sumário, capacidade do tutor, portões | Sem mudança |

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

1. ~~O domínio do exemplo condutor.~~ **Respondido:** montagem de computadores, MRP inverso.
2. **O livro passa a publicar fora de ordem.** Com o capítulo 07 no ar e as vagas 01 a 06
   ainda vazias, o sumário salta de 00 para 07. Proponho um **marcador visível de vaga
   declarada** na navegação, para o leitor entender que é ordem do mapa e não conteúdo
   faltando por descuido. Confirma?
3. **O vídeo.** Segue aberto. A primeira escolha é o canal do João Sarubbi, cujo uso está
   autorizado, mas o YouTube bloqueia leitura automatizada daqui e a Videoteca exige autor e
   duração conferidos. **Você indica o vídeo**, ou aprova uma alternativa aberta.
4. **Confirmação do exemplo.** Os números acima batem com o que você usa em sala? Em especial:
   o Tipo 2 leva **dois pentes de 16 GB** (e não um pente de 32 GB), que é o que faz a
   restrição de memória ser `x1 + 2·x2 ≤ 12`. Se na sua versão os pentes de 32 GB são um item
   separado de estoque, o modelo muda.

## Riscos

| Risco | Mitigação |
|---|---|
| O capítulo virar uma lista de exemplos sem espinha | O caso condutor é **um só**, retomado em todas as seções; exemplos adicionais entram como exercício, não como texto |
| Exercício de formulação ser difícil de avaliar por rubrica | Os critérios são escritos sobre **fatos verificáveis** do modelo (unidade declarada, objetivo em margem, uma restrição por recurso), não sobre "qualidade da modelagem" |
| A etapa do `po-zero` crescer além do capítulo | Contrato de etapa do [`po-zero/README.md`](../../po-zero/README.md): roda em minutos, instância pequena, versões declaradas |
| Primeira vez que a máquina de exercícios roda de ponta a ponta | É risco assumido e é **parte do valor desta rodada**: descobrir o que quebra com um capítulo real, e não com nove |
