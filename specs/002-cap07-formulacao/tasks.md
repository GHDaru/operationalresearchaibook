# Tasks 002 — Capítulo 07: Formulação de modelos lineares

**Especificação:** [`spec.md`](spec.md) · **Plano:** [`plan.md`](plan.md) · **Data:** 2026-08-06

## Bloco 1 — O experimento primeiro

- [x] T1.1 Instância `instancias/moveis.json` **com ficha**: origem, licença e limitações.
- [x] T1.2 `modelo.py` com as duas formulações (margem e receita) sobre as mesmas restrições.
- [x] T1.3 `experimento.py` gerando `resultados.json` com versões de Python, biblioteca e solver.
- [x] T1.4 Verificar determinismo: rodar duas vezes e comparar o hash do arquivo.
- [x] T1.5 `README.md` da etapa, com o contrato e o que ela deliberadamente não faz.

## Bloco 2 — Objetivos e exercícios (Backward Design)

- [x] T2.1 Quatro objetivos numerados, com verbos de Bloom.
- [x] T2.2 `cap07.exA` — reconhecer variável, parâmetro e consequência (O1).
- [x] T2.3 `cap07.exB` — formular com conferência de unidades (O2).
- [x] T2.4 `cap07.exC` — diagnosticar modelo que rodou e devolveu ótimo (O3).
- [x] T2.5 `cap07.exD` — o próprio problema do leitor, sem resposta-guia (O4).

## Bloco 3 — O capítulo

- [x] T3.1 `livro/capitulos/07-formulacao.md` no esqueleto do Guia Editorial.
- [x] T3.2 Abertura pelo erro, com o custo medido.
- [x] T3.3 Seção "quando não serve", com destino declarado para cada limite.
- [x] T3.4 Bateria montada (`data-bateria="cap07"`).
- [x] T3.5 Leitura executiva e verificação final ligada aos objetivos.

## Bloco 4 — Motor e registro

- [x] T4.1 Capacidade `formulacao` nos dois lados do espelho (backend e motor).
- [x] T4.2 Sumário com a Parte II e os marcadores de vaga declarada.
- [x] T4.3 `cartaoEnt` aceitando item sem arquivo + estilo `.ent-card-vaga`.
- [x] T4.4 **Portão novo:** `objetivo` obrigatório e verificado contra o capítulo.
- [x] T4.5 Videoteca com a dívida do vídeo dita por extenso.
- [x] T4.6 Histórico: edição 0.3, com as dívidas e o estado das anteriores.
- [x] T4.7 Corpus do tutor regenerado.

## Bloco 5 — Verificação

- [x] T5.1 `cd publicar && npm run build` verde.
- [x] T5.2 `python -m pytest -q` verde.
- [x] T5.3 Determinismo do experimento comprovado.
- [x] T5.4 Portão novo provado quebrando de propósito.
- [x] T5.5 Conferência número a número do capítulo contra `resultados.json`.
- [ ] T5.6 **Revisão por agente em contexto fresco** — gate humano, cabe ao autor acionar.
- [ ] T5.7 **Aprovação do autor** e escolha do vídeo.

## Dívidas que esta rodada abre

| Dívida | Fecha quando |
|---|---|
| Vídeo do capítulo sem autoria e duração conferidas | O autor indicar o vídeo do canal parceiro |
| Sem artigos científicos na seção de fundamentos | A varredura entrar pela fila do Radar |
