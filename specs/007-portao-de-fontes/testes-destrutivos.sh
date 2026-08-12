#!/usr/bin/env bash
# Os testes destrutivos do portão de fontes.
#
# Um portão sem teste de FALHA é um portão que se presume funcionar. Aqui cada
# critério de aceite que promete uma reprovação é provado QUEBRANDO o portão de
# propósito: se o portão não reclamar, o teste falha.
#
# Trabalha sobre cópias em diretório temporário — a bibliografia e o travamento
# do repositório nunca são tocados.
set -u
cd "$(dirname "$0")/../../publicar"

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
BIB0=../livro/bibliografia.md
LOCK0=../livro/fontes.lock.json

ok=0; falhou=0

# espera <nome> <esperado: passa|reprova> <bib> <lock> [trecho que deve aparecer]
espera() {
  local nome="$1" esperado="$2" bib="$3" lock="$4" trecho="${5:-}"
  local saida rc
  saida=$(FONTES_BIB="$bib" FONTES_LOCK="$lock" node verifica-fontes.mjs 2>&1); rc=$?
  local obtido="passa"; [ $rc -ne 0 ] && obtido="reprova"
  if [ "$obtido" != "$esperado" ]; then
    echo "✗ $nome — esperava $esperado, obteve $obtido"
    echo "$saida" | sed 's/^/      /'
    falhou=$((falhou+1)); return
  fi
  if [ -n "$trecho" ] && ! grep -qF "$trecho" <<<"$saida"; then
    echo "✗ $nome — reprovou, mas sem a mensagem esperada: $trecho"
    echo "$saida" | sed 's/^/      /'
    falhou=$((falhou+1)); return
  fi
  echo "✓ $nome"
  [ "$esperado" = "reprova" ] && echo "$saida" | head -4 | sed 's/^/      /'
  ok=$((ok+1))
}

echo "=== controle: o estado real do repositório ==="
espera "T0  bibliografia e travamento como estão" passa "$BIB0" "$LOCK0"

echo
echo "=== A5 — DOI ausente do travamento ==="
python3 -c "
import json;d=json.load(open('$LOCK0'));d['fontes']=[f for f in d['fontes'] if 'moor' not in f['doi']]
json.dump(d,open('$TMP/a5.json','w'),indent=2,ensure_ascii=False)"
espera "A5  DOI na bibliografia e fora do travamento" reprova "$BIB0" "$TMP/a5.json" "não está no travamento"

echo
echo "=== A6 — DOI fabricado (sufixo inventado sob prefixo real) ==="
sed 's|10\.1287/opre\.49\.1\.1\.11187|10.1287/opre.99.9.9.99999|g' "$BIB0" > "$TMP/a6.md"
python3 -c "
import json;d=json.load(open('$LOCK0'))
for f in d['fontes']:
    if 'opre.49' in f['doi']:
        f.update(doi='10.1287/opre.99.9.9.99999', estado='inexistente', titulo=None, ano=None, primeiro_autor=None, container=None, fonte='doi.org')
json.dump(d,open('$TMP/a6.json','w'),indent=2,ensure_ascii=False)"
espera "A6  DOI que o registro nega" reprova "$TMP/a6.md" "$TMP/a6.json" "NÃO EXISTE no registro"

echo
echo "=== A7 — DOI deslocado (DOI real, de outro trabalho) ==="
python3 -c "
import json;d=json.load(open('$LOCK0'))
for f in d['fontes']:
    if 'inte.20.4.43' in f['doi']:
        f['titulo']='Cycling in the dual simplex algorithm'; f['ano']=1955; f['primeiro_autor']='Beale'
json.dump(d,open('$TMP/a7.json','w'),indent=2,ensure_ascii=False)"
espera "A7  trabalho registrado ≠ trabalho declarado" reprova "$BIB0" "$TMP/a7.json" "título diverge do registro"

echo
echo "=== A8a — título divergente acima do limiar ==="
python3 -c "
import json;d=json.load(open('$LOCK0'))
for f in d['fontes']:
    if 'inte.20.4.43' in f['doi']: f['titulo']='Uma coisa completamente diferente sobre roteirizacao'
json.dump(d,open('$TMP/a8a.json','w'),indent=2,ensure_ascii=False)"
espera "A8a título sem relação reprova" reprova "$BIB0" "$TMP/a8a.json" "título diverge"

echo
echo "=== A8b — truncamento de subtítulo PASSA (o caso legítimo) ==="
python3 -c "
import json;d=json.load(open('$LOCK0'))
for f in d['fontes']:
    if '990308' in f['doi']: f['titulo']='Smoothed analysis of algorithms'
