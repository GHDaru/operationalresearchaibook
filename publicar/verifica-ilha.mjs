// Portão da ilha interativa — o leitor sentando na cadeira.
//
// Existe porque a ilha `regiao-viavel` foi o único artefato publicado do livro
// **sem verificação executável**: a lógica tinha sido corrigida e conferida por
// leitura, e ninguém a havia operado num navegador. O capítulo 08 faz
// afirmações concretas sobre o que ela mostra, e afirmação sem verificação é
// exatamente o que o Princípio XI proíbe.
//
// O que se verifica são as afirmações do CAPÍTULO, não detalhes de aparência:
//
//   1. a ilha monta de verdade (SVG no DOM, console sem erro);
//   2. abre com a segunda restrição DESLIGADA — a narrativa começa com uma faca só;
//   3. abaixo do ótimo a reta CORTA; no ótimo ela ENCOSTA; acima ela PASSA POR CIMA;
//   4. ligar a memória **mata o ótimo anterior**: R$ 1.500 deixa de ser alcançável
//      e o teto cai para R$ 1.100 — que é a virada do capítulo;
//   5. a tabela de vértices acompanha: (0,10) sai, (8,2) e (0,6) entram.
//
// NOTA DE MÉTODO, e ela vale mais do que o portão. A primeira versão deste
// teste procurava a palavra "encosta" no texto inteiro da ilha e acusava três
// falhas. A ilha estava CERTA: o rótulo do controle é "Subir até encostar", e a
// busca casava com a legenda em vez do estado. Diagnosticar antes de corrigir
// evitou "consertar" código correto. Por isso este portão lê a **frase de
// estado** — o último parágrafo —, e não o texto todo.
//
// Requer Playwright e o Chromium do ambiente. Se qualquer um faltar, o portão
// DECLARA que não mediu e sai com 0 — dívida visível é melhor do que falso verde.
import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname } from "node:path";

