# Spec 004 — Subir a infraestrutura do tutor

> **Raia:** infra (gates de reversibilidade obrigatórios) · **Rodada:** 5
> **Branch:** `004-infra-backend` · **Decisor:** Gilsiley Darú

## Intenção

O site está no ar no Vercel. Esta rodada prepara tudo o que depende do repositório para
que o **tutor** entre em operação, e documenta as etapas que exigem credenciais do autor.

## Escopo

### Entra (feito no repositório)

1. **URL do site corrigida** — `SITE` no motor aponta para o domínio do Vercel; afeta
   canônicas, Open Graph e o cabeçalho do Markdown consolidado.
2. **CORS apontando para o Vercel** — default de `ALLOWED_ORIGINS` e `.env.example`.
3. **Widget condicional** — sem `companion_backend` preenchido, o widget **não é
   injetado**. Um botão de chat que não responde é pior do que nenhum botão; e ligar o
   tutor passa a ser uma linha no sumário.
4. **Runbook** (`docs/infra/runbook-deploy.md`) — Neon, Railway, ligação ao site,
   verificação pós-deploy, custos, operação e riscos.
5. **Estudo do protocolo APH persistido** (`estudos/003-…`) — o desenho do fluxo de
   exercício via chat, que é a Rodada 6.

### Não entra (exige credenciais do autor)

- Criar as contas Neon e Railway e preencher as variáveis de ambiente.
- Preencher `companion_backend` com a URL real — é o gate humano que **liga** o tutor.

## Gates de reversibilidade (exigidos pela raia infra)

| Ação | Reversão | Custo da reversão |
|---|---|---|
| Ligar o tutor no site | esvaziar `companion_backend` e publicar | 1 commit; o livro segue íntegro |
| Subir o backend no Railway | derrubar o serviço | nenhum; o site não depende dele |
| Criar o esquema no Neon | tabelas criadas por `CREATE TABLE IF NOT EXISTS`; sem migration destrutiva | — |
| Operação destrutiva futura no banco | branch do Neon antes de operar | restaurar = apontar de volta |

Nenhuma etapa desta rodada é irreversível.

## Critérios de aceite

| # | Critério | Como verificar |
|---|---|---|
| CA-1 | Sem backend, o widget não é injetado | `grep -c companion.js docs/*.html` = 0 |
| CA-2 | Com backend, o widget volta | preencher o sumário e reconstruir |
| CA-3 | A URL canônica é a do Vercel | `grep -c ghdaru.github.io docs/` = 0 |
| CA-4 | CORS aceita o domínio publicado | default de `ALLOWED_ORIGINS` |
| CA-5 | Testes e build seguem verdes | `npm run build` e `pytest` |
