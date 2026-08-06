# Pesquisa Operacional — handbook vivo

Fundamentação completa de Pesquisa Operacional (PO), com **exercícios que corrigem**, **vídeos
curados**, **módulos aplicados por domínio** e atualização contínua a partir da literatura
científica. Livro vivo, modular e evolutivo, com tutor de IA.

O sumário inteiro — 77 vagas declaradas em onze partes — está no
[**Mapa do handbook**](livro/mapa-do-handbook.md).

## A ideia

Há dois jeitos de sair mal de um curso de PO: sabendo pivotear um quadro do Simplex sem saber
o que é variável de decisão, ou sabendo chamar o solver sem entender o que ele faz. Este
handbook existe para o meio — **modelar com intenção e entender o algoritmo o suficiente para
desconfiar dele**.

Cada método aparece três vezes: intuição, matemática, código. Nessa ordem.

## Três camadas, três ritmos

| Camada | O que é | Como envelhece |
|---|---|---|
| **Núcleo** (Partes I–IX) | Fundamentos, programação linear, redes, programação inteira, metaheurísticas, não linear, incerteza, modelos probabilísticos, decisão | Devagar, por janela de revisão |
| **Aplicados** (Parte X) | Um módulo por domínio: suprimentos, roteamento, produção, energia, saúde, finanças… | Cresce **por adição**, sem tocar no núcleo |
| **Fronteira** (Parte XI) | Aprendizado de máquina em solvers, aprendizado orientado à decisão, modelos de linguagem como modeladores | Rápido, com **cláusula de expiração** obrigatória |

É essa separação que permite fundamentação sedimentada **e** atualização constante ao mesmo
tempo: o que muda toda semana não mora onde o aluno aprende a base.

## Como está organizado

| Diretório | O que é |
|---|---|
| `livro/` | O livro em Markdown. Comece pelo [Mapa](livro/mapa-do-handbook.md) e pelo [Guia Editorial](livro/GUIA-EDITORIAL.md) |
| `radar/` | O [Radar científico](radar/RADAR.md): artigos lidos, datados, com o que cada um muda no livro |
| `po-zero/` | A [construção prática](po-zero/README.md): Python + PuLP/Pyomo + HiGHS, uma etapa por capítulo de método |
| `publicar/` | O motor: Markdown → HTML + PDF. `sumario.json` declara a estrutura publicada |
| `chat-companion/` | O tutor: FastAPI + RAG sobre o texto, correção de exercícios, progresso |
| `estudos/` | Notas de pesquisa — a começar pelo [corpo de conhecimento da PO](estudos/001-corpo-de-conhecimento-po.md) |
| `specs/` | Uma pasta por rodada (metodologia Maestro) |
| `adr/` | Decisões de arquitetura, com alternativas e consequências |

## Rodar localmente

```bash
# o site
cd publicar && npm ci && npm run build      # gera docs/ e roda os portões de qualidade
python3 -m http.server 8000 --directory ../docs

# o tutor (sobe sem chave nem banco, em modo echo + memória)
cd chat-companion/backend && pip install -r requirements.txt
uvicorn app:app --reload
python -m pytest -q
```

## Como contribuir

O trabalho segue a metodologia **[Maestro](https://github.com/GHDaru/maestro)**: uma
especificação por rodada, cada rodada em sua branch, com gates humanos para especificação,
plano e merge. As regras estão em [`CLAUDE.md`](CLAUDE.md) e na
[constituição](.specify/memory/constitution.md); as regras de escrita, no
[Guia Editorial](livro/GUIA-EDITORIAL.md).

O que vem a seguir está no [ROADMAP](ROADMAP.md).

## Créditos e licenças

- **Vídeos.** A curadoria conta com o canal de [João Sarubbi](https://www.youtube.com/@joaosarubbi)
  (CEFET-MG), cujo uso foi autorizado pelo autor do canal. A política está na
  [Videoteca](livro/videoteca.md).
- **Texto do livro:** ver [`LICENSE`](LICENSE).
- **Código** (motor de publicação, tutor e `po-zero`): MIT — ver [`LICENSE-CODE`](LICENSE-CODE).
  O motor é derivado do livro *Engenharia de Harness*, do mesmo autor
  ([ADR 0001](adr/0001-reuso-motor-livro-vivo.md)).