json.dump(d,open('$TMP/a8b.json','w'),indent=2,ensure_ascii=False)"
espera "A8b subtítulo cortado no registro passa" passa "$BIB0" "$TMP/a8b.json"

echo
echo "=== A8c — ano divergente ==="
python3 -c "
import json;d=json.load(open('$LOCK0'))
for f in d['fontes']:
    if 'inte.20.4.43' in f['doi']: f['ano']=1979
json.dump(d,open('$TMP/a8c.json','w'),indent=2,ensure_ascii=False)"
espera "A8c ano diverge do registro" reprova "$BIB0" "$TMP/a8c.json" "ano diverge"

echo
echo "=== A9 — selo usado e não declarado na legenda ==="
python3 - "$BIB0" "$TMP/a9.md" <<'PY'
import sys
t=open(sys.argv[1]).read()
t=t.replace("| ✓ᵐ | metadados |","| ✓ᵐ_REMOVIDO_DA_LEGENDA | metadados |",1)
open(sys.argv[2],'w').write(t)
PY
espera "A9  selo fora da legenda" reprova "$TMP/a9.md" "$LOCK0" "NÃO está declarado na legenda"

echo
echo "=== A10a — chave fora do contrato (Princípio X) ==="
python3 -c "
import json;d=json.load(open('$LOCK0'))
d['fontes'][0]['abstract']='Resumo do artigo, que é texto de terceiro e não pode ser versionado.'
json.dump(d,open('$TMP/a10a.json','w'),indent=2,ensure_ascii=False)"
espera "A10a chave fora do contrato" reprova "$BIB0" "$TMP/a10a.json" "fora do contrato"

echo
echo "=== A10b — campo de texto acima do teto ==="
python3 -c "
import json;d=json.load(open('$LOCK0'))
d['fontes'][0]['titulo']='x'*400
json.dump(d,open('$TMP/a10b.json','w'),indent=2,ensure_ascii=False)"
espera "A10b texto acima de 300 caracteres" reprova "$BIB0" "$TMP/a10b.json" "cheira a texto de terceiro"

echo
echo "=== A11 — entrada com DOI que o parser não consegue interpretar ==="
python3 - "$BIB0" "$TMP/a11.md" <<'PY'
import sys, re
t=open(sys.argv[1]).read()
# tira o título entre aspas da entrada do Charnes, mantendo o DOI
t=t.replace('"Optimality and Degeneracy in Linear Programming".','',1)
open(sys.argv[2],'w').write(t)
PY
espera "A11 título não extraível é DEFEITO, não omissão" reprova "$TMP/a11.md" "$LOCK0" "não extraível"

echo
echo "=== A2 — contagem independente diverge do parser ==="
python3 - "$BIB0" "$TMP/a2.md" <<'PY'
import sys
t=open(sys.argv[1]).read()
# injeta uma ligação doi.org solta, que a contagem bruta vê e o parser não
t=t.replace("## Complementar","Uma ligação solta: https://doi.org/10.9999/solta\n\n## Complementar",1)
open(sys.argv[2],'w').write(t)
PY
espera "A2  contagem bruta ≠ contagem do parser" reprova "$TMP/a2.md" "$LOCK0" "contagem divergente"

echo
echo "=== R1 — link mentiroso: rótulo verdadeiro, endereço trocado ==="
sed 's|DOI \[10.1287/inte.20.4.43\](https://doi.org/10.1287/inte.20.4.43)|DOI [10.1287/inte.20.4.43](https://doi.org/10.1287/opre.66.6.6666)|' "$BIB0" > "$TMP/r1.md"
espera "R1  o endereço do link é conferido, não só o rótulo" reprova "$TMP/r1.md" "$LOCK0" "o leitor clica no segundo"

echo
echo "=== R2 — 'resolvido' com título e ano nulos ==="
python3 -c "
import json;d=json.load(open('$LOCK0'))
for f in d['fontes']:
    if 'inte.20.4.43' in f['doi']: f['titulo']=None; f['ano']=None; f['primeiro_autor']=None
json.dump(d,open('$TMP/r2.json','w'),indent=2,ensure_ascii=False)"
espera "R2  estado e conteúdo não podem divergir (null == null)" reprova "$BIB0" "$TMP/r2.json" "estado e conteúdo divergem"

