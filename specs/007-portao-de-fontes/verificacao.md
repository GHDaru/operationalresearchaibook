# Verificação da rodada 007 — portão de fontes

**Data:** 2026-08-12 · Saída **colada**, não parafraseada (Princípio XI).

## T0 — o contrato do registro, verificado antes da decisão ser gravada

O especialista consultado não tinha egresso de rede e declarou o `doi.org/api/handles` como
conhecimento não verificado. Verificado aqui, antes de o ADR 0009 ser escrito:

```
$ curl -sS "https://doi.org/api/handles/10.1287/inte.20.4.43"
responseCode = 1 | handle = 10.1287/inte.20.4.43

$ curl -sS "https://doi.org/api/handles/10.1287/opre.99.9.9.99999"
responseCode = 100 | handle = 10.1287/opre.99.9.9.99999

$ curl -sS "https://doi.org/api/handles/10.99999/xyz"
responseCode = 100

$ curl -sS "https://api.crossref.org/prefixes/10.1287"
Institute for Operations Research and the Management Sciences (INFORMS)
```

A segunda linha é o que importa: **prefixo verdadeiro, sufixo inventado** — o modo típico de
fabricação — é negado pelo registro. A degradação prevista para o caso de o `handles` não servir
não foi necessária.

## A calibração do limiar — o experimento que substituiu a citação

```
$ node coleta-amostra.mjs
entradas com DOI declarado: 12
  ...
  curl: (22) The requested URL returned error: 429
  ✓ 10.1007/BF01589114  openalex
resolvidas: 12/12
```

> O `429` acima **não é ruído**: é o desenho de duas camadas se provando em campo. O Crossref
> recusou uma consulta e o OpenAlex atendeu.

### Primeira calibração — reprovou, e o defeito era meu

```
pior legítimo   0.022  (10.1007/bf01917108)
melhor impostor 0.496
janela          -0.473
✗ NÃO HÁ LIMIAR DEFENSÁVEL
```

Diagnóstico antes do fix: os "títulos declarados" eram **nomes de autor**. A alternância única do
*regex* casava `**DANTZIG, George B.**` porque o motor escolhe pela **posição** antes de escolher
pelo ramo.

### Segunda — com títulos certos, e ainda sem limiar

```
pior legítimo   0.517  (10.1145/990308.990310 — Spielman & Teng)
melhor impostor 0.560  (Origins of the simplex method × New Finite Pivoting Rules…)
janela          -0.043
✗ NÃO HÁ LIMIAR DEFENSÁVEL
```

O registro **corta o subtítulo** de Spielman & Teng; os dois impostores compartilham
*"simplex method"*. Nenhum número separa os dois casos.

### Terceira — critério novo, e aí sim

```
12 pares legítimos → todos 1.000
melhor impostor    → 0.560
janela             → 0.440
✓ limiar defensável: qualquer valor em (0.560, 1.000]
  sugerido (meio da janela): 0.78
```

**Alcance desta evidência, declarado:** o limiar está calibrado **nesta bibliografia, com 12
pares**. Não é constante universal. Entrada nova que reprove por título deve ser lida à mão
antes de qualquer ajuste do número — e ajustar o número para calar o portão é exatamente o que
o `calibra-limiar.mjs` existe para tornar visível.

## A primeira execução crua, antes de qualquer correção

Colada porque sem ela ninguém distingue *"o portão nasceu e a bibliografia estava certa"* de
*"a bibliografia foi ajustada até o portão calar"* (bloqueio B2 do guardião).

```
$ node atualiza-fontes.mjs
canários:
   ✓ 10.1287/inte.20.4.43 → sim
   ✓ 10.1002/nav.3800020406 → sim

11 entrada(s) com DOI declarado:
   ✓ 10.1287/inte.20.4.43 crossref
   ... (11 resolvidas)
✓ travamento gravado: 11 entrada(s) · 11 resolvidas · 0 sem metadados · 0 inexistentes

$ node verifica-fontes.mjs
✗ fontes: 3 falha(s)
   selo "✓ᵐ" é usado no arquivo e NÃO está declarado na legenda
   selo "❌" é usado no arquivo e NÃO está declarado na legenda
   contagem divergente: o arquivo tem 12 ligação(ões) doi.org e o parser leu 11 entrada(s) com DOI
```

