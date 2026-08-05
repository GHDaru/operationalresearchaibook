// Portão: o espelho de capacidades do widget (COMPANION_CAPS em build.mjs) tem
// de bater com a fonte da verdade (chat-companion/backend/capabilities.py).
//
// Existe porque a duplicação já divergiu uma vez: a capacidade "exercicios" foi
// adicionada ao backend e esquecida no espelho — e o check que havia (procurar
// "companion.js" no HTML) media um proxy, não o fato. Este mede o fato.
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const build = readFileSync(resolve(AQUI, "build.mjs"), "utf8");
const py = readFileSync(resolve(AQUI, "../chat-companion/backend/capabilities.py"), "utf8");

const doEspelho = [...build.matchAll(/\{\s*chave:\s*"([^"]+)",\s*rotulo:\s*"([^"]+)",\s*libera:\s*(\d+)\s*\}/g)]
  .map(([, chave, rotulo, libera]) => `${chave}|${rotulo}|${libera}`);
const daFonte = [...py.matchAll(/\{"chave":\s*"([^"]+)",\s*"rotulo":\s*"([^"]+)",\s*"libera":\s*(\d+)/g)]
  .map(([, chave, rotulo, libera]) => `${chave}|${rotulo}|${libera}`);

const falhas = [];
if (!daFonte.length) falhas.push("não consegui ler capabilities.py — o portão não está medindo nada");
for (const c of daFonte) if (!doEspelho.includes(c)) falhas.push(`no backend e não no espelho: ${c}`);
for (const c of doEspelho) if (!daFonte.includes(c)) falhas.push(`no espelho e não no backend: ${c}`);

if (falhas.length) {
  console.error("✗ espelho de capacidades divergente:");
  falhas.forEach((f) => console.error("   " + f));
  console.error("   corrija COMPANION_CAPS em publicar/build.mjs para bater com capabilities.py");
  process.exit(1);
}
console.log(`✓ espelho de capacidades em sincronia (${daFonte.length} capacidades)`);
