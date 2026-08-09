"""Etapa 02 — O método gráfico, feito do jeito que o aluno faz no papel.

A ideia central do capítulo: **todo vértice é a interseção de duas restrições
tratadas como igualdade**. Então o procedimento é mecânico:

  1. tome as restrições duas a duas;
  2. troque `<=` por `=` e resolva o sistema 2x2;
  3. jogue fora o que não satisfaz TODAS as outras restrições;
  4. avalie o lucro no que sobrou.

Isto não é o Simplex — é força bruta sobre pares. Serve para dois motivos: é
exatamente o que o leitor faz no GeoGebra, e prova, no caso pequeno, a afirmação
que o capítulo faz e não demonstra: *o ótimo está sempre num vértice*.

A não-negatividade entra como restrição de verdade (`-x <= 0`), e não como caso
especial. É isso que faz os eixos aparecerem como duas retas iguais às outras —
e é a razão de o primeiro quadrante ser, ele próprio, uma interseção.
"""

from __future__ import annotations

from itertools import combinations


class Restricao:
    """a1*x1 + a2*x2 <= b, com um rótulo para o capítulo poder citá-la."""

    def __init__(self, a1: float, a2: float, b: float, rotulo: str) -> None:
        self.a1, self.a2, self.b, self.rotulo = a1, a2, b, rotulo

    def satisfeita(self, p: tuple[float, float], tol: float = 1e-9) -> bool:
        return self.a1 * p[0] + self.a2 * p[1] <= self.b + tol

    def ativa(self, p: tuple[float, float], tol: float = 1e-9) -> bool:
        """Ativa = sem folga. É a restrição que está segurando o ponto."""
        return abs(self.a1 * p[0] + self.a2 * p[1] - self.b) <= tol

    def folga(self, p: tuple[float, float]) -> float:
        return round(self.b - (self.a1 * p[0] + self.a2 * p[1]), 9)


NAO_NEGATIVIDADE = [
    Restricao(-1, 0, 0, "x1 >= 0"),
    Restricao(0, -1, 0, "x2 >= 0"),
]


def cruzar(r: Restricao, s: Restricao) -> tuple[float, float] | None:
    """Interseção das duas retas. None quando são paralelas."""
    det = r.a1 * s.a2 - r.a2 * s.a1
    if abs(det) < 1e-12:
        return None
    x1 = (r.b * s.a2 - r.a2 * s.b) / det
    x2 = (r.a1 * s.b - r.b * s.a1) / det
    # `or 0.0` normaliza o zero negativo: -0.0 é falsy, e imprimir "-0" num livro
    # que fala de rigor é ruído gratuito.
    return (round(x1, 9) or 0.0, round(x2, 9) or 0.0)


def vertices(restricoes: list[Restricao], lucro: tuple[float, float]) -> list[dict]:
    """Todos os candidatos, com o veredito de cada um — inclusive os descartados.

    Devolver também os inviáveis é decisão didática: o capítulo mostra que a
    conta é fácil e o que dá trabalho é a TRIAGEM.
    """
    achados: list[dict] = []
    for r, s in combinations(restricoes, 2):
        p = cruzar(r, s)
        if p is None:
            continue
        viavel = all(t.satisfeita(p) for t in restricoes)
        violadas = [t.rotulo for t in restricoes if not t.satisfeita(p)]
        achados.append({
            "ponto": list(p),
            "das_restricoes": [r.rotulo, s.rotulo],
            "viavel": viavel,
            "violou": violadas,
            "lucro": round(lucro[0] * p[0] + lucro[1] * p[1], 6) if viavel else None,
        })
    # Um mesmo vértice pode aparecer por mais de um par (degenerescência). Aqui a
    # instância não tem esse caso, mas a deduplicação fica para o capítulo que trata dele.
    return achados


def resolver(restricoes: list[Restricao], lucro: tuple[float, float]) -> dict:
    todas = restricoes + NAO_NEGATIVIDADE
    cands = vertices(todas, lucro)
    viaveis = [c for c in cands if c["viavel"]]
    otimo = max(viaveis, key=lambda c: c["lucro"]) if viaveis else None
    if otimo:
        p = tuple(otimo["ponto"])
        otimo = {
            **otimo,
            "restricoes_ativas": [t.rotulo for t in todas if t.ativa(p)],
            "folgas": {t.rotulo: t.folga(p) for t in todas},
        }
    return {"candidatos": cands, "viaveis": viaveis, "otimo": otimo}
