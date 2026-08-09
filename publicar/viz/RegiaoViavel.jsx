// Ilha interativa do capítulo 08 — a região viável e a reta de iso-lucro.
//
// Substitui o GeoGebra da aula por um objeto que mora no livro. O leitor faz
// três coisas, e são exatamente as três da narrativa do capítulo:
//
//   1. liga e desliga a restrição de memória, e VÊ a região encolher;
//   2. sobe e desce a reta de iso-lucro, e vê onde ela toca por último;
//   3. lê, a cada instante, qual vértice está ganhando.
//
// Progressive enhancement: sem JavaScript, o Markdown em volta traz a mesma
// tabela de vértices e a mesma conclusão. A ilha acelera o entendimento; não é
// pré-requisito dele.

import React, { useMemo, useState } from "react";

const L1 = 100; // lucro do Tipo 1
const L2 = 150; // lucro do Tipo 2

const CPU = { a1: 1, a2: 1, b: 10, rotulo: "CPUs: x₁ + x₂ ≤ 10", cor: "#5c86c4" };
const MEM = { a1: 1, a2: 2, b: 12, rotulo: "Pentes: x₁ + 2x₂ ≤ 12", cor: "#7bb972" };

// Geometria do desenho
const W = 560, H = 420, M = { t: 18, r: 18, b: 38, l: 46 };
const XMAX = 13, YMAX = 11;
const sx = (x) => M.l + (x / XMAX) * (W - M.l - M.r);
const sy = (y) => H - M.b - (y / YMAX) * (H - M.t - M.b);

const lucro = (p) => L1 * p[0] + L2 * p[1];
const quase = (a, b) => Math.abs(a - b) < 1e-9;

function verticesDe(restricoes) {
  // Não-negatividade entra como restrição de verdade — é o que faz os eixos
  // serem duas retas como as outras.
  const todas = [...restricoes, { a1: -1, a2: 0, b: 0 }, { a1: 0, a2: -1, b: 0 }];
  const pts = [];
  for (let i = 0; i < todas.length; i++)
    for (let j = i + 1; j < todas.length; j++) {
      const r = todas[i], s = todas[j];
      const det = r.a1 * s.a2 - r.a2 * s.a1;
      if (Math.abs(det) < 1e-12) continue;
      const x = (r.b * s.a2 - r.a2 * s.b) / det;
      const y = (r.a1 * s.b - r.b * s.a1) / det;
      if (!todas.every((t) => t.a1 * x + t.a2 * y <= t.b + 1e-9)) continue;
      if (!pts.some((p) => quase(p[0], x) && quase(p[1], y))) pts.push([x + 0, y + 0]);
    }
  // Ordena pelo ângulo em torno do centroide, para o polígono fechar certo.
  const cx = pts.reduce((a, p) => a + p[0], 0) / pts.length;
  const cy = pts.reduce((a, p) => a + p[1], 0) / pts.length;
  return pts.sort((p, q) => Math.atan2(p[1] - cy, p[0] - cx) - Math.atan2(q[1] - cy, q[0] - cx));
}

// A reta L1·x + L2·y = nivel, recortada na área do gráfico.
function retaIso(nivel) {
  const pts = [];
  const yEm0 = nivel / L2;
  const xEm0 = nivel / L1;
  if (yEm0 >= 0 && yEm0 <= YMAX) pts.push([0, yEm0]);
  if (xEm0 >= 0 && xEm0 <= XMAX) pts.push([xEm0, 0]);
  const yEmXmax = (nivel - L1 * XMAX) / L2;
  if (yEmXmax >= 0 && yEmXmax <= YMAX) pts.push([XMAX, yEmXmax]);
  const xEmYmax = (nivel - L2 * YMAX) / L1;
  if (xEmYmax >= 0 && xEmYmax <= XMAX) pts.push([xEmYmax, YMAX]);
  return pts.slice(0, 2);
}

