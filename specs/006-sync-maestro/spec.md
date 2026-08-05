# Spec 006 — Sincronia com o Maestro como portão

> **Raia:** plena · **Rodada:** 8 · **Branch:** `008-sync-maestro-e-baterias`

## Intenção

O Princípio VI declara o Maestro instalado neste repositório. Instalação por cópia manual
apodrece em silêncio — e a constituição chama isso de "o pior dos dois mundos". Esta
rodada torna a ressincronia uma linha de comando e a divergência um portão.

## Diagnóstico

O Maestro evoluiu (spec 017: retro executada) e duas skills mudaram sem que o livro
soubesse:

- **`anti-padroes`** ganhou o anti-padrão 13 — *"check que mede o proxy, não o fato"* — e
  os anti-padrões 14 e 15;
- **`dod-verificavel`** ganhou a **segunda lei**: *"um check que você nunca viu acusar não
  é um check — é uma esperança"*.

Não há skill nem plugin de instalação publicado: o Maestro é um repositório privado com
as skills em `skills/`. A instalação continua sendo cópia — o que muda é que ela deixa de
ser manual e passa a ser verificável.

## Escopo

1. **`scripts/sync-maestro.sh`** — sincroniza skills, comandos e agentes. O modo
   `--check` não escreve e sai com erro se houver divergência.
2. **Portão na CI**, condicionado a um segredo com acesso ao repositório privado do
   Maestro. Sem o segredo, o passo é pulado — melhor pular explicitamente do que falhar
   sempre e ensinar o time a ignorar a CI.
3. **Skills ressincronizadas** (as duas que divergiram).
4. **Constituição** aponta para o script.

## A lei nova aplicada nesta própria rodada

O portão de sincronia foi **provado falhando antes de ser usado**: rodado com as skills
divergentes, acusou os dois itens e saiu com código 1; só depois foi sincronizado e
passou.

E o anti-padrão 13 encontrou um bug de verdade. O check que eu usava para confirmar que o
widget do tutor estava na página era `grep -c "companion.js"` — que casa com o **texto**,
não com o artefato. Trocado por um que lê a **configuração injetada**, ele revelou que a
capacidade `exercicios` fora adicionada ao backend e **esquecida no espelho** do widget
(a duplicação registrada como dívida no ADR 0001).

Correção da causa, não do sintoma: além de regenerar o espelho a partir da fonte da
verdade, entrou **`publicar/verifica-espelho.mjs`** no início do build — ele compara
`COMPANION_CAPS` com `capabilities.py` e falha a construção se divergirem. Também provado
falhando: removida a capacidade do espelho de propósito, o portão acusou.

## Critérios de aceite

| # | Critério | Como verificar |
|---|---|---|
| CA-1 | O script sincroniza | `scripts/sync-maestro.sh` depois `--check` sai 0 |
| CA-2 | O `--check` acusa divergência real | provado: acusou as duas skills antes da sincronia |
| CA-3 | O espelho de capacidades não pode divergir | `npm run build` falha se divergir (provado quebrando) |
| CA-4 | Nada regride | build, portão e 24 testes verdes |

---

## Parte 2 — Baterias de exercícios (item 2 do pedido do autor)

### O que a releitura do BBIT ensinou

Um agente releu as séries de exercícios do BBIT com foco na **arquitetura**, não no
conteúdo. Os achados que viraram desenho:

1. **A letra da variante troca UMA variável por vez** — tipicamente a *implicitude* do
   alvo: declarado → implícito com distrator → múltiplo. Não é "mais um exercício igual".
2. **O aviso de erro nasce no gabarito de A e migra para o enunciado de B.** Diagnose,
   depois profilaxia.
3. **Uma espinha de cenários recorrentes** atravessa o curso: o mesmo caso volta com a
   ferramenta nova, e o produto de um exercício vira o insumo do seguinte.
4. **O gabarito não dá a resposta, encena o raciocínio** — critério de seleção, resposta
   canônica, outras respostas válidas, cláusula de tolerância ("mesma linha de raciocínio,
   não mesmas palavras"), erro provável **com o mecanismo**, princípio generalizável.
5. **Quando o exercício é de contexto próprio, o gabarito some** e o critério de
   autoverificação sobe para o enunciado.
6. **A lacuna:** o BBIT nunca transforma o catálogo de erros em exercício. Os pares
   errado/certo estão prontos e ninguém deu o passo.

### O que foi construído

**34 exercícios em 9 baterias**, quatro variantes por capítulo (dois no capstone):

| Variante | Tipo | O que muda |
|---|---|---|
| A | traduzir | relação declarada, com stub sintático |
| B | implícito | relação escondida, distrator plantado, e o aviso do erro de A |
| C | **achar o erro** | raciocínio pronto e defeituoso; o leitor diz que teste falha e por quê |
| D | contexto próprio | sem gabarito possível; o critério sobe para o enunciado |

A variante C é a lacuna do BBIT preenchida.

**A espinha de cenários** atravessa o livro: a Gráfica Belmonte (caps. 02, 03, 05, 06, 07,
08, 09), a clínica de fisioterapia (02, 06, 08, 09), o time de suporte (02, 07, 08), a loja
de bairro (03, 05, 06, 09) e o gestor com a equipe (05, 07). O encadeamento entre capítulos
é literal: a injeção produzida na bateria do cap. 08 é o objetivo da bateria do cap. 09.

**A rubrica é do servidor.** Critérios, `erro_provavel` e `resposta_guia` **nunca são
publicados** — o leitor não lê por quais critérios será avaliado. Verificado por varredura
no `docs/` gerado.

O tutor passa a receber o mecanismo do erro provável e a resposta-guia, com a instrução
explícita de que a guia serve para julgar **equivalência de raciocínio, não de palavras**.

### Critérios de aceite — parte 2

| # | Critério | Como verificar |
|---|---|---|
| CA-5 | Todo capítulo numerado tem bateria | 9 baterias, 34 exercícios publicados |
| CA-6 | A rubrica não vaza para o site | varredura por trecho de critério/erro/guia no `docs/` — nenhum |
| CA-7 | O registro é íntegro | portão valida ids únicos, campos obrigatórios, capacidade existente, 3–5 critérios |
| CA-8 | Bateria inexistente quebra o build | `bateria()` lança se a série estiver vazia |
