// Ponto de entrada das ilhas interativas. Encontra cada <div data-viz="..."> nas
// páginas geradas e monta o componente React correspondente. Progressive
// enhancement: sem JS, a página mostra o conteúdo estático do Markdown (fallback).
import React from "react";
import { createRoot } from "react-dom/client";
import RegiaoViavel from "./RegiaoViavel.jsx";

const COMPONENTES = {
  "regiao-viavel": RegiaoViavel,
};

for (const el of document.querySelectorAll("[data-viz]")) {
  const Comp = COMPONENTES[el.getAttribute("data-viz")];
  if (Comp) {
    el.innerHTML = "";
    createRoot(el).render(<Comp />);
  }
}
