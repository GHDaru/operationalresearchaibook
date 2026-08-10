# Verificação — rodada 004

**Data:** 2026-08-09 · Saídas coladas, não transcritas.

## Build (7 portões)

```
> node verifica-espelho.mjs && node verifica-referencias.mjs && node build.mjs && node verifica-capitulos.mjs && node verifica-exercicios.mjs && node verifica-otimos.mjs

✓ espelho de capacidades em sincronia (7 capacidades)
✓ referências de capítulo OK: 22 referências (0 compostas) apontam para capítulos do mapa; 6 para vaga ainda não publicada — a aderência semântica é leitura humana
✓ Grafo do livro: 18 nós, 32 arestas
✓ Livro gerado [pt]: 13 páginas + capa em docs/ (links internos OK)
✓ template verificado [pt]: 4 capítulos com C01/N02 + 9 páginas de aparato OK
✓ registro de exercícios OK: 22 exercícios em 3 baterias, rubrica não publicada
✓ consistência de ótimo OK: 19 modelo(s) resolvido(s) em aritmética exata
```

## Testes do tutor

```
24 passed, 1 warning in 0.62s
```

## Experimento — `po-zero/etapa-03-simplex`

```
montadora: otimo · 2 pivô(s) · ponto ['8', '2'] · z = 1100 · concorda com HiGHS: True
montadora_com_compromisso: otimo · 3 pivô(s) · ponto ['2', '5'] · z = 950 · concorda com HiGHS: True
compromisso_impossivel: inviavel · 1 pivô(s) · ponto None · z = None · concorda com HiGHS: True
bases a enumerar com 20 variáveis e 20 restrições: 137.846.528.820
uma unidade a mais de CPUs: R$ 50.00
uma unidade a mais de pentes de memória de 16 GB: R$ 50.00
pior caso (Klee–Minty), pivôs: n=2: 3, n=3: 7, n=4: 15, n=5: 31, n=6: 63, n=7: 127 — todos iguais a 2^n-1: True
```

**Reprodutibilidade:** duas execuções consecutivas produzem `resultados.json` idêntico byte a
byte (`md5sum` `0d427a9f…` nas duas).

**Concordância com o solver:** os três casos batem **por veredito**, não só por ponto. O caso
inviável é o que dá valor aos outros dois.

## O portão novo, provado quebrando

Um portão que nunca reprovou não provou nada. Três cenários, todos executados:

### 1. O defeito histórico do `cap07.exC`, reintroduzido

Alterando o lucro do perfil B de 200 de volta para 300 — o valor que a edição 0.6 corrigiu à
mão:

```
✗ consistência de ótimo: 1 falha(s)
   cap07.exC [modelo do analista]: rubrica declara ótimo 96000, mas o ótimo do modelo é 103500
```

O portão **reencontra sozinho** o número que a revisão humana levou uma leitura inteira para
achar: 103.500, no vértice (137,5; 125).

### 2. Cobertura — exercício que afirma ótimo sem modelo declarado

Removendo o campo `modelo` do `cap08.exF`:

```
   cap08.exF: a rubrica afirma um ótimo e não há campo "modelo" para conferi-lo — declare o modelo ou justifique em SEM_MODELO_DECLARADO
```

Sem esta metade, bastaria omitir o campo para o exercício voltar exatamente ao estado em que o
defeito nasceu.

### 3. Ótimo finito declarado em região ilimitada

Invertendo o sentido do `cap08.exC` (minimização com pisos `≥`, região ilimitada para cima)
para maximização:

```
   cap08.exC: o objetivo é ilimitado na região, mas a rubrica declara ótimo finito
```

Restaurado o registro, o portão volta a verde: `✓ 19 modelo(s) resolvido(s)`.

## O que **não** foi verificado

Dito aqui porque omitir seria o defeito que este arquivo existe para evitar.

| Item | Estado | Por quê |
|---|---|---|
| **Autoria e duração do vídeo** | ❌ não conferidas | O ambiente não abre o YouTube (`403` do proxy de egresso) |
| **Atribuição da série do vídeo** | ❌ não confirmada na fonte | Aparece no resultado de busca; a fonte não é alcançável. É um grau a mais de dúvida que os vídeos dos capítulos 07 e 08 |
| **Fundamentos científicos** | ❌ lacuna declarada | arXiv, Crossref, OpenAlex e sites de editoras respondem `403` |
| **A ilha interativa do capítulo 08 em navegador** | ❌ segue sem verificação | Pendência herdada da rodada 003 |
| **Aderência semântica das referências de capítulo** | ⚠️ leitura humana | O portão confere que o número existe no mapa, não que aponta para o assunto certo |
| **Revisão em contexto fresco** | ⏳ pendente | Princípio Maestro: quem executa não verifica |

## Incidente registrado

O rascunho do capítulo trazia um **endereço de vídeo do YouTube inventado** — identificador
plausível, formato correto, apontando para nada verificado. Foi detectado ao testar se o
ambiente alcançava a fonte, e substituído por um endereço localizado em busca real.

A detecção foi **acidental**: não existe portão para URL externa. Está no
[plano](plan.md#o-que-quase-escapou) e virou item no ROADMAP.

---

## Adendo — o portão do Princípio XII

Acrescentado depois da emenda constitucional 1.1.0, ainda nesta rodada.

### Build, depois da emenda

```
✓ espelho de capacidades em sincronia (7 capacidades)
✓ referências de capítulo OK: 24 referências (0 compostas) apontam para capítulos do mapa; 6 para vaga ainda não publicada — a aderência semântica é leitura humana
✓ Grafo do livro: 19 nós, 33 arestas
✓ Livro gerado [pt]: 13 páginas + capa em docs/ (links internos OK)
✓ template verificado [pt]: 4 capítulos com C01/N02 + 9 páginas de aparato OK
✓ registro de exercícios OK: 22 exercícios em 3 baterias, rubrica não publicada
✓ consistência de ótimo OK: 19 modelo(s) resolvido(s) em aritmética exata
```

```
24 passed, 1 warning in 1.61s
```

### Provado quebrando

Renomeando a seção do capítulo 09 de `## De onde isto veio` para `## Um pouco de contexto`:

```
✗ verificação do template [pt]: 1 falha(s)
   09-simplex: sem a seção "De onde isto veio" — Princípio XII (ou declare a dívida em SEM_ORIGEM_DECLARADO)
```

Restaurado o título, o portão volta a verde.

### Um achado do próprio portão

Na primeira execução ele reprovou a **introdução** (`00-introducao`), que não é capítulo de
método e para a qual o Princípio XII não se aplica. Em vez de jogá-la na lista de dívida — o que
teria feito o build passar e mentido sobre o escopo —, o portão passou a ter **duas listas com
significados distintos**: `NAO_E_CAPITULO_DE_METODO` (não se aplica) e `SEM_ORIGEM_DECLARADO`
(dívida de verdade, hoje com os capítulos 07 e 08).

A distinção importa porque uma lista única esconderia, sob o mesmo nome, "não devia ter" e
"devia ter e não tem".
