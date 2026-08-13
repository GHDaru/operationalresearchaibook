# ADR 0015 — O longrun inclui o merge, até a v0 fechar

**Data:** 2026-08-13 · **Estado:** **decidida pelo autor**, em instrução direta · **Emenda:**
constituição 1.1.0 → **2.0.0** (MAJOR)

## Por que MAJOR, e não MINOR

A primeira redação desta ADR classificou a emenda como MINOR, argumentando que ela **acrescenta**
uma exceção com prazo em vez de remover um gate. O comitê discordou, e tem razão: a própria
constituição define **MAJOR como "remoção ou redefinição"**, e tirar o merge da lista de gates
**inegociáveis** — ainda que temporariamente — é redefinir a cláusula, não expandi-la.

Fica registrado porque a diferença não é cosmética: quem lê "1.2.0" entende continuidade, e quem
lê "2.0.0" vai conferir o que mudou. Numa emenda que muda **quem publica**, a segunda leitura é a
correta.

## Contexto

A constituição declara, na seção Governança: *"o autor aprova a especificação, o plano
(Constitution Check), o merge e qualquer publicação. Nenhum deles é delegável a agente."*

A skill [`longrun`](../.claude/skills/longrun/SKILL.md) nasceu na mesma sessão delegando o
**julgamento** ao agente, e deixou o merge de fora com esta justificativa escrita: *"é o único ato
não reversível por branch — ele publica —, e a constituição o declara não delegável. O agente não
emenda a constituição por conta própria."*

A skill fechava esse ponto assim: *"se o autor disser uma vez que longrun inclui o merge, esta
linha muda e a constituição é emendada por decisão dele — com ADR."* **O autor disse.**

## Decisão

**Enquanto a v0 não estiver fechada, o merge na `main` entra na delegação do longrun.**

O agente merge e publica sem esperar aprovação, dentro do rito da skill: lote verde nos portões,
revisão em contexto fresco feita e endereçada, decisões de médio ou alto impacto passadas pelo
comitê e registradas em ADR.

**A delegação expira sozinha.** No instante em que a v0 for declarada completa, esta linha volta
ao texto original da constituição e o merge retorna a ser gate humano. **Não é preciso pedir para
revogar** — é preciso pedir para estender.

### O que NÃO muda junto, e é a metade que importa

Esta emenda expande **um** gate. As demais travas do longrun continuam valendo, e valem
**exatamente porque** o merge deixou de esperar:

| Continua valendo | Por quê, agora que publicar é automático |
|---|---|
| Build ou teste vermelho **nunca** vira verde por ajuste | Era a rede de proteção contra a pressa; virou a única |
| **Quem executa não verifica** — revisão em contexto fresco antes de mergear | Sem o gate humano, é o último olho independente antes de publicar |
| Direito autoral e dado pessoal | Não são reversíveis por *branch*: a publicação é o dano |
| Fonte não confirmada não sustenta afirmação | Delegação não cria evidência |
| Comitê de três lentes + ADR em decisão de médio impacto | É o que substitui a conversa que deixou de acontecer |

### O que torna a expansão aceitável

Duas coisas, e nenhuma é confiança:

1. **Reversibilidade real.** `git revert` desfaz um merge, e o site republica a partir da `main`.
   O custo de um merge errado é uma rodada, não um dano permanente.
2. **A revisão em contexto fresco já reprovou uma vez** e mudou o resultado — o lote 1 foi
   reprovado por costura e corrigido antes de publicar. O mecanismo que substitui o gate humano
   **tem histórico de funcionar**, e é isso que autoriza contar com ele.

## Alternativas avaliadas

**Manter o merge com o autor.** Foi a posição do agente até esta instrução, e a razão continua
válida em regime normal: publicar é o único ato irreversível por *branch*. **Descartada pelo
autor**, com o argumento de que a v0 é fase de construção e o custo de esperar excede o risco de
reverter.

**Delegar o merge para sempre.** Não foi pedido, e o agente não estenderia por conta própria: a
justificativa da delegação é a fase, não o mecanismo. Depois da v0 o livro tem leitores, e o custo
de um merge errado deixa de ser uma rodada.

**Delegar com auto-revert por CI vermelho.** Descartada por complexidade sem ganho: o build já é
pré-condição do merge, e o autor pediu explicitamente para **não evoluir a infraestrutura** nesta
fase.

## Consequências

**Boas.** O longrun deixa de ter um ponto de parada obrigatório por rodada. O livro publica na
cadência em que é escrito, e o autor lê o resultado em vez de autorizar o processo.

**Ruins, e declaradas.** O autor deixa de ver o lote antes do leitor. Um defeito que a revisão em
contexto fresco não pegar chega publicado — e este repositório já produziu quatro defeitos dessa
natureza ("o corpo afirma o que a tabela nega"), três deles encontrados **depois** de publicados.
O antídoto é o portão de procedência, que cobre a forma grosseira e **não** cobre o caso completo,
como está declarado no próprio arquivo dele.

**O sinal que faria esta decisão ser revista:** dois merges seguidos que precisem de correção por
defeito que a revisão em contexto fresco deveria ter pego. Aí o problema não é o gate — é a
revisão, e ela é que precisa mudar.