export default function RegiaoViavel() {
  // Abre com a memória DESLIGADA de propósito: o capítulo conduz o leitor a
  // subir a reta com a CPU sozinha, ver o ótimo em (0,10), e só então mandar
  // "ligue a restrição". Abrir ligado inverteria a narrativa.
  const [comMemoria, setComMemoria] = useState(false);
  const [nivel, setNivel] = useState(600);

  const restricoes = comMemoria ? [CPU, MEM] : [CPU];
  const verts = useMemo(() => verticesDe(restricoes), [comMemoria]);
  const otimo = useMemo(
    () => verts.reduce((a, p) => (lucro(p) > lucro(a) ? p : a), verts[0]),
    [verts]
  );
  const maxLucro = lucro(otimo);
  const toca = nivel <= maxLucro + 1e-9;
  const iso = retaIso(nivel);

  // ATENÇÃO: "encostar" é passar pelo ÚLTIMO valor possível, não coincidir com
  // um vértice qualquer. Uma reta que passa por um vértice não-ótimo ainda CORTA
  // a região — em (0,6), com nível 900, ela também passa por (9,0), que é viável.
  // A versão anterior testava a coincidência com vértice e escrevia "encosta",
  // desmentindo a definição do capítulo justo onde o leitor a está formando.
  const noOtimo = quase(nivel, maxLucro);

  return (
    <div className="viz-regiao">
      <div className="viz-controles">
        <label className="viz-check">
          <input type="checkbox" checked={comMemoria}
                 onChange={(e) => setComMemoria(e.target.checked)} />
          <span>Restrição de memória (12 pentes)</span>
        </label>
        <label className="viz-slider">
          <span>Iso-lucro: <b>R$ {nivel.toLocaleString("pt-BR")}</b></span>
          <input type="range" min="0" max="1800" step="50" value={nivel}
                 onChange={(e) => setNivel(Number(e.target.value))} />
        </label>
        <button className="viz-botao" onClick={() => setNivel(maxLucro)}>
          Subir até encostar
        </button>
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} role="img"
           aria-label={`Região viável do problema de montagem. ${comMemoria
             ? "Com as restrições de CPU e de memória, o vértice ótimo é 8 do Tipo 1 e 2 do Tipo 2, com lucro de 1100 reais."
             : "Só com a restrição de CPU, o vértice ótimo é 10 do Tipo 2, com lucro de 1500 reais."}`}>
        {/* grade */}
        {Array.from({ length: XMAX + 1 }, (_, i) => (
          <line key={`gx${i}`} x1={sx(i)} y1={sy(0)} x2={sx(i)} y2={sy(YMAX)}
                stroke="currentColor" opacity=".08" />
        ))}
        {Array.from({ length: YMAX + 1 }, (_, i) => (
          <line key={`gy${i}`} x1={sx(0)} y1={sy(i)} x2={sx(XMAX)} y2={sy(i)}
                stroke="currentColor" opacity=".08" />
        ))}

        {/* região viável */}
        <polygon points={verts.map((p) => `${sx(p[0])},${sy(p[1])}`).join(" ")}
                 fill="#5c86c4" fillOpacity=".18" stroke="#5c86c4" strokeWidth="2" />

        {/* retas das restrições */}
        {restricoes.map((r) => {
          const p1 = [0, r.b / r.a2];
          const p2 = [r.b / r.a1, 0];
          return (
            <line key={r.rotulo} x1={sx(p1[0])} y1={sy(p1[1])} x2={sx(p2[0])} y2={sy(p2[1])}
                  stroke={r.cor} strokeWidth="2.5" opacity=".9" />
          );
        })}

        {/* reta de iso-lucro */}
        {iso.length === 2 && (
          <line x1={sx(iso[0][0])} y1={sy(iso[0][1])} x2={sx(iso[1][0])} y2={sy(iso[1][1])}
                stroke="#e0a24a" strokeWidth="3" strokeDasharray={toca ? "0" : "7 6"} />
        )}

        {/* Gradiente. O texto afirma que ele é PERPENDICULAR à reta de iso-lucro,
            então a seta precisa sair perpendicular NA TELA — e as escalas dos dois
            eixos são diferentes. Desenhar (100,150) em coordenadas de dados daria
            ~82°, e o leitor veria o capítulo se contradizer. Por isso a direção é
            calculada no espaço da tela. */}
        {(() => {
          const kx = (W - M.l - M.r) / XMAX, ky = (H - M.t - M.b) / YMAX;
          // direção ao longo da iso-lucro, em dados: (L2, -L1) → em tela:
          const dx = L2 * kx, dy = L1 * ky;
          const n = Math.hypot(dx, dy);
          // girar 90° na tela: (dx,dy) → (dy,-dx), que aponta para cima e à direita
          const ux = dy / n, uy = -dx / n;
          const x0 = sx(9.3), y0 = sy(7.6), C = 66;
          const x1 = x0 + ux * C, y1 = y0 + uy * C;
          const px = -uy, py = ux; // perpendicular à seta, para a ponta
          return (
            <g stroke="#e0a24a" strokeWidth="2" fill="none" opacity=".9">
              <line x1={x0} y1={y0} x2={x1} y2={y1} />
              <polygon fill="#e0a24a" stroke="none"
                points={`${x1},${y1} ${x1 - ux * 13 + px * 6},${y1 - uy * 13 + py * 6} ${x1 - ux * 13 - px * 6},${y1 - uy * 13 - py * 6}`} />
            </g>
          );
        })()}
        <text x={sx(6.4)} y={sy(7.2)} fontSize="12" fill="#e0a24a">∇ = (100, 150)</text>

        {/* vértices */}
        {verts.map((p) => {
          const eOtimo = quase(lucro(p), maxLucro);
          return (
            <g key={`${p[0]}-${p[1]}`}>
              <circle cx={sx(p[0])} cy={sy(p[1])} r={eOtimo ? 7 : 5}
                      fill={eOtimo ? "#e0a24a" : "#8fb2e6"} />
              <text x={sx(p[0]) + 9} y={sy(p[1]) - 7} fontSize="12" fill="currentColor">
                ({p[0]}, {p[1]}) · R$ {lucro(p).toLocaleString("pt-BR")}
              </text>
            </g>
          );
        })}

        {/* eixos */}
        <line x1={sx(0)} y1={sy(0)} x2={sx(XMAX)} y2={sy(0)} stroke="currentColor" strokeWidth="1.5" />
        <line x1={sx(0)} y1={sy(0)} x2={sx(0)} y2={sy(YMAX)} stroke="currentColor" strokeWidth="1.5" />
        <text x={sx(XMAX) - 4} y={sy(0) + 24} fontSize="13" fill="currentColor" textAnchor="end">
          x₁ — Tipo 1
        </text>
        <text x={sx(0) - 34} y={sy(YMAX) + 4} fontSize="13" fill="currentColor">x₂</text>
      </svg>

      <p className="viz-leitura">
        {toca ? (
          noOtimo ? (
            <>A reta <b>encosta</b> em ({otimo[0]}, {otimo[1]}) e não corta mais a região.{" "}
              <b>É o último valor possível — este é o ótimo.</b></>
          ) : (
            <>A reta <b>corta</b> a região: todo ponto dela sobre o azul rende R$ {nivel.toLocaleString("pt-BR")}. Continue subindo.</>
          )
        ) : (
          <>A reta <b>passou por cima</b> da região viável. Não existe plano que renda R$ {nivel.toLocaleString("pt-BR")} —
            o teto é R$ {maxLucro.toLocaleString("pt-BR")}.</>
        )}
      </p>
    </div>
  );
}
