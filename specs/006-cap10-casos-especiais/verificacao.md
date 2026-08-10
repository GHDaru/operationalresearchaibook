# Verificação — rodada 006

**Data:** 2026-08-09 · Saídas coladas, não transcritas. Este arquivo nasceu porque o
`guardiao-processo` apontou a sua ausência: **alegação sem evidência anexada viola o Princípio
XI**, e o plano alegava um hash sem lugar onde ele estivesse registrado.

## A mudança em artefato publicado, e o **alcance** da evidência

`po-zero/etapa-03-simplex/quadro.py` — publicado na `main` — ganhou o parâmetro `regra`. A
evidência de que isso não quebrou nada:

```
md5sum antes:   0d427a9fe3756e0c6de46f2ac93a16c8  po-zero/etapa-03-simplex/resultados.json
md5sum depois:  0d427a9fe3756e0c6de46f2ac93a16c8  po-zero/etapa-03-simplex/resultados.json
```

**O alcance desta evidência, dito com precisão, porque exagerá-lo seria o mesmo defeito que este
arquivo existe para corrigir:** o hash prova que **os três casos de `experimento.py` da etapa 03
produzem saída idêntica**. Não prova retrocompatibilidade geral de `quadro.py` — nenhum outro
chamador foi exercitado, porque não existe outro. É o tipo certo de evidência com alcance
limitado, e o limite está declarado.

## Etapa 04 — os cinco vereditos

```
custo da garantia · montadora            dantzig=2 bland=2 mesmo veredito=True mesmo valor=True
custo da garantia · vertice_degenerado   dantzig=2 bland=2 mesmo veredito=True mesmo valor=True
custo da garantia · multiplos_otimos     dantzig=1 bland=2 mesmo veredito=True mesmo valor=True
custo da garantia · sem_plano            dantzig=1 bland=3 mesmo veredito=True mesmo valor=True
1_vertice_degenerado     [dantzig] otimo                pivôs=  2 ponto=['8', '2'] · vértice DEGENERADO (básicas em zero: ['f3'])
2_multiplos_otimos       [dantzig] otimo                pivôs=  1 ponto=['0', '6'] · MAIS DE UM ÓTIMO (custo reduzido zero em ['x1'])
3_sem_teto               [dantzig] ilimitado            pivôs=  0 ponto=None
4_sem_plano              [dantzig] inviavel             pivôs=  1 ponto=None
5_giro_dantzig           [dantzig] limite_de_iteracoes  pivôs= 41 ponto=None · CICLO período 6 (base ['f1', 'f2', 'f3'] repetiu na iteração 6)
5_giro_bland             [bland  ] otimo                pivôs=  6 ponto=['1/25', '0', '1', '0']
```

**Reprodutibilidade:** duas execuções consecutivas produzem `resultados.json` idêntico byte a
byte (`9a6bd6f3…` nas duas).

**Conferência com o HiGHS**, por veredito:

```
1_vertice_degenerado     {'status': 'Optimal', 'ponto': [8.0, 2.0], 'valor': 1100.0}
2_multiplos_otimos       {'status': 'Optimal', 'ponto': [0.0, 6.0], 'valor': 1200.0}
3_sem_teto               {'status': 'Unbounded'}
4_sem_plano              {'status': 'Infeasible'}
5_giro                   {'status': 'Optimal', 'ponto': [0.04, 0.0, 1.0, 0.0], 'valor': 0.05}
```

O quinto merece nota: o solver de mercado resolve sem dificuldade a instância em que o Simplex
didático **gira para sempre** — e chega ao mesmo ponto que a regra de Bland, $(1/25, 0, 1, 0)$
com $z = 1/20 = 0{,}05$.

**Empates no teste da razão, no caso degenerado** — o sintoma que sobrevive à troca de regra:

```
[{'iteracao': 0, 'razoes': {'f1': '10', 'f2': '6', 'f3': '10'}},
 {'iteracao': 1, 'razoes': {'f1': '8', 'x2': '12', 'f3': '8'}}]
```

## A tese, medida

| Evidência | Valor |
|---|---|
| Ciclo com a regra de Dantzig | **sim** |
| Ciclo com a regra de Bland, **mesma instância** | **não** |
| Empates persistem no modelo degenerado, sob as duas regras | **sim** |

> O que é do modelo sobrevive à troca do método. O que some quando você troca o método era do
> método.

## Fontes abertas nesta rodada

Todas por `curl`, com código de resposta e tamanho registrados na sessão:

