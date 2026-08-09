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
| 004 | 09 — O método Simplex | O algoritmo por dentro, com a implementação didática do `po-zero` |
| 005 | 10 — Casos especiais e degenerescência | **Capítulo próprio por decisão editorial** — nenhuma das duas obras-base trata em separado, e é onde o aluno descobre que o problema está no modelo |
| 006 | 11 — Simplex revisado e implementação eficiente | Por que o solver real não faz o que o quadro faz |
| 007 | 12 — Dualidade | **Logo após o Simplex**, como em Arenales e não como em Lachtermacher: a leitura econômica do preço-sombra é o que dá sentido ao algoritmo |
| 008 | 13 — Análise de sensibilidade e pós-otimização | A parte que o gestor de fato usa |
| 009 | 14 — Métodos de pontos interiores | A alternativa que domina os problemas grandes |
| 010 | 15 — Modelagem aplicada em PL | O repertório de padrões, fechando a Parte II |

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
- **Portão de consistência de exercício** — verificar que todo exercício cujo enunciado afirme
  uma solução ótima seja consistente com o modelo que ele apresenta. É o portão que teria pego
  sozinho o defeito que a revisão da edição 0.6 encontrou à mão.
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
