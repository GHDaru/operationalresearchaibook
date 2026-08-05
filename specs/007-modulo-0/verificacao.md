# Verificação — rodada 9 (Módulo 0)

> **Prove, não declare.** Este arquivo existe porque a primeira versão do fechamento
> afirmava que os portões novos tinham sido provados, sem anexar a prova. A afirmação era
> verdadeira e a evidência não existia — que é exatamente a diferença que a segunda lei da
> DoD trata: *um check que você nunca viu acusar não é um check, é uma esperança*.

## Estado final — os cinco portões

```
✓ espelho de capacidades em sincronia (15 capacidades)
✓ referências de capítulo OK: 110 referências (5 compostas) apontam para capítulos
  existentes — a aderência semântica é leitura humana
✓ Grafo do livro: 15 nós, 35 arestas
✓ Livro gerado [pt]: 20 páginas + capa em docs/ (links internos OK)
✓ template verificado [pt]: 15 capítulos com C01/N02 + 5 páginas de aparato OK
✓ registro de exercícios OK: 50 exercícios em 13 baterias, rubrica não publicada
  24 passed
```

## `verifica-exercicios.mjs` — dez casos, cada um quebrado de propósito

Registro restaurado após cada quebra.

| Quebra aplicada | O que o portão disse |
|---|---|
| `capacidade: "inexistente"` | `cap01.exA: capacidade "inexistente" não existe em capabilities.py` |
| `capacidade: "injecoes"` no cap. 1 | `cap01.exA: capacidade "injecoes" só libera no cap. 12, mas o exercício é do cap. 1` |
| critérios cortados para 2 | `cap01.exA: 2 critério(s) de aceite — o contrato é de 3 a 5` |
| `resposta_guia` removida da variante A | `cap01.exA: variante A sem resposta_guia` |
| exercício `cap99.exA` acrescentado | `série "cap99" tem exercício mas nenhum capítulo a monta (data-bateria ausente)` |
| exercício duplicado | `cap01.exA: id duplicado` |
| `capitulo: 7` num id `cap01.*` | `cap01.exA: capítulo 7 não bate com o id` |
| `resposta_guia` colada em `docs/*.html` | `rubrica vazou em docs/01-sistema-e-restricao.html: cap01.exA (resposta_guia)` |
| `data-bateria` removido do cap. 07 | `07-pre-requisito: capítulo sem bateria — Princípio I exige prática com devolutiva` |
| cópia do backend editada à mão | `o registro empacotado no backend divergiu de livro/exercicios.json — rode build_corpus.py` |

### O falso-negativo que a revisão em contexto fresco encontrou

A primeira versão comparava o texto **cru** do registro com o HTML **escapado** da página:
`"de política"` no JSON vira `&quot;de política&quot;` na página, e o `includes()` não
casava. **18% dos campos da rubrica** têm aspas nos primeiros caracteres — para todos eles,
um vazamento real passaria com o portão imprimindo *"rubrica não publicada"*.

Corrigido normalizando os dois lados (desescapar entidades, reduzir a letras e dígitos).
Provado com o caso exato que passava antes:

```
exercício: cap03.exC
trecho   : Falha desde o passo 1: "capital de giro" é efeito, não lugar. A restri…
✗ rubrica vazou em docs/07-pre-requisito.html: cap03.exC (resposta_guia)
```

### Calibração da agulha (medida, não arbitrada)

O comprimento do trecho procurado foi escolhido contra o corpus publicado, não por gosto:

```
306 campos de rubrica, 44 arquivos publicados

 N  | sob vigilância | falsos positivos
 24 |    306/306     | 5
 40 |    302/306     | 0
 60 |    270/306     | 0
```

Com 24 caracteres alfanuméricos o portão acusava 5 vezes sem vazamento algum: o
`erro_provavel` de um exercício costuma abrir com a mesma frase que o capítulo publica de
propósito em "Erros comuns" — por exemplo, `cap01.exA` contra
`01-sistema-e-restricao.md:108`. Com 40, zero falsos positivos e 302 dos 306 campos
cobertos; os 4 mais curtos entram inteiros, e nenhum deles colide. **Nenhum campo fica sem
vigilância.**

