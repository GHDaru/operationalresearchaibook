# ADR 0002 — Publicar no Vercel, não no GitHub Pages

- **Status:** aceito
- **Data:** 2026-08-01
- **Rodada:** 4 (`specs/003-deploy-vercel`)
- **Decisor:** Gilsiley Darú

## Contexto

A decisão de front ficou em aberto na Rodada 1 ("Vercel ou GitHub Pages"). A Rodada 2
saiu com o workflow de Pages herdado do livro de origem, e o primeiro deploy real
falhou — o que resolveu a dúvida com um fato em vez de uma preferência.

**Diagnóstico do erro.** O build passou por inteiro (testes do tutor, corpus, geração do
site, PDFs) e falhou apenas em `actions/configure-pages@v5`. Essa etapa não cria o site
sozinha: exige que o Pages tenha sido habilitado antes nas configurações do repositório.
E há uma segunda causa, mais determinante: **este repositório é privado**, e o GitHub
Pages em repositório privado exige plano pago (Pro/Team/Enterprise).

Ou seja, manter Pages implicaria uma de duas coisas: assinar um plano, ou tornar o
repositório público — sendo que o repositório carrega o material de trabalho e os
rascunhos, e a decisão da Rodada 1 foi manter o material fora do ar.

## Decisão

**Publicar no Vercel**, seguindo o mesmo padrão já em produção no livro irmão
`GHDaru/protocolos`: `vercel.json` com `buildCommand` apontando para o motor e
`outputDirectory: docs`.

O Vercel publica repositório privado no plano gratuito, e o projeto continua privado
enquanto o site fica público.

## Consequência técnica: PDFs

O build do Vercel não tem Chromium com as bibliotecas de sistema que o Playwright exige,
e a instalação delas requer privilégios que o ambiente não concede. Sem Chromium, não há
PDF.

Em vez de remover o recurso, ele virou **opcional por ambiente**, com a flag `SEM_PDF=1`:

| Ambiente | PDFs | Comportamento |
|---|---|---|
| Local e GitHub Actions | sim | build completo, links de download presentes |
| Vercel (`SEM_PDF=1`) | não | o link de download some junto — nenhum link aponta para arquivo inexistente |

O portão de qualidade acompanha a flag: sem PDFs, ele deixa de exigir os links; com
PDFs, continua exigindo. Os dois modos foram verificados verdes.

*Alternativa descartada:* deixar os links de PDF apontando para arquivos ausentes. Um
livro que oferece download quebrado é pior do que um livro que não oferece download.

## Alternativas avaliadas

| Alternativa | Por que não |
|---|---|
| Assinar GitHub Pro para usar Pages em repo privado | Custo recorrente para um problema que o Vercel resolve de graça |
| Tornar o repositório público | Exporia material de trabalho e rascunhos; contraria a decisão da Rodada 1 |
| Separar um repositório público só para o site gerado | Duplicaria a fonte e criaria sincronização manual — exatamente o tipo de artefato morto que a metodologia rejeita |
| Gerar os PDFs no Vercel com Chromium empacotado | Build frágil e lento por um recurso secundário; a flag resolve com menos risco |

## Consequências

- O workflow de Pages permanece no repositório, sem a etapa de deploy: ele continua
  valendo como **CI** (roda os testes do tutor, regenera o corpus e prova que o site e os
  PDFs constroem) mesmo sem publicar.
- Passa a haver **dois caminhos de build** que precisam ficar verdes. O portão cobre os
  dois, e o `vercel.json` exercita o modo sem PDF a cada deploy.
- Etapa manual única: conectar o repositório ao Vercel uma vez. O `vercel.json` já traz
  toda a configuração.
