// Ilha interativa — "Que conexão é esta?"
//
// O leitor lê uma afirmação e escolhe se a relação entre as duas partes é de
// CAUSA E EFEITO ("se… então…") ou de PRÉ-REQUISITO ("para… é necessário…").
// O feedback é imediato e explica o porquê — prática formativa intercalada no
// texto, que é a forma de estudo com maior efeito medido (ver o Guia Editorial).
//
// Sem JS, o Markdown em volta da ilha mostra os mesmos itens como lista estática.
import React, { useState } from "react";

const ITENS = [
  {
    frase: "Se a equipe recebe mais pedidos do que consegue produzir, então o prazo de entrega aumenta.",
    resposta: "causa",
    porque:
      "A primeira parte PRODUZ a segunda por si só. Nada precisa ser decidido ou providenciado: dado o excesso de pedidos, o prazo aumenta como consequência.",
  },
  {
    frase: "Para reduzir o prazo de entrega, é necessário conhecer onde o trabalho fica parado.",
    resposta: "prerequisito",
    porque:
      "A segunda parte é uma CONDIÇÃO para a primeira, não uma consequência dela. Conhecer o gargalo não reduz prazo nenhum sozinho — apenas torna a redução possível.",
  },
  {
    frase: "Se o vendedor promete uma data que a fábrica não confirmou, então o cliente é informado de um prazo que ninguém garantiu.",
    resposta: "causa",
    porque:
      "Consequência direta e automática: a promessa não confirmada já é, por si, um prazo sem garantia chegando ao cliente.",
  },
  {
    frase: "Para que a fábrica confirme datas, é necessário que ela tenha visibilidade da fila de produção.",
    resposta: "prerequisito",
    porque:
      "Visibilidade não confirma data alguma automaticamente — é o que precisa existir ANTES para que a confirmação seja possível.",
  },
  {
    frase: "Se o cliente recebe um prazo que não é cumprido, então a confiança dele na empresa diminui.",
    resposta: "causa",
    porque:
      "Efeito produzido pelo descumprimento. Note que a conexão depende de uma premissa — que o cliente se importa com o prazo —, e é isso que o capítulo 04 vai examinar.",
  },
];

const ROTULOS = {
  causa: "Causa e efeito",
  prerequisito: "Pré-requisito",
};

export default function ClassificarConexao() {
  const [i, setI] = useState(0);
  const [escolha, setEscolha] = useState(null);
  const [acertos, setAcertos] = useState(0);
  const [fim, setFim] = useState(false);

  const item = ITENS[i];
  const respondido = escolha !== null;
  const acertou = respondido && escolha === item.resposta;

  function responder(valor) {
    if (respondido) return;
    setEscolha(valor);
    if (valor === item.resposta) setAcertos((n) => n + 1);
  }

  function avancar() {
    if (i + 1 >= ITENS.length) return setFim(true);
    setI(i + 1);
    setEscolha(null);
  }

  function recomeçar() {
    setI(0);
    setEscolha(null);
    setAcertos(0);
    setFim(false);
  }

  if (fim) {
    return (
      <div className="ilha">
        <p className="ilha-kicker">Exercício · Que conexão é esta?</p>
        <p className="ilha-placar">
          <strong>
            {acertos} de {ITENS.length}
          </strong>{" "}
          {acertos === ITENS.length
            ? "— você distingue as duas conexões com segurança. Siga para o capítulo 03."
            : "— vale reler a distinção antes de seguir: causa e efeito PRODUZ; pré-requisito HABILITA."}
        </p>
        <button className="ilha-btn" onClick={recomeçar}>
          Refazer o exercício
        </button>
      </div>
    );
  }

  return (
    <div className="ilha">
      <p className="ilha-kicker">
        Exercício · Que conexão é esta? <span className="ilha-passo">{i + 1}/{ITENS.length}</span>
      </p>
      <p className="ilha-frase">{item.frase}</p>
      <div className="ilha-opcoes">
        {Object.entries(ROTULOS).map(([valor, rotulo]) => {
          let classe = "ilha-op";
          if (respondido) {
            if (valor === item.resposta) classe += " ilha-op-certa";
            else if (valor === escolha) classe += " ilha-op-errada";
          }
          return (
            <button key={valor} className={classe} onClick={() => responder(valor)} disabled={respondido}>
              {rotulo}
            </button>
          );
        })}
      </div>
      {respondido && (
        <div className={acertou ? "ilha-fb ilha-fb-ok" : "ilha-fb ilha-fb-nao"}>
          <p>
            <strong>{acertou ? "Isso." : `É ${ROTULOS[item.resposta].toLowerCase()}.`}</strong> {item.porque}
          </p>
          <button className="ilha-btn" onClick={avancar}>
            {i + 1 >= ITENS.length ? "Ver o resultado" : "Próxima"}
          </button>
        </div>
      )}
    </div>
  );
}
