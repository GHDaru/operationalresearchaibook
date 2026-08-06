# ADR 0003 — Pilha do `po-zero`: Python com PuLP/Pyomo e solver aberto

**Data:** 2026-08-06 · **Status:** aceito

## Contexto

A constituição exige que toda afirmação empírica tenha um experimento reproduzível (Princípio
III) e que a fonte-base seja código que roda em CPU sem licença paga (Princípio IV). Isso
transforma a escolha de pilha em decisão constitucional, não em preferência de ferramenta.

Há uma tensão real: a sintaxe que os alunos vão encontrar no mercado é a de solvers comerciais
(Gurobi, CPLEX), cujas licenças acadêmicas são gratuitas — mas cuja dependência quebraria o
requisito de custo zero para quem lê o livro de fora da universidade.

## Decisão

**Python 3.11+, modelagem em PuLP e Pyomo, solver HiGHS (padrão) com CBC como alternativa.**
NumPy e SciPy para as implementações didáticas.

- **PuLP** nos primeiros capítulos: a menor distância entre a notação matemática e a primeira
  linha de código. O aluno enxerga a formulação.
- **Pyomo** quando o modelo cresce: conjuntos indexados, blocos, parametrização.
- **HiGHS** como solver padrão — aberto, empacotado via `pip`, competitivo em programação
  linear e inteira mista.
- **Solver comercial aparece como comparação**, nunca como dependência. Um capítulo pode
  mostrar a diferença de desempenho; nenhum capítulo pode exigir a licença para rodar.

Vale também a **regra das duas implementações**: cada método algorítmico do núcleo aparece como
implementação didática em NumPy *e* como chamada ao solver, e o capítulo compara as duas.

## Alternativas avaliadas

| Alternativa | Por que não |
|---|---|
| Gurobi/CPLEX com licença acadêmica | Quebra o custo zero para leitor fora da universidade. Fica como comparação |
| Planilha (Solver do Excel/LibreOffice) como porta de entrada | Boa didática inicial, mas não sustenta reprodutibilidade: não há semente, versão nem script que regenere o número. Pode aparecer como ponte, nunca como fonte de evidência |
| OR-Tools como pilha única | Excelente em roteamento e programação por restrições, mas a modelagem linear é menos legível que a de PuLP para quem está aprendendo a formular |
| Julia/JuMP | Modelagem elegante, comunidade menor entre os alunos-alvo; adiciona uma linguagem a aprender antes do conteúdo |

## Consequências

**Boas.** Qualquer leitor roda tudo com `pip install`, sem cadastro e sem licença. As duas
implementações endereçam diretamente os dois modos de sair mal de um curso de Pesquisa
Operacional (PO) descritos na introdução do handbook.

**Ruins, e assumidas.** Em instâncias grandes o HiGHS perde para os solvers comerciais, e há
capítulos — programação inteira de porte industrial — em que essa diferença é parte do assunto.
A saída é honesta: reduzir a instância publicada e documentar a instância cheia à parte, sempre
declarando qual foi usada.

**Obrigação decorrente.** Versão de Python, de bibliotecas e do solver entram em cada
`resultados.json`. Número medido com versão não declarada não é evidência.
