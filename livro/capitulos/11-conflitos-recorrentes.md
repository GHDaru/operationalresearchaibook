# 11 — Conflitos Recorrentes

> **Conteúdo revisado em 2026-08** · edição inaugural · [histórico](../HISTORICO.md)
>
> Capítulo em primeira versão — a ser aprofundado com o material do autor.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve conseguir:

1. **Identificar** um problema recorrente pelo padrão de oscilação entre dois comportamentos;
2. **Construir** o diagrama de loop, com as duas cadeias de causa e efeito e as duas violações;
3. **Explicar** por que a oscilação se sustenta sozinha, sem culpados;
4. **Distinguir** um conflito recorrente de um dilema pontual (capítulo 10).

## O problema

Existe uma classe de problema que não se resolve: ele volta. A empresa centraliza decisões, sofre com a lentidão, descentraliza; perde o controle, centraliza de novo. O gestor se envolve na operação, a equipe não desenvolve autonomia, ele se afasta; a qualidade cai, ele volta a se envolver.

O padrão é sempre o mesmo: **oscilação entre dois comportamentos, cada um adotado como correção do problema causado pelo outro**. E, como cada movimento parece racional no momento em que é feito, ninguém consegue apontar onde está o erro.

Não está em ninguém. Está na estrutura.

## O conceito

O diagrama que representa esse padrão tem quatro peças e um formato de loop fechado:

```
    ┌──→ violação do objetivo (1) ──┐
    │                               ↓
comportamento X                comportamento Y
    ↑                               │
    └── violação do objetivo (2) ←──┘
```

Lê-se assim:

1. Dois **comportamentos mutuamente exclusivos** (X e Y): não é possível fazer os dois ao mesmo tempo.
2. De cada comportamento sobe uma **cadeia de causa e efeito** — "se… então…", como no capítulo 09 — até uma **violação de objetivo**: um efeito negativo forte o bastante para gerar pressão de mudança.
3. Cada violação **empurra para o comportamento oposto**, fechando o loop.

O loop é autossustentável: nenhuma força externa é necessária para mantê-lo girando. É por isso que trocar as pessoas não resolve — a nova pessoa entra na mesma estrutura e passa a oscilar do mesmo jeito.

## Um exemplo

**X:** o gestor participa das decisões operacionais do time.
→ Se o gestor participa de cada decisão, então as decisões esperam por ele.
→ Se as decisões esperam por ele, então o time entrega mais devagar.
→ **Violação 1:** o time não cumpre os prazos combinados.

Essa violação empurra para **Y**.

**Y:** o gestor deixa o time decidir sozinho.
→ Se o time decide sozinho, então decisões são tomadas sem o contexto que só o gestor tem.
→ Se decisões são tomadas sem esse contexto, então algumas saem desalinhadas do que a empresa espera.
→ **Violação 2:** o time entrega rápido, mas o resultado precisa ser refeito.

E essa violação empurra de volta para **X**.

Ambos os movimentos são racionais. O loop, ainda assim, gira indefinidamente.

## Como construir

1. **Nomeie os dois comportamentos.** Devem ser observáveis e mutuamente exclusivos. Se é possível fazer os dois, não há loop.
2. **Suba cada cadeia separadamente**, respeitando o rigor do capítulo 09 — cada elo testado sozinho, sem saltos.
3. **Chegue a uma violação de objetivo em cada lado.** Ela precisa ser negativa o bastante para justificar a mudança de comportamento. Se ninguém mudaria por causa dela, você ainda não chegou lá.
4. **Feche o loop**: verifique que cada violação de fato empurra para o comportamento oposto.

## Verificação

- **Teste dos comportamentos:** são realmente exclusivos? Se coexistem, não é este o diagrama.
- **Teste das cadeias:** cada elo passa no teste de suficiência do capítulo 06?
- **Teste da violação:** o efeito final é ruim o suficiente para provocar a virada?
- **Teste do loop:** partindo de X e seguindo as setas, você volta a X?

Se o loop não fecha, ou você está diante de um dilema pontual — use a Nuvem do capítulo 10 — ou falta um elo em alguma das cadeias.

## Nuvem ou loop?

| | **Nuvem** (cap. 10) | **Loop** (este capítulo) |
|---|---|---|
| **Situação** | dilema no presente | problema que se repete no tempo |
| **Pergunta** | qual das duas escolher? | por que continuamos alternando? |
| **Estrutura** | pré-requisito | causa e efeito |
| **Revela** | as necessidades por trás das ações | por que cada correção gera a próxima crise |

As duas ferramentas são complementares, e frequentemente o mesmo problema comporta as duas leituras. Comece pela que responde à sua pergunta.

## Para que serve o diagrama

O valor imediato do loop não é a solução — é **tirar a culpa da conversa**.

Enquanto o problema for lido como falha de alguém, cada lado defende a própria posição. Com o loop desenhado, os dois lados veem que cada um está reagindo racionalmente à violação que enxerga — e que o adversário faz exatamente o mesmo do outro lado. A conversa muda de "você errou" para "estamos presos nisto".

A solução vem depois, pelo mesmo caminho da Nuvem: examinar as premissas de alguma conexão causal e quebrar a que sustenta o loop. É o capítulo 12.

## Erros comuns

**Comportamentos que não se excluem.** Se dá para fazer os dois, não há oscilação — há apenas duas práticas.

**Fechar o loop cedo demais.** Ligar diretamente um comportamento ao outro, sem passar pela violação de objetivo, esconde exatamente o que explica a oscilação.

**Repetir o mesmo efeito nos dois lados.** As violações precisam ser diferentes — são elas que dão a cada lado a sua razão.

**Confundir com "solução que falha".** Nem toda solução ruim gera loop. O loop exige que a correção do problema de um lado **crie** o problema do outro.

## Mão na massa

<div data-bateria="cap11"></div>

### Leitura executiva

Problemas recorrentes seguem um padrão de **oscilação entre dois comportamentos mutuamente exclusivos**, cada um adotado como correção do problema causado pelo outro. O diagrama sobe uma cadeia de causa e efeito de cada comportamento até uma **violação de objetivo**, e cada violação empurra para o lado oposto — fechando um loop autossustentável. Por isso trocar as pessoas não resolve: a estrutura permanece. O valor imediato do diagrama é retirar a culpa da conversa, mostrando que cada lado reage racionalmente à violação que enxerga. Use a Nuvem para dilemas do presente; o loop para o que se repete no tempo.
