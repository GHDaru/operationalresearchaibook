# ADR 0007 — A fronteira entre defeito de modelo e defeito de método

**Data:** 2026-08-09 · **Status:** aceito · **Rodada:** 006 (capítulo 10)
· **Decisão por:** consulta a especialista, registrada abaixo

## Contexto

O capítulo 10 do handbook trata os quatro vereditos que o Simplex pode devolver quando **não** é
"aqui está seu plano": inviável, ilimitado, múltiplos ótimos e o vértice degenerado — mais a
ciclagem, que o capítulo 09 prometeu explicitamente.

Duas decisões precisavam ser tomadas antes de escrever qualquer linha, e nenhuma era mecânica.

**D1 — a divisão de trabalho entre os capítulos 09 e 10.** O 09 já ensina a **detecção** de dois
dos quatro casos: inviável (artificial sobra na base) e ilimitado (nenhuma razão positiva).
Repetir seria redundância; omitir deixaria o Mapa do handbook mentindo, porque ele promete os
quatro aqui.

**D2 — onde mora a degenerescência no discurso do livro.** Patologia de algoritmo, ou sintoma de
modelo? A resposta muda título de seção, ordem de exposição e o que o aluno leva. E há uma
tensão real: a **ciclagem** é indiscutivelmente um problema da regra de pivoteamento, não do
modelo — e uma instância que cicla é construída de propósito.

### O dado que estava disponível antes da decisão

Duas execuções sobre o Simplex do próprio livro (`po-zero/etapa-03-simplex`), com a instância
clássica de ciclagem, mudando **só a regra de pivoteamento** e mantendo o modelo intacto:

| Regra | Veredito | Pivôs | Repete base? |
|---|---|---:|---|
| **Dantzig** (a que o capítulo 09 ensina) | não termina | estoura o limite | **sim** |
| **Bland** (menor índice na entrada **e** na saída) | ótimo | 6 | não |

E, na montadora com uma restrição redundante que passa pelo vértice ótimo, o **empate no teste da
razão continua existindo sob as duas regras** — é o modelo que o produz.

## Decisão

**D1 — a divisão é assimétrica, e a assimetria é a regra.**

> **Detecção já ensinada no capítulo 09 vira uma linha de tabela com âncora. Detecção inédita
> vira seção.**

O capítulo 09 é o **sintoma**; o 10 é o **diagnóstico e a conduta**. Mas o 10 **ensina a
detecção** de múltiplos ótimos (custo reduzido zero em variável não-básica) e de ciclagem, porque
ali não há redundância a evitar — há lacuna.

O capítulo abre pelo erro, como manda o Guia Editorial: quatro segundas-feiras na mesma
montadora, quatro saídas que não são um plano, e a pergunta *"o que você diz na reunião?"*. Logo
depois, uma **tabela-mapa** com a coluna **"onde se aprende a detectar"**, apontando duas linhas
para o capítulo 09 e duas para o próprio capítulo 10. A fronteira fica **desenhada**, não
deduzida — e o leitor ganha permissão explícita para pular o que já sabe.

**D2 — degenerescência é sintoma de modelo; ciclagem é defeito de regra; e a distinção vira o
teste que o leitor leva embora.**

> **O que é do modelo é o que sobrevive à troca do método. O que some quando você troca o método
> era do método.**

É a *ideia reaproveitável* do capítulo, no sentido do Princípio XII, e ela **sai do experimento
acima**, não de retórica: troque Dantzig por Bland com o modelo intacto e a ciclagem some,
enquanto os empates continuam.

Consequências editoriais que decorrem:

- Degenerescência ganha seção como **fato do modelo** — vértice sobredeterminado, tipicamente por
  restrição redundante —, e o capítulo diz explicitamente que **vértice degenerado é comum e
  legítimo**: é bandeira amarela, não defeito.
- A ciclagem ganha seção própria, declarada como **a única página deste livro em que o defeito é
  do algoritmo**. A contradição com a tese da Parte II é **nomeada**, e é justamente ao nomeá-la
  que ela vira lição.

## Alternativas avaliadas

**Tratar os quatro vereditos com peso igual.** Rejeitada: produziria reensino de metade do
capítulo 09 e um capítulo sem centro. A assimetria é real e esconder isso custa páginas.

**Tratar ciclagem como um grau de degenerescência.** Rejeitada, e é o erro mais tentador —
tecnicamente a ciclagem *requer* degenerescência, então soa natural agrupá-las. Mas isso apagaria
exatamente a distinção que o experimento revela, e deixaria o leitor achando que trocar o modelo
resolve ciclo. Não resolve; trocar a regra resolve.

**Declarar degenerescência como patologia de algoritmo.** Rejeitada por três razões: o capítulo
08 já a define **antes de existir algoritmo no livro** ("três restrições passando pelo mesmo
vértice — sustentado por mais retas do que precisa"); contraria o Princípio II; e é desmentida
pelo experimento, já que os empates sobrevivem à troca de regra.

**Esperar a decisão do autor.** Não era opção nesta rodada: o autor autorizou execução longa e
instruiu consultar especialista, registrar em ADR e prosseguir. Este documento é esse registro —
e a decisão continua **reversível**: nada foi publicado na `main`.

## Consequências

**Boas:**

- O capítulo ganha uma tese própria, testável e transferível, em vez de ser um catálogo de casos.
- A ciclagem deixa de ser advertência de rodapé e vira **fenômeno medido no código do livro** —
  o mesmo movimento que o cubo de Klee–Minty fez no capítulo 09.
- A fronteira 09/10 fica explícita para o leitor, e não só para quem escreve.

**Custosas, e assumidas:**

- **O capítulo 10 fica curto em mecânica de quadro.** Risco de parecer "capítulo de conversa". A
  mitigação é deslocar a mecânica para a etapa 04 do `po-zero` e para exercícios do tipo *ler a
  saída*.
- **Depende do capítulo 09.** Quem pular o 09 sente falta. A tabela-mapa com âncoras é a rampa,
  e ela não reensina.
- **Obriga a corrigir o capítulo 09.** A frase da seção "quando não serve" diz que o código "usa
  a mais simples (menor índice)" para desempatar, sugerindo cobertura parcial contra ciclagem.
  **Não há cobertura nenhuma**: desempatar a linha pelo menor índice não é a regra de Bland. A
  correção entra nesta rodada.