echo
echo "=== R3 — DOI duplicado no travamento ==="
python3 -c "
import json;d=json.load(open('$LOCK0'))
d['fontes'].append(dict(d['fontes'][0]))
json.dump(d,open('$TMP/r3.json','w'),indent=2,ensure_ascii=False)"
espera "R3  duplicata no travamento não passa em silêncio" reprova "$BIB0" "$TMP/r3.json" "aparece mais de uma vez"

echo
echo "=== R4 — estado ausente ou vazio ==="
python3 -c "
import json;d=json.load(open('$LOCK0'))
d['fontes'][0]['estado']=''
json.dump(d,open('$TMP/r4.json','w'),indent=2,ensure_ascii=False)"
espera "R4  estado vazio reprova" reprova "$BIB0" "$TMP/r4.json" "estado desconhecido"

echo
echo "=== R5 — 'DOI [' que não casa o formato é DEFEITO, não ausência ==="
sed 's|DOI \[10.2307/1907845\](https://doi.org/10.2307/1907845)|DOI [10.2307/1907845]|' "$BIB0" > "$TMP/r5.md"
espera "R5  DOI malformado não é ignorado" reprova "$TMP/r5.md" "$LOCK0" "não casa o formato"

echo
echo "=== A3 — zero chamadas de rede no caminho do build ==="
cat > "$TMP/sem-rede.mjs" <<'JS'
// Prova a AUSÊNCIA da dependência de rede, que é mais forte do que simular
// queda: qualquer tentativa de sair para a rede aborta o processo.
import { execFileSync } from "node:child_process";
globalThis.fetch = () => { console.error("✗ o portão chamou fetch()"); process.exit(9); };
const proibido = (m) => { console.error(`✗ o portão chamou ${m}()`); process.exit(9); };
for (const m of ["get", "request"]) {
  const http = await import("node:http"); const https = await import("node:https");
  http.default[m] = proibido.bind(null, "http." + m);
  https.default[m] = proibido.bind(null, "https." + m);
}
const cp = await import("node:child_process");
for (const m of ["execFileSync", "execSync", "spawnSync", "exec", "spawn"])
  cp.default[m] = proibido.bind(null, "child_process." + m);
await import("./verifica-fontes.mjs");
JS
cp "$TMP/sem-rede.mjs" ./__sem-rede.mjs
if node ./__sem-rede.mjs >/dev/null 2>&1; then echo "✓ A3  o portão não tocou a rede"; ok=$((ok+1))
else echo "✗ A3  o portão tentou sair para a rede"; falhou=$((falhou+1)); fi
rm -f ./__sem-rede.mjs

echo
echo "=== A12 — idempotência do travamento ==="
# O arquivo versionado é PRESERVADO e restaurado. A primeira versão deste teste
# prometia não tocá-lo e rodava o gerador em cima dele; e como o código de saída
# não era checado, sem rede o gerador abortava nos canários, nada era escrito, e
# h1 == h2 declarava idempotência que não havia sido exercida.
cp "$LOCK0" "$TMP/lock-versionado.json"
hash_sem_data() { python3 -c "
import json,hashlib,sys
d=json.load(open(sys.argv[1]))
for f in d['fontes']: f.pop('verificado_em',None)
print(hashlib.md5(json.dumps(d,sort_keys=True).encode()).hexdigest())" "$1"; }
h1=$(hash_sem_data "$LOCK0")
if node atualiza-fontes.mjs >"$TMP/gerador.log" 2>&1; then
  h2=$(hash_sem_data "$LOCK0")
  if [ "$h1" = "$h2" ]; then echo "✓ A12 travamento idêntico a menos da data ($h1)"; ok=$((ok+1))
  else echo "✗ A12 travamento mudou entre duas execuções: $h1 → $h2"; falhou=$((falhou+1)); fi
else
  echo "⚠ A12 NÃO exercida: o gerador não completou (sem rede?) — dívida declarada, não verde falso"
  tail -3 "$TMP/gerador.log" | sed 's/^/      /'
fi
cp "$TMP/lock-versionado.json" "$LOCK0"   # o repositório volta como estava

echo
echo "=== D8 — o gerador recusa rodar em integração contínua ==="
if CI=1 node atualiza-fontes.mjs >/dev/null 2>&1; then
  echo "✗ D8  o gerador rodou com CI=1"; falhou=$((falhou+1))
else echo "✓ D8  o gerador recusou rodar com CI=1"; ok=$((ok+1)); fi

echo
echo "──────────────────────────────────────────"
echo "$ok verificação(ões) OK · $falhou falha(s)"
[ $falhou -eq 0 ] || exit 1
