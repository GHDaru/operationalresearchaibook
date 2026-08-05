"""Registro de exercícios — a fonte da verdade do que o leitor está praticando.

A página do livro declara apenas o **identificador** do exercício em foco; o
enunciado e os critérios de avaliação são resolvidos aqui, no servidor. Duas
consequências que valem o desenho:

  1. o leitor não consegue forjar um exercício que não existe (nem alterar os
     critérios pelos quais será avaliado);
  2. o enunciado não paga tokens de ida e volta a cada turno.

O arquivo-fonte é `livro/exercicios.json` (conteúdo editorial, versionado com o
livro). Em deploy isolado — Railway com Root Directory na pasta do backend —
vale a cópia empacotada ao lado do `corpus.json`, gerada por `build_corpus.py`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


class Exercicios:
    """Índice imutável de exercícios, por id."""

    def __init__(self, repo_root: Path, pacote: Optional[Path] = None) -> None:
        self._por_id: dict[str, dict] = {}
        for origem in (repo_root / "livro" / "exercicios.json", pacote):
            if origem and Path(origem).exists():
                try:
                    dados = json.loads(Path(origem).read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    continue
                for ex in dados:
                    if isinstance(ex, dict) and ex.get("id"):
                        self._por_id[str(ex["id"])] = ex
                if self._por_id:
                    break

    def get(self, exercicio_id: str) -> Optional[dict]:
        return self._por_id.get((exercicio_id or "").strip())

    def do_capitulo(self, capitulo: int) -> list[dict]:
        return [e for e in self._por_id.values() if e.get("capitulo") == capitulo]

    def __len__(self) -> int:
        return len(self._por_id)

    def para_prompt(self, ex: dict) -> str:
        """O exercício como o modelo o recebe — enunciado e critérios explícitos.

        Os critérios são a rubrica: é o que separa uma devolutiva fundamentada de
        um elogio genérico. Vão para o modelo, nunca para o cliente.
        """
        criterios = "\n".join(f"  - {c}" for c in ex.get("criterios", []))
        erro = ex.get("erro_provavel", "")
        guia = ex.get("resposta_guia", "")
        partes = [
            f"Exercício em foco, declarado pela página do livro (id {ex['id']}, "
            f"capítulo {ex.get('capitulo')}, variante {ex.get('variante', '-')}, "
            f"tipo {ex.get('tipo', '-')}):",
            f"Título: {ex.get('titulo', '')}",
            f"Enunciado: {ex.get('enunciado', '')}",
            "Critérios de avaliação (a rubrica; avalie contra eles e diga quais foram "
            f"atendidos e quais não):\n{criterios}",
        ]
        if erro:
            # A devolutiva mais valiosa é a que explica o MECANISMO do erro. Ela vem
            # escrita aqui para o tutor não ter de improvisar — mas só é usada se o
            # leitor de fato cometer o erro.
            partes.append(
                f"Erro provável nesta tarefa (use APENAS se o leitor cometê-lo; explique "
                f"o mecanismo, nunca diga só 'errado'): {erro}")
        if guia:
            partes.append(
                f"Resposta-guia (NUNCA entregue ao leitor antes de ele responder; serve "
                f"para você julgar equivalência de RACIOCÍNIO, não de palavras — resposta "
                f"diferente com a mesma linha de raciocínio está correta): {guia}")
        partes.append(
            "Conduza este exercício: se o leitor ainda não respondeu, peça a resposta "
            "dele — uma pergunta por vez. Se já respondeu, avalie contra os critérios, "
            "dê a devolutiva explicando o porquê, e registre a tentativa com a "
            "ferramenta 'exercicio_registrar_tentativa'. Continue valendo a regra "
            "inegociável: você não resolve o exercício pelo leitor.")
        return "\n".join(partes)