| Fonte | Resposta | Estado |
|---|---|---|
| Dantzig, Orden & Wolfe (1955), *Pacific Journal of Mathematics* — [PDF](https://msp.org/pjm/1955/5-2/pjm-v5-n2-p04-s.pdf) | `200`, 1.297.915 b | ✓ **lida** |
| Hall & McKinnon, arXiv math/0012242 | `200`, 178.418 b | ✓ **lida** |
| Beale (1955), Crossref | `200` | ✓ᵐ metadados |
| Bland (1977), Crossref | `200` | ✓ᵐ metadados |
| Gill et al. (1989), Crossref | `200` | ✓ᵐ metadados |
| Hall & McKinnon (2004), Crossref | `200` | ✓ᵐ metadados |
| Guerrero-García & Santos-Palomo (Hoffman) | `403` | ❌ não aberta |
| Gass & Vinjamuri (2004), cópia aberta | `404` | ❌ não aberta |

## O que **não** foi verificado

| Item | Estado | Por quê |
|---|---|---|
| A forma primal da instância aparecer literalmente em Beale (1955) | ⏳ | Editora recusa acesso automatizado; e o título do artigo fala em simplex **dual** |
| O enunciado exato da regra de Bland, e a prova de terminação | ⏳ | INFORMS `403`. O handbook **mede** a terminação, não a prova |
| Charnes (1952) → origem do *big-M* e o que propõe para degenerescência | ⏳ / ❌ | Artigo não aberto. Dívida herdada da rodada 004 |
| Prioridade Hoffman: 1951 ou 1953 | ⏳ | Divergência entre levantamentos, não resolvida |

## Parecer do guardião de processo

**PODE PROSSEGUIR COM RESSALVAS**, cinco bloqueios. Quatro eram defeitos reais e estão corrigidos
— o registro está no [plano](plan.md#o-que-o-guardião-barrou). O quinto **não é meu para
resolver**: o guardião observa que a tese editorial fixada no ADR 0007 e a alteração de capítulo
já publicado estão mais perto de "publicação" — gate do autor — do que de *clarify*, e que um ADR
não pode declarar inaplicável o gate do autor.

**Conduta:** o trabalho segue na branch, que é reversível; a tese e a alteração do capítulo 09 vão
ao autor como **itens explícitos de ratificação** no gate de merge. Nada foi publicado na `main`.

---

## Verificação final — depois de escrito o capítulo

### Build (7 portões)

```
✓ espelho de capacidades em sincronia (8 capacidades)
✓ referências de capítulo OK: 52 referências (0 compostas) apontam para capítulos do mapa; 7 para vaga ainda não publicada
✓ Grafo do livro: 22 nós, 47 arestas
✓ Livro gerado [pt]: 14 páginas + capa em docs/ (links internos OK)
✓ template verificado [pt]: 5 capítulos com C01/N02 + 9 páginas de aparato OK
✓ registro de exercícios OK: 27 exercícios em 4 baterias, rubrica não publicada
✓ consistência de ótimo OK: 23 modelo(s) resolvido(s) em aritmética exata
```

### Ilha interativa e testes do tutor

```
✓ ilha interativa operada em navegador: 15 verificações, 0 falhas
24 passed, 1 warning
```

### Reprodutibilidade das duas etapas

```
etapa-04  fb41eb6cdd730cbd545fa7712c7a4b3c  (idêntico em duas execuções)
etapa-03  0d427a9fe3756e0c6de46f2ac93a16c8  (inalterado desde a rodada 004)
```

### Portões provados quebrando

**1. Princípio XII** — renomeando a seção do capítulo 10 de `## De onde isto veio` para outro
título:

```
✗ verificação do template [pt]: 1 falha(s)
   10-casos-especiais: sem a seção "De onde isto veio" — Princípio XII (ou declare a dívida em SEM_ORIGEM_DECLARADO)
```

**2. Consistência de ótimo** — declarando ponto único no `cap10.exC`, que na verdade tem um
segmento de ótimos:

```
✗ consistência de ótimo: 1 falha(s)
   cap10.exC: 2 vértices atingem o ótimo ((2,3), (4,0)), mas a rubrica declara um ponto único
```

Este segundo caso merece nota: **o portão encontrou sozinho os dois vértices** — $(4,0)$ e
$(2,3)$ —, que são exatamente os que o enunciado do exercício pede ao leitor para descobrir. A
resposta do exercício está conferida por um caminho independente do que a escreveu.

Restaurados os dois, os portões voltam a verde.

## O que **não** foi verificado

| Item | Estado | Por quê |
|---|---|---|
| **Duração do vídeo do capítulo 10** | ❌ | A página não devolveu o campo em nenhuma tentativa — nem por requisição direta, nem por navegador. Título, endereço e autoria **foram** conferidos |
| Enunciado exato da regra de Bland e prova de terminação | ⏳ | Editora recusa acesso automatizado. O handbook **mede** a terminação |
| Forma primal da instância em Beale (1955) | ⏳ | Mesmo motivo, agravado pelo título do artigo falar em simplex **dual** |
| Prioridade de Hoffman: 1951 ou 1953 | ⏳ | Divergência entre levantamentos |
| Charnes (1952) → origem do *big-M* | ⏳ | Dívida herdada da rodada 004 |
| **Revisão em contexto fresco** | ⏳ | Próximo passo. Quem executa não verifica |
