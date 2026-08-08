# Banco de Exercícios — sintaxe e como a correção funciona

> **Conteúdo revisado em 2026-08** · documento de **referência**. O *porquê* está na
> [constituição](../.specify/memory/constitution.md) (Princípio I); o *como escrever bem* está
> no [Guia Editorial §4](GUIA-EDITORIAL.md). Aqui está a mecânica.

## Por que a correção mora no servidor

A página que você lê **não conhece a resposta certa**. Quando o leitor responde, a resposta
viaja até o backend do handbook, que corrige, explica e devolve o feedback.

Três razões, nesta ordem:

1. **Feedback melhor.** O servidor sabe quantas vezes o leitor já tentou. Na primeira
   tentativa errada ele explica o conceito e devolve à seção certa; só na segunda revela a
   resposta esperada. Um gabarito embutido no HTML não consegue esperar.
2. **A avaliação por rubrica só existe lá.** Em Pesquisa Operacional (PO) o exercício que mais
   ensina é aberto — "formule este problema", "diga o que está errado neste modelo". Avaliar
   isso exige um modelo de linguagem, e um modelo exige um servidor.
3. **O erro é o sinal mais valioso do projeto.** Saber qual exercício erra mais, e com que
   resposta, é o que corrige o livro. Exercício com taxa de acerto muito baixa é sintoma de
   texto mal escrito — e entra na fila de revisão.

O livro é aberto: quem quiser ver a rubrica acha no repositório. Não estamos escondendo —
estamos evitando que a resposta esteja a um `Ctrl+U` de distância no momento em que o leitor
deveria estar pensando. Há **portão de build** que falha se a rubrica vazar para o site.

**Sem backend configurado**, o exercício continua legível e diz isso honestamente. O livro
nunca finge ter corrigido.

## Onde os exercícios vivem

Em dois lugares que precisam concordar:

| Arquivo | O que é |
|---|---|
| `livro/exercicios.json` | O **registro editorial**: enunciado, critérios de aceite, erro provável e resposta-guia |
| `livro/capitulos/NN-*.md` | O **marcador** `<div data-bateria="capNN">`, que diz onde a bateria daquele capítulo é montada na página |

O motor faz dois recortes do mesmo registro:

| Consumidor | O que recebe |
|---|---|
| `publicar/build.mjs` → a página | título e enunciado, **sem** critérios, **sem** erro provável, **sem** resposta-guia |
| `chat-companion/backend/` (via `build_corpus.py`) | tudo, para poder avaliar |

## Sintaxe do registro

Cada exercício é um objeto em `livro/exercicios.json`:

```json
{
  "id": "cap99.exA",
  "capitulo": 99,
  "serie": "cap99",
  "variante": "A",
  "tipo": "formular",
  "objetivo": "O2",
  "capacidade": "formulacao",
  "titulo": "TITULO CURTO, EXIBIDO NO CARTAO",
  "enunciado": "O TEXTO DO PROBLEMA. Markdown e aceito.",
  "criterios": [
    "PRIMEIRO CRITERIO — um fato verificavel da resposta, nao uma impressao",
    "SEGUNDO CRITERIO — outro fato verificavel",
    "TERCEIRO CRITERIO — de 3 a 5 no total"
  ],
  "erro_provavel": "O MAL-ENTENDIDO COMUM, e por que ele esta errado.",
  "resposta_guia": "A RESPOSTA DE REFERENCIA, para o tutor julgar equivalencia."
}
```

> **Por que o exemplo está em caixa-alta, com um capítulo que não existe.** Há um portão que
> procura, nas páginas publicadas, os 40 primeiros caracteres normalizados de cada campo de
> rubrica. Um exemplo de documentação escrito com texto realista **colide** com a rubrica de um
> exercício real e derruba o build — corretamente, porque nesse ponto o leitor conseguiria
> inferir a rubrica lendo esta página. Aconteceu na primeira vez que este documento e um
> capítulo real coexistiram. Exemplo de sintaxe usa texto que ninguém escreveria de verdade.

### Campos

