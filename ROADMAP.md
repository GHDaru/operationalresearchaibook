# Roadmap

> **Atualizado em 2026-08-06.** O que vem agora, em que ordem e por quê. **Cada item vira uma
> especificação** em `specs/NNN-nome/`, numa rodada própria, seguindo a metodologia
> [Maestro](https://github.com/GHDaru/maestro).

O destino está no [Mapa do handbook](livro/mapa-do-handbook.md) — 77 vagas declaradas. Este
documento é a **ordem de ataque**, e ela não é a ordem do sumário.

## Princípio de ordenação

Três critérios, nesta prioridade:

1. **O que a sala de aula precisa primeiro.** O handbook é o corpo de conhecimento de uma
   disciplina real; o que é ensinado no próximo semestre vem antes.
2. **O que destrava mais capítulos depois.** Programação Linear (PL) é pré-requisito de
   redes, de programação inteira e de metade dos módulos aplicados.
3. **O que prova a máquina.** Uma parte completa — com exercícios, vídeo e código — vale mais
   do que dez capítulos pela metade, porque só ela demonstra que o ciclo inteiro funciona.

---

## Rodada 001 — Fundação e sumário ✅

**Entregue em 2026-08-06.** Repositório refundado para PO; estudo do corpo de conhecimento;
mapa do handbook com as 77 vagas; aparato editorial (guia, bibliografia, videoteca, glossário,
Radar); motor religado.

## A cadência: uma rodada por capítulo

**Decisão do autor (2026-08-06): cada capítulo é uma rodada Maestro completa** —
`specify → clarify → plan → tasks → implement`, com sua pasta em `specs/NNN-nome/` e gate
humano no fim.

A razão é a mesma que faz o Maestro existir: o gate humano só é útil quando cabe na cabeça de
quem revisa. Uma Parte inteira num único gate vira carimbo. Um capítulo por rodada mantém a
especificação pequena o bastante para ser lida de verdade — e o custo é baixo, porque o
esqueleto de capítulo já está fixado no [Guia Editorial](livro/GUIA-EDITORIAL.md).

**Definition of Done de toda rodada de capítulo**, sem exceção:

- Objetivos de aprendizagem numerados, com **cada exercício rastreando a um deles**.
- Mínimo de **3 exercícios** com devolutiva que explica, e **1 vídeo** curado.
- A etapa correspondente do `po-zero`, com os números do capítulo **regeneráveis por script**.
- A seção **"quando não serve"** — obrigatória (constituição, Princípio II).
- Build verde, testes verdes, histórico atualizado, revisão em contexto fresco.

## Rodadas 002 a 010 — Parte II: Programação Linear 🚧

O coração do handbook e o que o autor aplica com os alunos. Uma rodada por capítulo, nesta
ordem:

| Rodada | Capítulo | Por que aqui |
|---|---|---|
| 002 ✅ | 07 — Formulação de modelos lineares | O capítulo mais praticado do livro. Sem ele, nada do resto tem sobre o que operar |
| 003 ✅ | 08 — A geometria da Programação Linear | Dá a intuição que o Simplex vai formalizar |
| 004 ✅ | 09 — O método Simplex | O algoritmo por dentro, com a implementação didática do `po-zero` |
| 006 ✅ | 10 — Casos especiais e degenerescência | **Capítulo próprio por decisão editorial** — nenhuma das duas obras-base trata em separado, e é onde o aluno descobre que o problema está no modelo |
| 007 ✅ | *(rodada de motor)* — Portão de fontes | Inserida pelo autor em 2026-08-12, fora da ordem prevista. Ver a nota de numeração abaixo |
| 008 🚧 | 11 — Simplex revisado e implementação eficiente | Por que o solver real não faz o que o quadro faz |
| 009 | 12 — Dualidade | **Logo após o Simplex**, como em Arenales e não como em Lachtermacher: a leitura econômica do preço-sombra é o que dá sentido ao algoritmo |
| 010 | 13 — Análise de sensibilidade e pós-otimização | A parte que o gestor de fato usa. **Recebe as regras de precificação**, remetidas do 11 (2026-08-12) — o capítulo 10 prometeu a continuação e ela chega aqui |
| 011 | 14 — Métodos de pontos interiores | A alternativa que domina os problemas grandes |
| 012 | 15 — Modelagem aplicada em PL | O repertório de padrões, fechando a Parte II |

> **Nota de numeração, 2026-08-12.** A rodada 007 estava reservada ao capítulo 11 e o autor
> inseriu no lugar dela uma rodada de motor; a Parte II deslocou uma unidade daqui para baixo.
> A regra que isso fixa: **a numeração é sequencial na pasta `specs/`, e este `ROADMAP` é ordem
> de ataque, não contrato.** Registrada no [ADR 0010](adr/0010-a-semantica-do-selo.md), anexo R2 —
> junto com R1, que classifica **rodada de motor como raia plena**, não leve, porque mexe no que
> barra publicação.

## Rodada 011 em diante — Parte I: Fundamentos

Escrita **depois** da PL, de propósito. Um capítulo de fundamentos escrito antes de existir
qualquer método concreto vira abstração; escrito depois, ele pode apontar para o que o leitor
já viu. Seis capítulos, seis rodadas.

Inclui a consolidação do `po-zero` como trilha completa.

## Depois: o primeiro módulo aplicado

O primeiro da Parte X, escolhido pelo autor em função da turma. É a rodada que **prova a
promessa evolutiva**: um módulo aplicado deve entrar sem tocar em nenhum capítulo existente.
Se tocar, a arquitetura está errada e o problema é de motor, não de conteúdo.

Candidatos naturais, por proximidade com a PL: cadeia de suprimentos e projeto de rede;
planejamento e programação da produção; gestão de estoques.

## Backlog priorizado

| Ordem | Item | Por quê |
|---|---|---|
| 1 | Parte III — Redes e Fluxos | Puxa diretamente da PL (fluxo de custo mínimo é PL com estrutura) |
| 2 | Parte IV — Programação Inteira | Onde mora a modelagem que a indústria usa |
| 3 | Parte V — Heurísticas e Metaheurísticas | Pedido explícito do autor, e **lacuna das duas obras-base** |
| 4 | Segundo e terceiro módulos aplicados | Consolidar a cadência de crescimento por adição |
| 5 | Parte VIII — Modelos probabilísticos | Filas e simulação; cobertura que os livros-texto dão e os cursos cortam |
| 6 | Parte VII — Otimização sob incerteza | **Lacuna das duas obras-base** |
| 7 | Parte XI — Fronteira | **Lacuna das duas obras-base**, mas só depois do núcleo firme: fronteira sem base é hype |
| 8 | Partes VI e IX | Não linear, decisão multicritério |
| 9 | Par em inglês do núcleo | Dívida declarada na constituição (Princípio VIII) |

> As três lacunas marcadas acima — metaheurísticas, incerteza e fronteira — são o que
> [a bibliografia](livro/bibliografia.md) mostrou que **nenhuma das duas obras-base cobre**.
> São a maior contribuição própria do handbook, e por isso não podem cair no fim da fila para
> sempre.

## Trabalho contínuo (não é rodada)

- **Radar científico** — cadência quinzenal. Artigo lido vira linha datada em
  `radar/RADAR.md`, com o veredito e o que ele muda. Linha que altera uma recomendação dispara
  revisão do capítulo afetado.
- **Janela trimestral de revisão** — reconferir vídeos (link morto é dívida do livro),
  reexecutar os experimentos do `po-zero` com as versões correntes de biblioteca e solver,
  atualizar as datas de captura.
- **Portão de URL externa — CONTINUA ABERTO, e subiu de prioridade.** Hoje a defesa contra
  endereço inventado é a disciplina de quem escreve, e disciplina não é mecanismo. Um portão que
  exija que toda URL de vídeo esteja na Videoteca com estado declarado fecharia parte do buraco.
  Nasceu do incidente da rodada 004 — **uma URL de vídeo inventada**.
  > **A rodada 007 NÃO fechou este item, e é importante não confundir os dois.** O portão de
  > fontes cobre **identificador de objeto digital (DOI)**: 12 das ~25 entradas da bibliografia.
  > URL comum, página institucional, curso gravado e identificador do arXiv seguem sem
  > mecanismo — e **o incidente que motivou a rodada 007 continuaria passando por ela**. Portão
  > que cria confiança maior do que sua cobertura é pior do que portão nenhum, então isto está
  > dito também na própria bibliografia e no cabeçalho do `verifica-fontes.mjs`.
- **Sessão de história** — pesquisa concentrada que alimenta as seções "De onde isto veio" das
  rodadas seguintes, em vez de pesquisar capítulo a capítulo. Primeira rodada feita em 2026-08-09
  ([estudo 002](estudos/002-historia-dos-metodos.md)); a próxima cobre as Partes VI a IX e a
  fronteira. A **fila de verificação** do estudo lista o que fecharia mais dívida por esforço.
- **Comparação entre regras de pivoteamento** — Dantzig, Bland, maior melhoria, *steepest edge*.
  É o que decidiria qual regra ensinar como padrão; hoje o capítulo 09 ensina a de Dantzig por ser
  a que a sala pratica, não por evidência comparativa.
- **Varredura sobre qualidade de formulação** — como se avalia se um modelo está bem escrito, e
  não se o solver está rápido. A impressão de que essa literatura é fina está declarada no
  capítulo 07 como impressão, não como resultado.
- **Gatilho por telemetria** — exercício com taxa de acerto muito baixa e volume relevante é
  sintoma de **texto mal escrito**, não de leitor fraco. Entra na fila de revisão.

## Decisões em aberto

1. **Prioridade dentro da Parte X.** Qual módulo aplicado vem primeiro depende da turma;
   decisão do autor.
2. **Ordem interna das Partes VI a IX.** Filas antes ou depois de programação dinâmica é
   discussão em aberto, e não foi testada com alunos.

## Decisões fechadas

| Data | Decisão | Onde |
|---|---|---|
| 2026-08-06 | Mapa do handbook aprovado pelo autor | [Mapa](livro/mapa-do-handbook.md) |
| 2026-08-06 | Livros-base mapeados: as duas obras **não cobrem** as Partes V, VII e XI | [Bibliografia](livro/bibliografia.md) · edição 0.2 |
| 2026-08-06 | **Uma rodada Maestro por capítulo** | Este documento |
| 2026-08-06 | Materiais de terceiros em repositório privado separado; histórico purgado | [ADR 0005](adr/0005-materiais-em-repositorio-privado.md) |
| 2026-08-09 | Rodadas 002 e 003 aprovadas e publicadas na `main` | [Histórico](livro/HISTORICO.md) · edição 0.6 |
| 2026-08-09 | Simplex ensinado pelo **quadro**; Fase I / *big-M* dentro do capítulo 09 | [Spec 004](specs/004-cap09-simplex/spec.md) · clarify |
| 2026-08-09 | Portão de consistência de ótimo **construído** — a dívida da edição 0.6 | `publicar/verifica-otimos.mjs` |
| 2026-08-09 | **Princípio XII — nenhum método cai do céu.** Constituição 1.1.0 | [ADR 0006](adr/0006-o-metodo-tem-historia.md) |
| 2026-08-09 | Dívida retroativa do Princípio XII quitada nos capítulos 07 e 08 | [Histórico](livro/HISTORICO.md) · edição 0.9 |
| 2026-08-09 | História pesquisada em **sessão concentrada**, não capítulo a capítulo | [Spec 005](specs/005-historia-dos-metodos/spec.md) |
| 2026-08-09 | Ilha interativa com **portão em navegador**; vídeos e fundamentos fechados | [Histórico](livro/HISTORICO.md) · edição 0.12 |
| 2026-08-09 | Degenerescência é do **modelo**; ciclagem é da **regra**. Tese da Parte II | [ADR 0007](adr/0007-fronteira-entre-modelo-e-metodo.md) — **pendente de ratificação do autor** |