**Três falhas, e uma delas era do próprio portão.** A contagem independente — o critério A2, que
o guardião chamou de circular na primeira versão e mandou tornar independente — apanhou o parser
no primeiro uso.

Causa raiz: **`\z` não existe em regex de JavaScript.** É *identity escape* para a letra `z`
literal, então o corpo da entrada terminava no primeiro `z` minúsculo. A entrada perdida era a de
Gill et al., cujo título contém "optimi**z**ation". Sem A2, o portão teria ficado verde ignorando
uma entrada.

As outras duas eram **defeitos reais da bibliografia**, exatamente o que a rodada foi buscar.

## Estado final

```
$ npm run build
✓ espelho de capacidades em sincronia (8 capacidades)
✓ fontes OK: 12 DOI(s) na bibliografia · 12 no travamento · 12 resolvido(s) · 0 sem metadados · 0 inexistente(s) — URL comum e arXiv seguem sem portão
✓ referências de capítulo OK: 52 referências (0 compostas) apontam para capítulos do mapa; 7 para vaga ainda não publicada — a aderência semântica é leitura humana
✓ Grafo do livro: 22 nós, 47 arestas
✓ Livro gerado [pt]: 14 páginas + capa em docs/ (links internos OK)
✓ template verificado [pt]: 5 capítulos com C01/N02 + 9 páginas de aparato OK
✓ registro de exercícios OK: 27 exercícios em 4 baterias, rubrica não publicada
✓ consistência de ótimo OK: 23 modelo(s) resolvido(s) em aritmética exata

$ SEM_PDF=1 npm run build
✓ (idem, verde)

$ cd chat-companion/backend && python -m pytest -q
24 passed, 1 warning in 2.41s
```

