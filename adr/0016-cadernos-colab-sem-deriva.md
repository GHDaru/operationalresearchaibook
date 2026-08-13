# ADR 0016 — Os cadernos Colab: invólucro, nunca cópia

**Data:** 2026-08-13 · **Rodada:** 011 · **Estado:** decidida sob delegação de longrun
([ADR 0015](0015-longrun-inclui-o-merge-ate-a-v0.md)); aguardando ratificação do autor

## Contexto

O autor acrescentou ao escopo da v0 os **cadernos Colab** — o leitor abre e executa —, com o
pedido explícito de **simplificar, sem evoluir para banco de dados**.

Isso é decisão de médio impacto pela régua da skill `longrun`: cria precedente e muda o que o
leitor recebe. Foi a comitê de três lentes — didática, conformidade, rigor técnico. **Cada
recomendação foi reconferida por medição própria**, e o que segue é o que sobreviveu.

---

## D1 — O caderno é **invólucro que importa o script**, nunca cópia

**Decisão:** o `.py` do `po-zero` é a **fonte única**. O caderno clona o repositório, importa o
módulo e chama funções. **Nenhuma linha de algoritmo é duplicada no caderno** — proibido `def` e
`class` nas células.

**Por quê, e as três lentes convergiram por caminhos diferentes:**

- **Didática:** *"`faixa_de_validade` publicou 13/2 onde o certo era 6; uma cópia em caderno ainda
  estaria exibindo o número errado hoje, com ar de autoridade."*
- **Conformidade:** caderno é artefato que produz números, logo herda o Princípio XI e a
  [ADR 0014](0014-relatorio-de-sensibilidade-e-a-faixa-medida.md) D3 — *"número no livro tem dono,
  e o dono é um teste"*.
- **Técnica:** a alternativa de **gerar** o caderno a partir do `.py` por conversor foi **testada e
  quebra**. Os módulos resolvem caminho por `Path(__file__)`, que não existe num caderno:
  `NameError: name '__file__' is not defined`. Conseguir isso exigiria refatorar seis módulos —
  contra o pedido de simplicidade.

**Reconferido por medição própria:** rodei o protótipo do comitê — 4 testes verdes, 6 células,
**0 com saídas gravadas, 0 com `def`/`class`**.

## D2 — A unidade é a **Parte**, com uma seção por capítulo

**Decisão:** um caderno por Parte do livro, espelhando a etapa do `po-zero` (que já é uma por
Parte, [ADR 0013](0013-o-que-e-a-v0.md) D3), com uma seção por capítulo dentro dele.

**Por quê:** o que dá sentido ao código é a **instância-fio da Parte**. A montadora atravessa os
capítulos 07 a 15; um caderno por capítulo a redigitaria cinco vezes e obrigaria o leitor a
recontextualizar cenário a cada abertura — e o `dual.py` já se recusa a redigitar a instância. Um
caderno único para o livro inteiro perde o *"abro e caio onde eu estava lendo"*.

## D3 — Saída gravada no `.ipynb` é **defeito**, não conveniência

**Decisão:** caderno é commitado **limpo** — sem `outputs`, sem `execution_count` — e o portão
falha se houver.

**Por quê:** uma célula com saída salva é **número publicado fora de qualquer portão**. É
exatamente a classe de defeito das duas faixas erradas, ressuscitada num artefato que o
`verifica-capitulos.mjs` não olha. Foi o achado que a lente didática nomeou como *"o que este
handbook vai esquecer"*, e ela estava certa: eu ia esquecer.

## D4 — O caderno é **conveniência**, e a trilha padrão não depende dele

**Decisão:** todo caderno roda **localmente sem Colab**, e o link para o Colab é opcional e
declarado como tal na página.

**Por quê, com o texto na mão.** A lente de conformidade fez uma correção que este registro
preserva porque ela me pega num erro: **a constituição não contém as palavras "vendor-agnóstico",
"neutralidade" nem "fornecedor"** — conferido, zero ocorrências. O que existe é o Princípio IV,
literal: *"O handbook nasce de código que roda em CPU, sem licença paga"* e *"Custo zero é
requisito, não preferência… nunca como dependência"*.

Conta Google gratuita **não** é licença paga, então o IV não barra o Colab. O que ele barra é a
**dependência**: se o único artefato que regenera um número vivesse no Colab, o experimento teria
deixado de rodar na CPU do leitor. Daí a condição — o caderno é espelho de conveniência, e o `.py`
continua sendo o experimento.

