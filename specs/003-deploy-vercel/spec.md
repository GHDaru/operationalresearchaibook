# Spec 003 — Publicar o livro (Vercel)

> **Raia:** infra · **Rodada:** 4 · **Branch:** `003-deploy-vercel`
> **Decisor:** Gilsiley Darú · **Status:** aguardando gate humano

## Intenção

Colocar o livro no ar. O primeiro deploy pelo GitHub Pages falhou; esta rodada
diagnostica a causa, escolhe o caminho e deixa o repositório pronto para publicar.

## Diagnóstico (causa antes da correção)

O build passou por inteiro — testes do tutor, corpus, site, PDFs — e falhou apenas em
`actions/configure-pages@v5`. Duas causas, ambas reais:

1. O Pages não estava habilitado nas configurações do repositório. A etapa não cria o
   site sozinha (o próprio comentário herdado do workflow já avisava disso).
2. **Mais determinante:** o repositório é privado, e Pages em repositório privado exige
   plano pago. Habilitar não resolveria sem assinar um plano ou abrir o repositório.

## Decisão

Publicar no **Vercel** (ADR 0002), pelo padrão já em produção no livro irmão
`GHDaru/protocolos`: publica repositório privado no plano gratuito.

## Escopo

- `vercel.json` com o build do motor e `outputDirectory: docs`.
- Flag `SEM_PDF=1`: o Vercel não tem Chromium, então o site sai sem PDFs **e sem os
  links** para eles — nenhum download quebrado.
- O workflow de Pages vira **CI**: continua rodando testes, corpus, site e PDFs (agora
  também no branch da rodada), sem publicar.
- ADR 0002 registrando decisão, alternativas e consequências.

## Critérios de aceite

| # | Critério | Como verificar |
|---|---|---|
| CA-1 | O build completo (com PDFs) continua verde | `npm run build` |
| CA-2 | O build do Vercel fica verde | `SEM_PDF=1 node build.mjs && SEM_PDF=1 node verifica-capitulos.mjs` |
| CA-3 | Sem PDFs, nenhum link aponta para PDF | `grep -c 'href="pdf/'` = 0 nas páginas |
| CA-4 | Com PDFs, os links voltam | build completo mantém os links |
| CA-5 | A CI cobre os dois caminhos | etapa `SEM_PDF` no workflow |

## Etapa manual (única, do autor)

Conectar o repositório ao Vercel — importar o projeto e confirmar. O `vercel.json` já
traz toda a configuração; nenhuma variável de ambiente é necessária nesta fase (o tutor
ainda não está no ar).
