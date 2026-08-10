"""Os cinco casos em que o Simplex **não** devolve "aqui está seu plano".

Esta etapa não implementa um método novo: ela **instrumenta** o Simplex do
capítulo 09 para que cada veredito possa ser observado, e não apenas descrito.

A instrumentação é de dois tipos:

1. **Detecção de ciclo por repetição de base.** `quadro.resolver` devolve todas
   as iterações; se uma base se repete, houve ciclo — e o período é a distância
   entre as duas ocorrências. A detecção é *post-hoc*, de propósito: o motor do
   capítulo 09 fica exatamente como foi publicado.

2. **Leitura do quadro final.** Duas perguntas que o quadro responde e o número
   sozinho não: *há variável básica valendo zero?* (vértice degenerado) e *há
   custo reduzido zero em variável fora da base?* (mais de um plano ótimo).

O que **não** está aqui, e é dito porque omitir seria pior: nenhuma prova. Que a
regra de Bland termina é **medido** nesta etapa, não demonstrado (ver ADR 0008).
"""

from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

# O Simplex é o do capítulo 09. Reusar em vez de duplicar é decisão de projeto,
# registrada no plano da rodada 006: duplicar duzentas linhas para trocar duas
# escolhas seria pior de ler e pior de manter.
sys.path.insert(0, str(Path(__file__).parent.parent / "etapa-03-simplex"))
from quadro import Restricao, fmt, imprimir, resolver  # noqa: E402


def ciclo(iteracoes) -> dict | None:
    """Procura uma base repetida. Se houver, houve ciclo — e o período é a
    distância entre as duas primeiras ocorrências."""
    vistas: dict[tuple, int] = {}
    for it in iteracoes:
        chave = tuple(sorted(it.base))
        if chave in vistas:
            return {
                "houve_ciclo": True,
                "base_repetida": list(it.base),
                "primeira_ocorrencia": vistas[chave],
                "repetiu_em": it.numero,
                "periodo": it.numero - vistas[chave],
            }
        vistas[chave] = it.numero
    return None


def degenerado(it) -> dict:
    """Vértice degenerado: alguma variável **na base** vale zero.

    É o sinal algébrico do que o capítulo 08 mostrou no desenho — mais
    restrições passando pelo vértice do que o necessário para sustentá-lo.
    """
    zeros = [it.base[i] for i, v in enumerate(it.lado_direito) if v == 0]
    return {"degenerado": bool(zeros), "basicas_em_zero": zeros}


def multiplos_otimos(it, n_dec: int) -> dict:
    """Mais de um plano ótimo: custo reduzido **zero** numa variável **fora** da
    base. Andar naquela coluna não muda o objetivo — leva a outro vértice com o
    mesmo valor."""
    fora = [j for j in range(len(it.colunas)) if it.colunas[j] not in it.base]
    empatadas = [it.colunas[j] for j in fora if it.linha_z[j].m == 0 and it.linha_z[j].n == 0]
    return {"multiplos_otimos": bool(empatadas), "colunas_com_custo_reduzido_zero": empatadas}


def analisar(nome: str, descricao: str, lucros, restricoes, regra="dantzig", limite=100) -> dict:
    r = resolver([F(c) for c in lucros], restricoes, limite=limite, regra=regra)
    final = r["iteracoes"][-1]
    return {
        "descricao": descricao,
        "regra": regra,
        "status": r["status"],
        "pivos": r["pivos"],
        "ponto": r["ponto"],
        "valor": r["valor"],
        "caminho": r["vertices"],
        "ciclo": ciclo(r["iteracoes"]),
        "vertice": degenerado(final),
        "otimo": multiplos_otimos(final, len(lucros)) if r["status"] == "otimo" else None,
        "quadro_final": imprimir(final),
        "empates_no_teste_da_razao": [
            {"iteracao": it.numero, "razoes": it.razoes}
            for it in r["iteracoes"]
            if len(it.razoes) > 1 and len(set(it.razoes.values())) < len(it.razoes)
        ],
    }