> **Registro de erro meu, para não se repetir.** Eu havia argumentado "o handbook é
> vendor-agnóstico por princípio constitucional". Não é: é decisão de ADR (a 0014, D1), não
> princípio. É a terceira vez que atribuo à constituição algo que ela não diz — as anteriores
> foram uma promessa de anonimato e o mesmo tipo de invocação. **Citar a constituição exige
> `grep`, não memória.**

## D5 — O caderno tem de fazer o que a página não faz

**Decisão:** todo caderno traz, no mínimo, **uma célula "mexa aqui"** e **o erro rodado antes da
correção**.

**Por quê:** senão o caderno é um script com botão. No livro, o modelo certo e o errado aparecem
lado a lado e o leitor nunca chega a errar; no caderno ele roda o errado, se compromete com uma
conclusão, e **só então** vê o certo. É o exercício `diagnosticar` encenado — a única coisa aqui
que a página impressa não consegue fazer.

## D6 — Nenhum caderno existe antes de o CI cobrir a medição

**Decisão, e ela foi executada antes desta ADR ser escrita:** o CI passou a rodar `po-zero`.

**Por quê:** o comitê achou que o CI **nunca** rodou aqueles testes — o filtro `paths:` listava
`livro/`, `publicar/` e `chat-companion/`, e não `po-zero/`, e não havia passo que os executasse.
São as seis suítes que sustentam o selo 🔵. **Acrescentar artefato novo a um pipeline que não cobre
o antigo é multiplicar o buraco**, então o conserto veio primeiro.

## D7 — O teste do caderno roda **sem rede** e contra o código de hoje

**Decisão:** um `pytest` lê o `.ipynb` como JSON — ele é JSON —, concatena as células de código e
executa num namespace único, com o clone substituído por um atalho para a árvore de trabalho.
Quatro asserções: sem saídas gravadas; sem `def`/`class`; sem magias de IPython; e tudo executa
com os `assert` passando.

**Nada novo a instalar** — Jupyter não é necessário. **Proibidas as magias** `!git clone` e `%cd`:
não são Python e impediriam o teste local; usa-se `subprocess.run` e caminho relativo, que roda
idêntico nos dois lugares.

**Provado mordendo:** o comitê simulou deriva renomeando uma função na chamada do caderno, e o
teste falhou em 0,04 s. Reconferido aqui.

---

## O que foi descartado, e por quê

| Descartado | Motivo |
|---|---|
| Caderno **gerado** do `.py` por conversor | Testado: quebra em `__file__`. Consertar exige refatorar seis módulos, contra o pedido de simplicidade |
| `.ipynb` com saídas gravadas | Número publicado sem dono — a classe de defeito das duas faixas erradas |
| Um caderno por **capítulo** | Redigitaria a instância-fio cinco vezes; carga cognitiva pura |
| Um caderno **único** para o livro | Perde o "abro e caio onde eu estava lendo" |
| Teste com rede como padrão | Torna o CI flaky. Fica como marcador opcional, se um dia houver execução noturna |

## Consequências

**Boas.** Zero linha de algoritmo duplicada; o caderno lê o código que publica. O leitor ganha as
duas coisas que a página não dá: mexer num parâmetro e ver o preço deixar de valer, e **errar
antes de ver o certo**.

**Ruins, e declaradas.** O invólucro **esconde o algoritmo atrás de um `import`**, e a regra das
duas implementações existe para o código ser lido. Mitigação decidida: exibir a fonte com
`inspect.getsource` no ponto que ensina, e exigir que cada caderno tenha **ao menos uma célula
cuja saída não está no livro** — senão ele é redundante. Segundo custo: ~15 s de `git clone` por
sessão, e a assinatura pública das funções vira contrato.

**O sinal que faria esta decisão ser revista:** um caderno que precise de `def` para ser
compreensível. Aí o problema não é a regra — é que o script está mal fatiado, e é ele que muda.

## Dívida registrada, achada pelo comitê

`po-zero/README.md` ainda diz *"uma etapa por capítulo de método"*, contradizendo a ADR 0013 D3,
que mudou a unidade para a **Parte**. Como a estrutura dos cadernos deriva dele, isso é corrigido
nesta rodada.
