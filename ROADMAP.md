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

## Rodada 002 — Parte II: Programação Linear 🚧

**A próxima.** É o coração do handbook e o que o autor aplica com os alunos.

Escopo: os nove capítulos da Parte II — formulação, geometria, Simplex, casos especiais e
degenerescência, Simplex revisado, dualidade, análise de sensibilidade, pontos interiores e
modelagem aplicada.

Cada capítulo entrega, sem exceção:

- Objetivos de aprendizagem numerados, com exercícios que rastreiam a eles.
- Mínimo de **3 exercícios** com devolutiva explicativa e **1 vídeo** curado.
- A etapa correspondente do `po-zero`, com os números do capítulo regeneráveis por script.

**Decisão pendente do autor:** a Parte II sai em uma rodada única ou em duas
(formulação+geometria+Simplex, depois dualidade+sensibilidade+avançados)? A recomendação é
**duas** — uma parte inteira numa rodada só é grande demais para um gate humano útil.

## Rodada 003 — Parte I: Fundamentos

Escrita **depois** da PL, de propósito. Um capítulo de fundamentos escrito antes de existir
qualquer método concreto vira abstração; escrito depois, ele pode apontar para o que o leitor
já viu.

Inclui a instalação e o esqueleto do `po-zero`.

## Rodada 004 — Primeiro módulo aplicado

O primeiro da Parte X, escolhido pelo autor em função da turma. É a rodada que **prova a
promessa evolutiva**: um módulo aplicado deve entrar sem tocar em nenhum capítulo existente.
Se tocar, a arquitetura está errada e o problema é de motor, não de conteúdo.

Candidatos naturais, por proximidade com a PL: cadeia de suprimentos e projeto de rede;
planejamento e programação da produção; gestão de estoques.

## Rodada 005 — Parte III: Redes e Fluxos

Puxa diretamente da PL (fluxo de custo mínimo é PL com estrutura) e destrava boa parte dos
módulos aplicados.

## Backlog priorizado

| Ordem | Item | Por quê |
|---|---|---|
| 6 | Parte IV — Programação Inteira | Onde mora a modelagem que a indústria usa |
| 7 | Parte V — Heurísticas e Metaheurísticas | Pedido explícito do autor; módulo inteiro |
| 8 | Segundo e terceiro módulos aplicados | Consolidar a cadência de crescimento por adição |
| 9 | Parte VIII — Modelos probabilísticos | Filas e simulação; cobertura que os livros-texto dão e os cursos cortam |
| 10 | Parte XI — Fronteira | Só depois do núcleo firme: fronteira sem base é hype |
| 11 | Partes VI, VII, IX | Não linear, incerteza, decisão multicritério |
| 12 | Par em inglês do núcleo | Dívida declarada na constituição (Princípio VIII) |

## Trabalho contínuo (não é rodada)

- **Radar científico** — cadência quinzenal. Artigo lido vira linha datada em
  `radar/RADAR.md`, com o veredito e o que ele muda. Linha que altera uma recomendação dispara
  revisão do capítulo afetado.
- **Janela trimestral de revisão** — reconferir vídeos (link morto é dívida do livro),
  reexecutar os experimentos do `po-zero` com as versões correntes de biblioteca e solver,
  atualizar as datas de captura.
- **Gatilho por telemetria** — exercício com taxa de acerto muito baixa e volume relevante é
  sintoma de **texto mal escrito**, não de leitor fraco. Entra na fila de revisão.

## Decisões em aberto

1. **Mapeamento dos livros-base.** Assim que os dois livros didáticos de referência forem
   anexados, cada vaga do mapa ganha a correspondência capítulo-a-capítulo na
   [bibliografia](livro/bibliografia.md). Só metadado bibliográfico é versionado — conteúdo,
   não (constituição, Princípio X).
2. **Granularidade das rodadas de conteúdo.** Ver a decisão pendente da rodada 002.
3. **Prioridade dentro da Parte X.** Depende da turma; decisão do autor.
