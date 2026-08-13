#!/usr/bin/env bash
# Prova que o portão de maturidade FALHA quando deve — critério A3 da spec 009.
# "Prove, não declare": um portão que nunca foi visto vermelho não é portão.
#
# ARMADILHA JÁ PAGA, na primeira execução deste arquivo: a restauração usava
# `git checkout --`, que devolve os arquivos ao HEAD. Como o portão sob teste
# ainda não estava commitado, o primeiro caso APAGOU o que ele testava, e os
# três seguintes acusaram "o portão passou verde" contra um portão que nem
# existia mais no disco. Um teste destrutivo não pode supor que o estado sob
# teste é o estado commitado — a cópia é de arquivo, não de revisão.
set -u
cd "$(dirname "$0")/../.."
ALVOS=(publicar/sumario.json)
TMP="$(mktemp -d)"
salvar() { for a in "${ALVOS[@]}"; do cp "$a" "$TMP/$(basename "$a")"; done; }
restaura() { for a in "${ALVOS[@]}"; do cp "$TMP/$(basename "$a")" "$a"; done; }
limpar() { restaura; rm -rf "$TMP"; }
trap limpar EXIT
salvar

ok=0; falhou=0
caso() { # nome, trecho esperado no erro
  if SEM_PDF=1 node publicar/verifica-capitulos.mjs 2>&1 | grep -qF "$2"; then
    echo "  ✓ $1"; ok=$((ok+1))
  else
    echo "  ✗ $1 — o portão passou verde"; falhou=$((falhou+1))
  fi
  restaura
}

echo "portão de maturidade — testes destrutivos"

# 1. Selo ausente no sumário.
python3 -c "
p='publicar/sumario.json'; s=open(p,encoding='utf-8').read()
open(p,'w',encoding='utf-8').write(s.replace('      \"maturidade\": \"verificado\",\n','',1))"
caso "capítulo sem maturidade declarada" 'maturidade "(ausente)"'

# 2. Valor fora da escada.
python3 -c "
p='publicar/sumario.json'; s=open(p,encoding='utf-8').read()
open(p,'w',encoding='utf-8').write(s.replace('\"maturidade\": \"verificado\"','\"maturidade\": \"quase-la\"',1))"
caso "maturidade fora da escada" 'maturidade "quase-la"'

# 3. O falso verde que importa: o sumário passa a dizer 🟡 e a PÁGINA continua
#    exibindo ✅, porque ninguém reconstruiu. É o modo pelo qual um selo se
#    torna decorativo sem que nenhum arquivo pareça errado.
python3 -c "
p='publicar/sumario.json'; s=open(p,encoding='utf-8').read()
open(p,'w',encoding='utf-8').write(s.replace('\"maturidade\": \"verificado\"','\"maturidade\": \"v0\"',1))"
caso "sumário e página divergem" "exibe outro selo"

# 4. A razão da ADR 0013 D2: 🟡 acima do teto de 3 por ✅. Aqui todos viram 🟡,
#    o que zera o denominador — então o caso real é 4 🟡 e 1 ✅ (teto 3).
python3 -c "
p='publicar/sumario.json'; s=open(p,encoding='utf-8').read()
open(p,'w',encoding='utf-8').write(s.replace('\"maturidade\": \"verificado\"','\"maturidade\": \"v0\"',3))"
caso "🟡 acima do teto por ✅" "ADR 0013, D2"

echo "  → $ok passaram, $falhou falharam"
[ "$falhou" -eq 0 ]