const AQUI = dirname(fileURLToPath(import.meta.url));
const DOCS = resolve(AQUI, "..", "docs");
// O binário do Chromium mora em lugares diferentes conforme o ambiente: no CI,
// onde `npx playwright install` o coloca no cache padrão; aqui, num caminho
// pré-instalado. Tenta o padrão primeiro e cai para os conhecidos.
const CAMINHOS = ["/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                  "/opt/pw-browsers/chromium/chrome-linux/chrome"].filter(existsSync);

let chromium;
try { ({ chromium } = await import("playwright")); }
catch { console.log("⚠ ilha NÃO verificada: playwright ausente (dívida declarada, não falha)"); process.exit(0); }
if (!existsSync(resolve(DOCS, "08-geometria.html"))) { console.error("✗ ilha: docs/08-geometria.html ausente — rode o build antes"); process.exit(1); }

const TIPOS = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png" };
const servidor = createServer(async (req, res) => {
  try {
    const p = resolve(DOCS, decodeURIComponent(req.url.split("?")[0]).replace(/^\//, "") || "index.html");
    if (!p.startsWith(DOCS)) { res.writeHead(403).end(); return; }
    res.writeHead(200, { "content-type": TIPOS[extname(p)] || "application/octet-stream" }).end(await readFile(p));
  } catch { res.writeHead(404).end(); }
});
await new Promise((ok) => servidor.listen(0, "127.0.0.1", ok));
const PORTA = servidor.address().port;

const falhas = [];
const ok = (cond, msg) => { if (!cond) falhas.push(msg); };
let verificacoes = 0;
const checa = (cond, msg) => { verificacoes++; ok(cond, msg); };

async function abrirNavegador() {
  const tentativas = [undefined, ...CAMINHOS];
  let ultimo;
  for (const executablePath of tentativas) {
    try { return await chromium.launch(executablePath ? { executablePath } : {}); }
    catch (e) { ultimo = e; }
  }
  throw ultimo;
}

let nav;
try { nav = await abrirNavegador(); }
catch (e) {
  // Sem navegador não há o que medir. Declarar a dívida é melhor do que um
  // verde falso — mas ela precisa aparecer, não sumir.
  console.log(`⚠ ilha NÃO verificada: nenhum Chromium disponível (dívida declarada, não falha) — ${String(e).slice(0, 120)}`);
  servidor.close();
  process.exit(0);
}
try {
  const pag = await nav.newPage({ viewport: { width: 1280, height: 900 } });
  const erros = [];
  pag.on("console", (m) => m.type() === "error" && erros.push(m.text()));
  pag.on("pageerror", (e) => erros.push(String(e)));

  await pag.goto(`http://127.0.0.1:${PORTA}/08-geometria.html`, { waitUntil: "networkidle" });
  await pag.waitForTimeout(1200);

  const ilha = pag.locator('[data-viz="regiao-viavel"]');
  checa(await ilha.count() === 1, "ponto de montagem data-viz=regiao-viavel ausente ou duplicado");
  checa((await ilha.innerHTML()).toLowerCase().includes("<svg"), "a ilha não renderizou SVG — não montou");
  checa(erros.length === 0, `console com ${erros.length} erro(s): ${erros.slice(0, 3).join(" | ").slice(0, 200)}`);

  const caixa = ilha.locator('input[type="checkbox"]').first();
  const slider = ilha.locator('input[type="range"]').first();
  checa(await caixa.count() > 0, "sem controle da restrição de memória");
  checa(await slider.count() > 0, "sem controle deslizante da iso-lucro");
  checa(!(await caixa.isChecked()), "a ilha abre com a memória LIGADA — a narrativa do capítulo começa com uma restrição só");

  // A frase de estado é o último parágrafo não vazio do texto da ilha.
  const estado = async (z) => {
    await slider.fill(String(z));
    await pag.waitForTimeout(250);
    const linhas = (await ilha.innerText()).split("\n").map((s) => s.trim()).filter(Boolean);
    return linhas[linhas.length - 1].toLowerCase();
  };
  const vertices = async () => (await ilha.innerText()).replace(/\s+/g, " ");

  // Só a CPU: o capítulo afirma ótimo em (0,10) com R$ 1.500.
  checa((await estado(900)).includes("corta"), "em z=900 a reta deveria CORTAR a região");
  const noOtimo = await estado(1500);
  checa(noOtimo.includes("encosta") && noOtimo.includes("(0, 10)"), "em z=1500 a reta deveria ENCOSTAR em (0, 10)");
  checa(noOtimo.includes("ótimo"), "em z=1500 a ilha deveria nomear o ponto como ótimo");
  checa((await estado(1800)).includes("por cima"), "em z=1800 a reta deveria passar POR CIMA da região");
  checa((await vertices()).includes("(0, 10) · R$ 1.500"), "sem memória, a tabela de vértices deveria trazer (0, 10) · R$ 1.500");

  // A virada do capítulo: ligar a memória mata o ótimo anterior.
  await caixa.check();
  await pag.waitForTimeout(300);
  const antigo = await estado(1500);
  checa(antigo.includes("por cima") && antigo.includes("1.100"),
        "com memória, z=1500 deveria deixar de ser alcançável e o teto cair para R$ 1.100");
  const novo = await estado(1100);
  checa(novo.includes("encosta") && novo.includes("(8, 2)"), "com memória, em z=1100 a reta deveria encostar em (8, 2)");
  const tab = await vertices();
  checa(tab.includes("(8, 2) · R$ 1.100") && tab.includes("(0, 6)"), "com memória, a tabela deveria trazer (8, 2) e (0, 6)");
  checa(!tab.includes("(0, 10)"), "com memória, (0, 10) deveria sair da tabela — a restrição nova o tornou inviável");
} finally {
  await nav.close();
  servidor.close();
}

if (falhas.length) {
  console.error(`✗ ilha interativa: ${falhas.length} falha(s) de ${verificacoes} verificações`);
  falhas.forEach((f) => console.error("   " + f));
  process.exit(1);
}
console.log(`✓ ilha interativa operada em navegador: ${verificacoes} verificações, 0 falhas`);