> **Correção factual.** Uma versão anterior rotulou `SEM_PDF=1 npm run build` como "o caminho do
> Vercel". **Não é.** O `vercel.json` constrói com `SEM_PDF=1 node build.mjs && SEM_PDF=1 node
> verifica-capitulos.mjs` — **pula `verifica-fontes` e os outros quatro portões**. O merge é
> conferido porque a integração contínua roda `npm run build`; a **publicação** não passa por
> portão nenhum. É defeito **pré-existente**, herdado pelos outros portões, e não regressão desta
> rodada — mas quem lê "portão do build" precisa saber. Entra no `ROADMAP`.

## Os testes destrutivos

Um portão sem teste de falha é um portão que **se presume** funcionar.

```
$ bash specs/007-portao-de-fontes/testes-destrutivos.sh
✓ T0  bibliografia e travamento como estão
✓ A5  DOI na bibliografia e fora do travamento
✓ A6  DOI que o registro nega
✓ A7  trabalho registrado ≠ trabalho declarado
✓ A8a título sem relação reprova
✓ A8b subtítulo cortado no registro passa
✓ A8c ano diverge do registro
✓ A9  selo fora da legenda
✓ A10a chave fora do contrato
✓ A10b texto acima de 300 caracteres
✓ A11 título não extraível é DEFEITO, não omissão
✓ A2  contagem bruta ≠ contagem do parser
✓ R1  o endereço do link é conferido, não só o rótulo
✓ R2  estado e conteúdo não podem divergir (null == null)
✓ R3  duplicata no travamento não passa em silêncio
✓ R4  estado vazio reprova
✓ R5  DOI malformado não é ignorado
✓ A3  o portão não tocou a rede
✓ A12 travamento idêntico a menos da data (83669ae6c1309137dbd46e55233631f2)
✓ D8  o gerador recusou rodar com CI=1
──────────────────────────────────────────
20 verificação(ões) OK · 0 falha(s)
```

### O que a revisão independente encontrou, e o que virou teste

A primeira revisão **reprovou o merge** com cinco achados. Todos confirmados por medição antes de
aceitos, e os cinco viraram correção **mais teste** — porque correção sem teste é promessa:

| Achado | O que era | Onde virou teste |
|---|---|---|
| Queda dos índices produzia build verde com zero verificação | O canário só exercitava `doi.org`. Com Crossref e OpenAlex fora, as 12 entradas viravam `registrado-sem-metadados`, com título e ano **nulos**, e nada abortava — era o bloqueio B3 do plano voltando pela única porta não coberta | canário agora exercita **os dois** caminhos; rebaixamento de qualquer tipo conta no limiar de degradação; `indeterminado` distinguido de `ausente` |
| O portão conferia o **rótulo** do DOI, não o endereço | Trocar só o `href` passava verde — e o identificador que o leitor usa é o do link | **R1** |
| A reconferência mensal dizia "confere" para DOI não consultado | Em `indeterminado` o gerador reempurra a entrada antiga, o diff dá vazio, e o workflow anuncia conferência sobre um título que o registro nunca devolveu | linha `RECONFERENCIA indeterminados=N` + passo que **falha** o workflow |
| `null == null` virava acordo | Travamento `resolvido` com título e ano nulos passava como "12 resolvidos", sem um aviso | **R2** |
| O denominador publicado estava errado | "12 de cerca de 25" — medido, são **36 linhas com selo**, 31 obras distintas. Cobertura real **39%**, não 48% | contagem com o comando, na spec e na bibliografia |

Mais três, sem bloqueio: duplicata no travamento (**R3**), `estado` vazio (**R4**) e `DOI [`
malformado tratado como ausência (**R5**).

**A3 merece nota de método, e uma ressalva.** O critério original dizia "rodar com a rede indisponível", que não
é reproduzível em integração contínua nem aqui. O guardião mandou trocar por algo mais forte, e
o teste hoje **prova a ausência da dependência**: substitui `fetch`, `http.get`, `https.request`
e toda a família de `child_process` por funções que abortam o processo, e então importa o portão.

**A ressalva, apontada pela revisão:** *import* nomeado de módulo nativo em ESM **não enxerga** a
mutação posterior de `module.exports`, e `net`, `dns`, `http2` e `undici` não são cobertos. Hoje o
fato vale — o portão importa apenas `node:fs`, `node:path` e `node:url` — mas **o teste não
pegaria a regressão que existe para pegar**. Fica declarado como o que é: verificação parcial. A
prova forte seria estática, sobre a árvore de *imports*, e está no `ROADMAP`.

## Rastreamento dos critérios de aceite

| # | | Estado |
|---|---|---|
| A1 | M | ✅ encadeado antes de `build.mjs`; `SEM_PDF=1` verde |
| A2 | M | ✅ e **pegou defeito real no primeiro uso** |
| A3 | M | ✅ ausência de rede provada por instrumentação |
| A4 | H | ✅ saída colada acima |
| A5–A12 | M | ✅ os oito testes destrutivos |
| A13 | M | ✅ nenhuma credencial; o portão roda sem chave |
| A14 | M | ✅ 24 testes verdes |
| A15 | M | ✅ **CI** no glossário e no mapa de siglas do motor |
| A16 | H | ✅ edição 0.14, **incluindo a dívida de URL** |
| A17 | H | ✅ numeração deslocada, `007 🚧` desmarcado, item de URL marcado como aberto |
| A18 | H | ⏳ **revisão em contexto fresco — pendente** |
| A19 | M | ✅ este arquivo |
| A20 | M | ✅ `reconfere-fontes.yml`, mensal, abre issue ao divergir |

## O que esta rodada NÃO prova

Dito aqui porque um `verificacao.md` que só lista verdes é propaganda.

1. **Cobertura: 12 de ~25 entradas.** Mais da metade da bibliografia continua sem portão.
2. **O incidente que motivou a rodada continuaria passando.** Era uma **URL de vídeo**, e URL
   comum está fora de escopo.
3. **O `✓` continua não verificável por máquina, para sempre e por desenho.** Nenhum portão pode
   atestar que um humano leu. A defesa é revisão humana e o *diff* (ADR 0010).
4. **A reconferência mensal ainda não rodou** — o workflow existe e nunca disparou. A defesa
   contra auto-atestação está **instalada**, não **exercida**.
