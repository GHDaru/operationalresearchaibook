# Spec 009 — Lote 1: fechar a Parte II, mais duas antecipações

**Data:** 2026-08-12 · **Raia:** plena · **Unidade:** a **Parte**, não o capítulo
([ADR 0013](../../adr/0013-o-que-e-a-v0.md), D1) · **Estado:** aguardando ratificação do autor

## O lote

| Vaga | Capítulo | Estado-alvo | Por quê neste lote |
|---|---|---|---|
| 11 | Simplex revisado e implementação eficiente | 🔵 **medido** | Já tem spec/plan/ADRs da rodada 008, e duas dívidas publicadas cobram |
| 12 | Dualidade | 🟡 v0 | **O maior destravamento do livro** — 13, 19, 20, 25, 27, 28, 29, 40 e toda a Parte X dependem |
| 13 | Análise de sensibilidade e pós-otimização | 🟡 v0 | A parte que o gestor usa. Nasce com dívida histórica declarada |
| 14 | Métodos de pontos interiores | 🟡 v0 | Fonte primária já levantada (Khachiyan, Karmarkar) |
| 15 | Modelagem aplicada em PL | 🟡 v0 | Fecha a Parte e é pré-requisito da Parte X |
| **38** | Convexidade | 🟡 v0 | **Antecipado.** O capítulo 09 já a usa a crédito; escrevê-la agora deixa ~40 capítulos **apontarem** em vez de reexplicar |
| **77** | Como ler um artigo científico de PO | 🟡 v0 | **Antecipado.** Barato, sem método, e dá ao resto do livro o direito de **citar em vez de explicar** — antídoto do risco de fabricação |

## O que já está feito

**A sessão de história da Parte** ([estudo 004](../../estudos/004-historia-parte-II.md)) — que por
D4 é pré-requisito de qualquer linha de capítulo. Sete fontes com metadados no Crossref **e**
existência no registro; **duas dívidas nomeadas** que não serão preenchidas com invenção.

## A instância-fio do lote

**A montadora continua**, e é decisão, não inércia: ela atravessa 07/08/09/10 e é metade da razão
de aqueles capítulos funcionarem. O leitor não reaprende cenário; o autor não inventa sete
fábricas.

| Capítulo | O que a montadora mostra aqui |
|---|---|
| 11 | O mesmo quadro final, relido como $B^{-1}$ e $y$ |
| 12 | **O dual da montadora** — os `50` da linha $z$ ganham nome: preço da CPU e do pente |
| 13 | Quanto o estoque pode variar antes de o plano mudar |
| 14 | O mesmo ótimo, alcançado por dentro em vez de pelas quinas |
| 15 | A montadora **generalizada** — de duas variáveis para o padrão de mistura |

## Objetivos e exercícios — três e três, um para um

Por D5. Cada capítulo tem **O1, O2, O3** e **exA, exB, exC**, nesta progressão:

| | Tipo | Rastreia |
|---|---|---|
| **A** | `formular` ou `resolver` — reconhecimento e mecânica | O1 |
| **B** | **`diagnosticar`** — um modelo errado que rodou e devolveu ótimo | O2 |
| **C** | `interpretar`, `escolher` ou `julgar` — *a conta está certa e a conclusão está errada* | O3 |

**O item B é inegociável.** É o único que treina o erro caro em Pesquisa Operacional (PO) — o de
formulação.

### Capítulo 12 — Dualidade

- **O1** — Escrever o dual de um modelo primal e dizer o que cada variável dual **significa** no
  problema, em unidade e sinal.
- **O2** — Diagnosticar um modelo em que o preço-sombra foi lido **fora da faixa de validade**.
- **O3** — Julgar uma decisão de negócio tomada a partir de preço-sombra, e dizer quando ela não
  se sustenta.

### Capítulo 13 — Sensibilidade

- **O1** — Ler um relatório de sensibilidade e dizer o que cada faixa autoriza.
- **O2** — Diagnosticar a leitura de faixa em modelo **degenerado**, onde o preço-sombra é ambíguo
  (encadeia no capítulo 10).
- **O3** — Decidir se uma mudança de dado exige **resolver de novo** ou se a resposta já está lá.

### Capítulo 14 — Pontos interiores

- **O1** — Explicar o que "atravessar em vez de contornar" significa geometricamente.
- **O2** — Diagnosticar quando a resposta de um método interior **não é vértice** e o que isso
  quebra na leitura.
- **O3** — Escolher entre Simplex e ponto interior para uma instância descrita, e justificar.

### Capítulo 15 — Modelagem aplicada

- **O1** — Reconhecer o padrão (mistura, cobertura, transporte) num enunciado em prosa.
- **O2** — Diagnosticar um modelo cujo padrão foi escolhido errado.
- **O3** — Julgar se o modelo responde à pergunta que foi feita.

### Capítulo 38 — Convexidade

- **O1** — Decidir se um conjunto dado é convexo, e dizer por quê.
- **O2** — Diagnosticar um modelo em que o ótimo local **não** é global, e identificar o que
  quebrou a convexidade.
- **O3** — Julgar a afirmação "o solver achou o ótimo" quando o modelo não é convexo.

### Capítulo 77 — Como ler um artigo

- **O1** — Aplicar as três passadas a um artigo de PO.
- **O2** — Diagnosticar uma afirmação de desempenho que o artigo **não sustenta** (instância não
  declarada, comparação sem controle).
- **O3** — Decidir se um resultado publicado se aplica ao **seu** problema.

## Critérios de aceite

| # | | Critério |
|---|---|---|
| **A1** | M | Cada capítulo tem exatamente **3 objetivos** e **3 exercícios**, um para um, e o exercício B é `diagnosticar` |
| **A2** | M | Os três portões novos passam em todo capítulo: "quando não serve", "Assista", piso de 3 |
| **A3** | M | Todo capítulo declara `maturidade` no `sumario.json`, e o portão o verifica |
| **A4** | M | Nenhum capítulo 🟡 publica número que não saiba regenerar (D3) |
| **A5** | M | Nenhuma fonte nova sem passar pelo portão de fontes — DOI existe no registro |
| **A6** | H | Capítulo sem fonte histórica publica **"De onde isto veio — em dívida"**, nomeando o que falta |
| **A7** | M | Build verde, testes verdes, 9 portões |
| **A8** | H | **Revisão em contexto fresco do lote inteiro**, lido como leitor — seguindo o fio, não capítulo a capítulo |
| **A9** | M | Um commit por capítulo, para o autor poder rejeitar um sem rejeitar os outros |
| **A10** | H | Dossiê de gate: uma página por capítulo |

## O que este lote NÃO faz, declarado

- **Não escreve a prova.** ADR 0013, D6 — produto separado, raia infra.
- **Não promove nenhum capítulo a ✅** salvo o 11, que tem medição própria.
- **Não toca texto publicado** sem item explícito de ratificação.