| Campo | Obrigatório | O que é |
|---|---|---|
| `id` | sim | Padrão `capNN.exX`, com `X` em A–Z. Único no livro inteiro; duplicata quebra o build |
| `capitulo` | sim | Número do capítulo. **Precisa bater com o `NN` do id** |
| `serie` | sim | `capNN` — é por ela que a bateria é montada. **Precisa bater com o id** |
| `variante` | sim | `A`, `B`, `C` ou `D`. **Precisa bater com o id** |
| `tipo` | sim | O gênero do exercício (ver §"Os tipos") |
| `capacidade` | sim | A chave em `chat-companion/backend/capabilities.py`. O portão confere que existe **e que já foi liberada** no capítulo do exercício |
| `titulo` | sim | Nome curto, exibido no cartão |
| `enunciado` | sim | O texto do problema. Markdown é aceito |
| `objetivo` | sim | O `O1`/`O2`… declarado na seção de objetivos do capítulo. **O portão confere que ele existe lá** |
| `contexto` | não | `livro` (padrão) ou `leitor` — ver abaixo |
| `criterios` | sim | **De 3 a 5** critérios de aceite. Menos que 3 não avalia; mais que 5 não é rubrica, é gabarito disfarçado |
| `erro_provavel` | recomendado | O mal-entendido comum, e por que ele está errado. É o que produz devolutiva útil |
| `resposta_guia` | ver abaixo | A resposta de referência, que permite ao tutor julgar equivalência de raciocínio |

### A regra do `contexto`

| `contexto` | Significa | Regra |
|---|---|---|
| `livro` (padrão) | O problema é dado pelo livro | **Exige** `resposta_guia` |
| `leitor` | O leitor traz o próprio problema — a sua operação, a sua turma, o seu dado | **Proíbe** `resposta_guia` |

Não há resposta-guia possível para o problema do leitor, e declarar uma seria mentira.

> **Isto já foi amarrado à letra "D" do identificador.** Funcionava enquanto uma bateria era o
> mesmo exercício em quatro variantes. Quando o capítulo de método gráfico pediu um banco de
> dez, a regra virou arbitrária: nada torna o décimo item mais "do leitor" que o terceiro.
> `contexto` declara a **natureza** do exercício; a letra do identificador declara só a
> **posição** na bateria. Confundir as duas foi o defeito.

## Os tipos

O tipo declara o que o exercício treina. Em PO os cinco que importam são:

| Tipo | O que pede |
|---|---|
| `formular` | Dada a situação em prosa, escrever variáveis, objetivo e restrições |
| `diagnosticar` | Dado um modelo errado e sua saída, encontrar o erro de formulação |
| `interpretar` | Dada a solução do solver, dizer o que ela autoriza a decidir — e o que não |
| `escolher` | Dada a instância, dizer qual família de método serve e por quê |
| `resolver` | Dado o modelo, chegar ao ótimo pelo método do capítulo, mostrando o caminho |
| `julgar` | Dado um trecho de artigo ou um resultado, dizer se a comparação sustenta a conclusão |

## Os portões que isto atravessa

`publicar/verifica-exercicios.mjs` roda depois do build e barra:

1. Campo obrigatório ausente, identificador duplicado, ou identificador que não bate com
   `capitulo`, `serie` e `variante`.
2. Número de critérios fora da faixa de 3 a 5.
3. `contexto: livro` sem resposta-guia, ou `contexto: leitor` com resposta-guia.
4. `capacidade` inexistente em `capabilities.py`, ou liberada num capítulo posterior ao do
   exercício — o tutor não pode avaliar com uma capacidade que o leitor ainda não destravou.
5. **Exercício órfão**: série que existe no registro e não é montada por nenhum capítulo.
6. **Capítulo sem bateria**: Princípio I é não-negociável. Capítulo numerado sem prática falha
   o build, a menos que a dívida esteja **declarada em código**, na lista
   `SEM_BATERIA_DECLARADO`.
7. **Registro divergente do empacotado** no backend — se divergirem, o site publica um
   enunciado e o tutor corrige por outro, com todos os portões verdes. Rode `build_corpus.py`.
8. **Rubrica publicada** — critérios, erro provável ou resposta-guia encontrados no HTML, no
   Markdown baixável ou no grafo.

Enquanto o handbook não tiver capítulo de método publicado, o registro é legitimamente vazio, e
o portão aceita isso **apenas** enquanto o sumário não declarar nenhum capítulo numerado além
da abertura. Publicado o primeiro capítulo de método, o portão volta a exigir registro não
vazio — sem que ninguém precise lembrar de reativá-lo.
