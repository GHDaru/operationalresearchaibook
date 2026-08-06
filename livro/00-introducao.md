# 00 — Introdução

> **Conteúdo revisado em 2026-08** · edição inaugural · [histórico](HISTORICO.md)

## O problema que este handbook resolve

Há dois jeitos de sair mal de um curso de Pesquisa Operacional (PO).

O primeiro é sair sabendo **executar** e não sabendo **modelar**: pivotear um quadro do Simplex à mão sem conseguir olhar para uma operação real e dizer o que é variável de decisão. Esse aluno passa na prova e trava no primeiro problema que ninguém formulou para ele.

O segundo é sair sabendo **chamar o solver** e não sabendo o que ele faz: escrever quinze linhas de Python, receber um número e não ter como distinguir um modelo certo de um modelo que responde à pergunta errada com quatro casas decimais. Esse aluno é produtivo até o dia em que o resultado é absurdo — e aí não tem por onde começar a procurar.

Este handbook existe para o meio: **modelar com intenção e entender o algoritmo o suficiente para desconfiar dele**. É por isso que cada método aparece três vezes — a intuição, a matemática e o código — e nessa ordem.

## Para quem é

Para quem está aprendendo PO em curso de graduação e para quem já trabalha com decisão e quer a fundamentação que faltou. O pré-requisito honesto é álgebra linear básica e alguma familiaridade com programação; onde for preciso mais do que isso, o texto avisa e ensina.

Ele também é o **corpo de conhecimento de uma disciplina real** — o que o autor aplica com os próprios alunos. Isso tem uma consequência boa para quem lê de fora: o material é testado em sala, e o que não funciona é reescrito.

## As três camadas

O handbook não é uma lista de capítulos. São três camadas que envelhecem em ritmos diferentes, e essa é a decisão de projeto mais importante do livro:

- **O núcleo** — fundamentos, programação linear, redes, programação inteira, metaheurísticas, otimização não linear, otimização sob incerteza, modelos probabilísticos e decisão. É a base em que os livros-texto de referência concordam. Muda devagar, de propósito.
- **Os módulos aplicados** — um por domínio: cadeia de suprimentos, roteamento, produção, energia, saúde, finanças e assim por diante. Cada um é fechado em si e entra sem mexer nos outros. **Esta camada cresce indefinidamente.**
- **A fronteira** — o que está se movendo agora: aprendizado de máquina dentro de solvers, aprendizado orientado à decisão, modelos de linguagem como modeladores. Aqui todo capítulo carrega **cláusula de expiração**.

A separação existe para sustentar duas promessas que normalmente se atrapalham: fundamentação sedimentada **e** atualização científica constante. O truque é não deixar o que muda toda semana morar no lugar onde o aluno aprende a base.

O mapa inteiro, com as vagas já declaradas, está em [Mapa do handbook](mapa-do-handbook.md).

## Como se estuda por ele

Cada capítulo é um ciclo fechado, sempre na mesma ordem: **objetivos de aprendizagem → o problema → intuição → matemática → código → prática com devolutiva → vídeo → síntese → verificação**.

Três coisas valem a pena saber antes de começar:

1. **Os exercícios corrigem.** A resposta vai ao servidor, que avalia, explica o porquê e devolve você à seção certa. Na primeira tentativa errada ele explica o conceito; só na segunda revela o esperado. Errar faz parte do desenho.
2. **Os vídeos são escolhidos pelo que o texto não faz bem.** Geometria animada, uma derivação no ritmo do quadro. Vídeo que só repete o capítulo não entra.
3. **Há código que roda.** A construção prática `po-zero` acompanha o livro: modelos em Python que resolvem os problemas do capítulo, com implementações didáticas dos algoritmos ao lado de solvers de mercado. Tudo em CPU, sem licença paga.

## O que o handbook exige de si mesmo

Quatro compromissos que valem como regra, não como intenção:

- **Nenhum número sem procedência.** Ou é medido por um experimento do `po-zero`, com semente e versão declaradas, ou é citado, ou não é afirmado.
- **Toda afirmação sobre o estado da arte é datada.** O selo no topo de cada capítulo diz quando aquilo foi verdade.
- **Capítulo sem prática com devolutiva está incompleto**, por melhor que esteja escrito.
- **Artigo científico entra pelo Radar**, datado, com o registro do que ele muda no livro — e não por menção solta no texto.

## Um livro vivo

Nenhuma versão é final. Cada capítulo traz a data da última revisão e o [histórico](HISTORICO.md) registra o que mudou a cada edição. Conforme a literatura avança e a prática em sala mostra o que não funciona, o texto é reescrito.

Isso tem uma consequência para você: se algo aqui não estiver claro, a hipótese de trabalho é que **o texto está mal escrito**, não que você não entendeu. Exercício com taxa de acerto muito baixa entra na fila de revisão do capítulo — o erro do leitor é o sinal que corrige o livro.

## Nota de autoria e método

Este handbook é **co-escrito com um agente de IA** sob autoria, curadoria e responsabilidade humanas. O agente pesquisa, redige e executa o ciclo de produção; o autor humano define o escopo, decide, verifica cada fonte e responde pelo conteúdo. Seguindo as políticas editoriais de autoria vigentes, a IA **não** é listada como autora — não pode ser responsável — e seu uso é divulgado aqui, na abertura.

O processo de produção segue a metodologia [Maestro](https://github.com/GHDaru/maestro): a especificação é a fonte de verdade, os agentes executam, o humano decide, aprova e verifica. As regras de escrita estão no [Guia Editorial](GUIA-EDITORIAL.md).

## Sobre as fontes

O texto é **autoral**. Os livros-texto que fundamentam o campo são citados por fonte oficial na [Bibliografia](bibliografia.md), e materiais de terceiros não são reproduzidos aqui.

Nada neste handbook substitui as obras de referência. Ele se propõe a outra coisa: ser o caminho praticado, datado e conectado à literatura corrente que um livro-texto impresso, por natureza, não consegue ser.

### Leitura executiva

Este é um handbook de Pesquisa Operacional construído para o meio-termo que os cursos costumam perder: **modelar com intenção e entender o algoritmo o suficiente para desconfiar dele**. Cada método aparece como intuição, depois matemática, depois código. A estrutura tem três camadas com ritmos próprios — um núcleo estável de fundamentos e métodos, uma camada de módulos aplicados que cresce por adição, e uma camada de fronteira com cláusula de expiração obrigatória. Os exercícios são corrigidos no servidor, com devolutiva que explica; os vídeos entram pelo que o texto não faz bem; e a construção prática `po-zero` garante que todo número afirmado tenha um script que o regenera. É um livro vivo: datado, versionado e reescrito conforme a literatura avança e a sala de aula mostra o que não funciona.
