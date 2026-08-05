#!/usr/bin/env bash
# Sincroniza as skills, comandos e agentes do Maestro neste repositório.
#
# Por que existe: a constituição (Princípio VI) declara o Maestro como regra
# vigente e as skills como instaladas. Cópia manual apodrece em silêncio — e
# "divergência silenciosa entre a regra publicada e a instalada é o pior dos
# dois mundos". Este script torna a ressincronia uma linha, e o --check
# transforma a sincronia num portão verificável.
#
# Uso:
#   scripts/sync-maestro.sh            # sincroniza a partir do clone padrão
#   MAESTRO=/caminho scripts/sync-maestro.sh
#   scripts/sync-maestro.sh --check    # não escreve; sai 1 se houver divergência
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAESTRO="${MAESTRO:-$(cd "$RAIZ/../maestro" 2>/dev/null && pwd || true)}"
CHECK=0
[[ "${1:-}" == "--check" ]] && CHECK=1

if [[ -z "$MAESTRO" || ! -d "$MAESTRO/skills" ]]; then
  echo "erro: repositório do Maestro não encontrado." >&2
  echo "      clone GHDaru/maestro ao lado deste repo, ou aponte com MAESTRO=/caminho" >&2
  exit 2
fi

divergentes=0
sincronizar() {  # <origem-dir> <destino-dir> <rótulo>
  local origem="$1" destino="$2" rotulo="$3"
  [[ -d "$origem" ]] || return 0
  mkdir -p "$destino"
  for item in "$origem"/*; do
    local nome; nome="$(basename "$item")"
    [[ "$nome" == "README.md" ]] && continue
    if [[ $CHECK -eq 1 ]]; then
      if ! diff -rq "$item" "$destino/$nome" >/dev/null 2>&1; then
        echo "≠ $rotulo/$nome divergente do Maestro"
        divergentes=$((divergentes + 1))
      fi
    else
      rm -rf "${destino:?}/$nome"
      cp -r "$item" "$destino/$nome"
    fi
  done
}

sincronizar "$MAESTRO/skills"          "$RAIZ/.claude/skills"   "skills"
sincronizar "$MAESTRO/.claude/commands" "$RAIZ/.claude/commands" "commands"
sincronizar "$MAESTRO/.claude/agents"   "$RAIZ/.claude/agents"   "agents"

if [[ $CHECK -eq 1 ]]; then
  if [[ $divergentes -gt 0 ]]; then
    echo "✗ $divergentes item(ns) fora de sincronia com o Maestro — rode scripts/sync-maestro.sh" >&2
    exit 1
  fi
  echo "✓ skills, comandos e agentes em sincronia com o Maestro"
else
  echo "✓ sincronizado a partir de $MAESTRO ($(cd "$MAESTRO" && git log --oneline -1))"
fi
