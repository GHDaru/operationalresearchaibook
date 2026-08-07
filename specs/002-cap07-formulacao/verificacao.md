# Verificação 002 — Capítulo 07

> **Executada em 2026-08-06.** "Prove, não declare" (constituição, Princípio XI): a saída
> abaixo é colada, não parafraseada.

## Build do site — todos os portões

```
✓ espelho de capacidades em sincronia (5 capacidades)
✓ referências de capítulo OK: 0 referências (0 compostas) apontam para capítulos existentes — a aderência semântica é leitura humana
✓ Grafo do livro: 10 nós, 12 arestas
✓ Livro gerado [pt]: 11 páginas + capa em docs/ (links internos OK)
✓ template verificado [pt]: 2 capítulos com C01/N02 + 9 páginas de aparato OK
✓ registro de exercícios OK: 4 exercícios em 1 baterias, rubrica não publicada
```

## Testes do backend

```
24 passed, 1 warning in 0.57s
```

## Determinismo do experimento

Duas execuções seguidas, hash do arquivo gerado:

```
  correto (margem): {'mesa': 30.0, 'estante': 40.0} -> R$ 13800.00
  errado (receita): {'mesa': 60.0, 'estante': 0.0} -> margem R$ 13200.00
  custo do erro:    R$ 600.00 por mês
d35de6819d5d194204085d451000bb84  resultados.json
d35de6819d5d194204085d451000bb84  resultados.json
```

## O portão novo, provado quebrando de propósito

Com o objetivo do `cap07.exA` trocado para um que o capítulo não declara:

```
   cap07.exA: objetivo "O9" não é declarado em 07-formulacao.md
exit: 1
```

Restaurado:

```
✓ registro de exercícios OK: 4 exercícios em 1 baterias, rubrica não publicada
exit: 0
```

## Conferência número a número

Todo número do capítulo, contra `po-zero/etapa-01-formulacao/resultados.json`:

| Número no capítulo | Campo em `resultados.json` | Confere |
|---|---|---|
| 60 mesas, 0 estantes | `modelo_errado_receita.plano` | ✅ |
| Receita de R$ 54.000 | `modelo_errado_receita.receita_total_reais` | ✅ |
| 30 mesas, 40 estantes | `modelo_correto_margem.plano` | ✅ |
| Margem de R$ 13.800 | `modelo_correto_margem.margem_total_reais` | ✅ |
| Margem de R$ 13.200 no plano errado | `modelo_errado_receita.margem_total_reais` | ✅ |
| Diferença de R$ 600 por mês | `custo_do_erro.margem_perdida_reais_por_mes` | ✅ |
| 60 horas de acabamento paradas | `modelo_errado_receita.folga_dos_recursos.acabamento_h` | ✅ |
| Folga zero nos dois recursos (plano correto) | `modelo_correto_margem.folga_dos_recursos` | ✅ |
| Receita de R$ 47.000 (plano correto) | `modelo_correto_margem.receita_total_reais` | ✅ |

## O que esta verificação NÃO cobre

- **Se o capítulo ensina bem.** Nenhum portão mede isso; é leitura humana, e é o gate do autor.
- **O vídeo.** Continua `⏳` — a dívida está declarada no capítulo, na Videoteca e no histórico.
- **Revisão em contexto fresco.** Quem executou não verifica (Maestro, Princípio II).