## `verifica-referencias.mjs` — o portão que a rodada não tinha

Nasceu de um erro real, não de hipótese. A renumeração remapeou os números com uma
substituição ancorada na palavra-chave (`capítulo NN`), então o **segundo número de toda
referência composta** nunca foi visto. Quatro erros chegaram a conteúdo publicado e foram
achados pela revisão em contexto fresco, não pelos portões.

Prova: os quatro defeitos originais foram restaurados no repositório e o portão acusou os
cinco (o quarto vale por dois — a rubrica do capstone tinha duas referências quebradas):

```
✗ referências de capítulo: 5 falha(s)
   00-introducao.md:68: "capítulos 06–05" — intervalo/par em ordem decrescente
   bibliografia.md:13: "capítulos 10 e 08" — intervalo/par em ordem decrescente
   bibliografia.md:24: "capítulos 06 a 05" — intervalo/par em ordem decrescente
   exercicios.json:900: "caps. 06 e 06" — o par cita o mesmo capítulo duas vezes
                        (sintoma clássico de remapeamento parcial)
   exercicios.json:901: "caps. 08 e 08" — o par cita o mesmo capítulo duas vezes
```

E o ramo que os quatro não exercitavam, provado à parte:

```
   glossario.md:53: "cap. 22" — capítulo 22 não existe no sumário
```

### O que este portão NÃO faz

Ele verifica que o número **existe**, que o intervalo **sobe** e que o par não **repete**.
Ele não verifica se a referência aponta para o capítulo semanticamente certo — isso
continua sendo leitura humana. O portão imprime essa ressalva na própria saída para não
ser lido como mais do que é. Foi um critério de aceite que se apresentou como cobertura e
media um proxy que deixou os quatro erros passarem; a correção não é só o portão, é o
portão dizendo o que não cobre.

## Critérios de aceite da spec

| # | Critério | Evidência |
|---|---|---|
| CA-1 | O livro define restrição | 47 ocorrências do conceito nos caps. 01–02, com fonte citada (*A Meta*, 1984; Dettmer, 2007) |
| CA-2 | Os cinco passos, um a um | identificar/explorar/subordinar/elevar/inércia, cada um com o erro típico, no cap. 03 |
| CA-3 | As três perguntas mapeiam | tabela pergunta→ferramenta→módulo em `04-tres-perguntas.md:77-79` |
| CA-4 | Nenhuma referência cruzada quebrou | **falhou na primeira tentativa** — 4 erros publicados, achados pela revisão. Corrigidos; hoje `verifica-referencias.mjs` cobre a classe inteira (110 referências) |
| CA-5 | Os exercícios seguiram | 50 exercícios em 13 baterias (34 remapeados + 16 novos), ids alinhados |
| CA-6 | O gating acompanha | `verifica-espelho.mjs`: 15 capacidades em sincronia |
| CA-7 | Nada regride | os cinco portões + 24 testes, verdes |

## Correções vindas da revisão em contexto fresco

Achados aceitos e corrigidos nesta rodada: referências quebradas na introdução,
bibliografia e rubrica do capstone; nota de época no `HISTORICO`; `A Meta` e *Não é Sorte*
com ponteiros de capítulo corretos na bibliografia; contradição entre glossário e capítulo
na definição de gargalo (*igual ou menor* que a demanda); atribuição da frase "uma hora
perdida…" ao termo original (**gargalo**, não restrição) com a generalização sinalizada;
fonte para "diga-me como você me mede"; ganho, inventário e despesa operacional definidos
no corpo e no glossário; `Processos de Raciocínio` no glossário; rubrica de `cap01.exC`
passando a aceitar a leitura de política que o próprio capítulo planta; `cap02.exC`
passando a **exigir** a explicação da restrição a 71% em vez de mandar aceitá-la; ADR 0004
com as alternativas que a reescrita do programa de auditoria havia apagado.

Fica para o autor (é julgamento editorial dele, não meu): a espinha de cenários — os
capítulos 01–03 criaram uma gráfica que não é a **Gráfica Belmonte** dos capítulos 10–13, e
o mesmo time de suporte aparece com "módulo fiscal" e "módulo de faturamento".
