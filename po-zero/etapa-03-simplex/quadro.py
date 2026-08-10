"""O Simplex de quadro, escrito para ser lido — não para ser rápido.

Esta é a implementação didática do capítulo 09. Ela executa exatamente o
procedimento que o leitor faz à mão no papel, e por isso faz três escolhas que
nenhum solver de verdade faria:

  1. **Aritmética exata** (`Fraction`). O quadro impresso aqui é o quadro do
     caderno: 1/2 é 1/2, e não 0.4999999999999999. Sem isso, comparar "o que
     dá no papel" com "o que dá na máquina" viraria discussão sobre epsilon.
  2. **O quadro inteiro é guardado a cada iteração.** Um solver descarta;
     aqui a sequência de quadros *é* o produto — é o que o capítulo publica.
  3. **O *big-M* é simbólico.** Cada coeficiente de custo é o par
     `(parte em M, parte numérica)`, com M tratado como "maior que qualquer
     número que apareça". É como se faz no quadro-negro: a coluna de M anda ao
     lado da numérica, e nunca se escolhe um valor para M. Escolher um valor
     concreto (1e6, digamos) é o atalho que produz o erro clássico de M pequeno
     demais, em que uma solução inviável parece ótima.

Fora isso, é o Simplex primal com regra de Dantzig: entra quem tem o custo
reduzido mais negativo, sai quem o teste da razão apontar.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Literal

Num = Fraction


class CustoM:
    """Um número da forma `m·M + n`, com M arbitrariamente grande e positivo.

    Existe para que o *big-M* seja exato. A comparação é lexicográfica: quem
    tem parte em M menor é menor, porque M domina qualquer parte numérica —
    que é precisamente o que "M grande o suficiente" quer dizer.
    """

    __slots__ = ("m", "n")

    def __init__(self, m: Num | int = 0, n: Num | int = 0) -> None:
        self.m, self.n = Fraction(m), Fraction(n)

    def __add__(self, o: "CustoM") -> "CustoM":
        return CustoM(self.m + o.m, self.n + o.n)

    def __sub__(self, o: "CustoM") -> "CustoM":
        return CustoM(self.m - o.m, self.n - o.n)

    def __mul__(self, k: Num) -> "CustoM":
        return CustoM(self.m * k, self.n * k)

    def __lt__(self, o: "CustoM") -> bool:
        return (self.m, self.n) < (o.m, o.n)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, CustoM) and (self.m, self.n) == (o.m, o.n)

    def negativo(self) -> bool:
        return (self.m, self.n) < (0, 0)

    def texto(self) -> str:
        if self.m == 0:
            return fmt(self.n)
        base = f"{fmt(self.m)}M" if abs(self.m) != 1 else ("M" if self.m > 0 else "-M")
        if self.n == 0:
            return base
        return f"{base} {'+' if self.n > 0 else '-'} {fmt(abs(self.n))}"


def fmt(v: Num) -> str:
    """Fração como o caderno escreve: inteiro quando é inteiro."""
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


@dataclass
class Restricao:
    coefs: list[Num]
    sinal: Literal["<=", ">=", "="]
    b: Num
    rotulo: str = ""


@dataclass
class Iteracao:
    numero: int
    base: list[str]
    colunas: list[str]
    corpo: list[list[Num]]        # uma linha por restrição, sem o lado direito
    lado_direito: list[Num]
    linha_z: list[CustoM]         # custos reduzidos, uma entrada por coluna
    valor_z: CustoM
    ponto: list[Num]              # valor das variáveis de decisão neste quadro
    entra: str | None = None
    sai: str | None = None
    razoes: dict[str, str] = field(default_factory=dict)


def montar(
    lucros: list[Num],
    restricoes: list[Restricao],
    nomes: list[str] | None = None,
) -> tuple[list[str], list[list[Num]], list[Num], list[CustoM], list[int], set[str]]:
    """Põe o modelo na forma padrão e devolve o primeiro quadro.

    Cada `<=` ganha uma folga, que entra na base. Cada `>=` ganha um excesso
    (que **não** serve de base, porque entra com coeficiente -1) e uma
    artificial, que serve. Cada `=` ganha só a artificial. É a razão de o
    *big-M* existir: sem artificial, uma restrição `>=` ou `=` não oferece
    coluna de base viável, e o algoritmo não teria de onde partir.
    """
    n = len(lucros)
    nomes = nomes or [f"x{i+1}" for i in range(n)]
    colunas = list(nomes)
    custos = [CustoM(0, c) for c in lucros]
    corpo = [[Fraction(v) for v in r.coefs] for r in restricoes]
    lado = [Fraction(r.b) for r in restricoes]
    base: list[int] = [-1] * len(restricoes)
    artificiais: set[str] = set()

    # Lado direito negativo inverteria o sentido da desigualdade sem avisar.
    for i, r in enumerate(restricoes):
        if lado[i] < 0:
            corpo[i] = [-v for v in corpo[i]]
            lado[i] = -lado[i]
            r.sinal = {"<=": ">=", ">=": "<=", "=": "="}[r.sinal]

    def nova_coluna(nome: str, custo: CustoM, linha: int, coef: Num) -> int:
        colunas.append(nome)
        custos.append(custo)
        for j, l in enumerate(corpo):
            l.append(coef if j == linha else Fraction(0))
        return len(colunas) - 1

    for i, r in enumerate(restricoes):
        if r.sinal == "<=":
            base[i] = nova_coluna(f"f{i+1}", CustoM(0, 0), i, Fraction(1))
        else:
            if r.sinal == ">=":
                nova_coluna(f"e{i+1}", CustoM(0, 0), i, Fraction(-1))
            nome = f"a{i+1}"
            artificiais.add(nome)
            base[i] = nova_coluna(nome, CustoM(-1, 0), i, Fraction(1))

    return colunas, corpo, lado, custos, base, artificiais


def resolver(
    lucros: list[Num],
    restricoes: list[Restricao],
    nomes: list[str] | None = None,
    limite: int = 100,
) -> dict:
    """Executa o Simplex de quadro e devolve **todas** as iterações."""
    colunas, corpo, lado, custos, base, artificiais = montar(lucros, restricoes, nomes)
    n_dec = len(lucros)
    iteracoes: list[Iteracao] = []
    status = "otimo"

    for k in range(limite + 1):
        # Linha z: custo reduzido de cada coluna é z_j - c_j, com
        # z_j = soma dos custos das básicas vezes a coluna.
        cb = [custos[b] for b in base]
        linha_z = [
            sum((cb[i] * corpo[i][j] for i in range(len(base))), CustoM()) - custos[j]
            for j in range(len(colunas))
        ]
        valor_z = sum((cb[i] * lado[i] for i in range(len(base))), CustoM())

        ponto = [Fraction(0)] * n_dec
        for i, b in enumerate(base):
            if b < n_dec:
                ponto[b] = lado[i]

        it = Iteracao(
            numero=k,
            base=[colunas[b] for b in base],
            colunas=list(colunas),
            corpo=[list(l) for l in corpo],
            lado_direito=list(lado),
            linha_z=list(linha_z),
            valor_z=valor_z,
            ponto=list(ponto),
        )

        # Parada: nenhum custo reduzido negativo, ninguém sobe mais.
        candidatos = [j for j in range(len(colunas)) if linha_z[j].negativo()]
        if not candidatos:
            iteracoes.append(it)
            break

        entra = min(candidatos, key=lambda j: (linha_z[j].m, linha_z[j].n, j))
        it.entra = colunas[entra]

        # Teste da razão: até onde dá para andar antes de alguma básica zerar.
        razoes = {i: lado[i] / corpo[i][entra] for i in range(len(base)) if corpo[i][entra] > 0}
        it.razoes = {colunas[base[i]]: fmt(r) for i, r in razoes.items()}
        if not razoes:
            it.sai = None
            iteracoes.append(it)
            status = "ilimitado"
            break

        melhor = min(razoes.values())
        # Empate no teste da razão é degenerescência; desempata pelo menor
        # índice (regra de Bland parcial), que é o que evita ciclagem.
        sai = min(i for i, r in razoes.items() if r == melhor)
        it.sai = colunas[base[sai]]
        iteracoes.append(it)

        if k == limite:
            status = "limite_de_iteracoes"
            break

        # Pivoteamento.
        piv = corpo[sai][entra]
        corpo[sai] = [v / piv for v in corpo[sai]]
        lado[sai] = lado[sai] / piv
        for i in range(len(base)):
            if i == sai:
                continue
            f = corpo[i][entra]
            if f != 0:
                corpo[i] = [v - f * w for v, w in zip(corpo[i], corpo[sai])]
                lado[i] = lado[i] - f * lado[sai]
        base[sai] = entra

    final = iteracoes[-1]
    # Artificial que sobra na base com valor positivo é o atestado de
    # inviabilidade: o modelo só "fecha" com uma quantidade fictícia.
    if status == "otimo":
        for i, b in enumerate(base):
            if colunas[b] in artificiais and lado[i] > 0:
                status = "inviavel"
                break

    return {
        "status": status,
        "iteracoes": iteracoes,
        "colunas": colunas,
        "artificiais": sorted(artificiais),
        "ponto": [fmt(v) for v in final.ponto] if status == "otimo" else None,
        "ponto_float": [float(v) for v in final.ponto] if status == "otimo" else None,
        "valor": fmt(final.valor_z.n) if status == "otimo" else None,
        "valor_float": float(final.valor_z.n) if status == "otimo" else None,
        "pivos": sum(1 for it in iteracoes if it.sai is not None),
        "vertices": [[fmt(v) for v in it.ponto] for it in iteracoes],
    }


def imprimir(it: Iteracao) -> str:
    """O quadro em texto, na mesma disposição do caderno."""
    larg = max([6] + [len(c) for c in it.colunas] + [len(z.texto()) for z in it.linha_z])
    cab = "base".ljust(8) + "".join(c.rjust(larg + 2) for c in it.colunas) + "b".rjust(larg + 2)
    linhas = [cab, "-" * len(cab)]
    for i, b in enumerate(it.base):
        linhas.append(
            b.ljust(8)
            + "".join(fmt(v).rjust(larg + 2) for v in it.corpo[i])
            + fmt(it.lado_direito[i]).rjust(larg + 2)
        )
    linhas.append(
        "z".ljust(8)
        + "".join(z.texto().rjust(larg + 2) for z in it.linha_z)
        + it.valor_z.texto().rjust(larg + 2)
    )
    return "\n".join(linhas)
