# Colocar o backend no ar

> **Estado em 2026-08-12.** O backend **funciona** — provado de ponta a ponta nesta máquina — e
> **não está publicado**. O site em `https://ghdaru.github.io/operationalresearchaibook/` está no
> ar com o widget de chat **inerte**, porque `companion_backend` está vazio no
> `publicar/sumario.json`.

## O que já foi provado

Rodado localmente, com o adaptador `echo` (sem rede, sem chave):

```
POST /session       200
POST /chat          200   5 capacidades ativas no capítulo 7
GET  /exercicios    200   4 exercícios · rubrica NÃO vazou
GET  /history       200
GET  /progresso     200
```

O gating por capítulo funciona e a rubrica de correção não chega ao cliente — que são as duas
coisas que o handbook não pode errar.

## O que falta, e de quem é cada parte

| # | Passo | De quem |
|---|---|---|
| 1 | Criar a chave do modelo (gratuita) | **autor** — é conta |
| 2 | Criar o banco (gratuito) | **autor** — é conta |
| 3 | Publicar o serviço | **autor** — é conta |
| 4 | Ligar o site ao backend | agente, com a URL do passo 3 |
| 5 | Provar que o laço fecha no navegador | agente |

**Nenhum segredo entra no repositório.** As chaves vivem só nas variáveis de ambiente do serviço
(constituição: *credenciais só em `.env`, fora do versionamento*).

---

## Passo 1 — chave do modelo (custo zero)

1. Entre em <https://build.nvidia.com> e gere uma chave (`nvapi-…`).
2. Guarde. Ela vai virar a variável `OPENAI_API_KEY` no passo 3.

A trilha padrão do handbook é **custo zero** por princípio. O endpoint da NVIDIA é
OpenAI-compatível, então trocar de provedor depois é mudar duas variáveis, não código.

## Passo 2 — banco (custo zero)

1. Entre em <https://neon.tech>, crie um projeto.
2. Copie a *connection string* (**Connection Details → URI**). Formato:
   `postgresql://USUARIO:SENHA@ep-xxxx.REGIAO.aws.neon.tech/neondb?sslmode=require`

> **Sem esta variável o backend sobe e funciona**, guardando tudo em memória — e perde tudo a
> cada reinício. Para o tutor, isso é aceitável em teste. **Para a prova, não**: nota que some no
> primeiro *deploy* não é nota.

## Passo 3 — publicar o serviço

O repositório já traz `Procfile`, `runtime.txt` e `railway.json` — a configuração do
[Railway](https://railway.app) está pronta e o *healthcheck* aponta para `/health`.

1. **New Project → Deploy from GitHub repo** → `GHDaru/operationalresearchaibook`.
2. **Root Directory:** `chat-companion/backend`
3. **Variables** — cole exatamente estas:

```
LLM_ADAPTER=openai
OPENAI_BASE_URL=https://integrate.api.nvidia.com/v1
OPENAI_API_KEY=<a chave do passo 1>
LLM_MODEL=nvidia/nemotron-3-ultra-550b-a55b
DATABASE_URL=<a string do passo 2>
ALLOWED_ORIGINS=https://ghdaru.github.io,http://localhost:8000
ADMIN_TOKEN=<invente uma senha longa; é o que protege GET /suggestions>
```

> **A origem do Pages é o HOST, sem o caminho do repositório** — `https://ghdaru.github.io`, e
> **não** `https://ghdaru.github.io/operationalresearchaibook`. O navegador manda só o host no
> cabeçalho `Origin`; incluir o caminho faz o CORS falhar com uma mensagem que não explica nada.
> É o erro mais comum deste passo.

4. Ao fim, o Railway dá uma URL do tipo `https://algo.up.railway.app`. **Confira antes de seguir:**

```bash
curl -sS https://SUA-URL.up.railway.app/health
# esperado: {"ok":true,"llm":"openai","store":"postgres"}
```

Se vier `"llm":"echo"`, a chave não chegou. Se vier `"store":"memory"`, o `DATABASE_URL` não
chegou. O `/health` responde as duas perguntas de uma vez, de propósito.

## Passo 4 — ligar o site ao backend

Me passe a URL. Eu acrescento ao `publicar/sumario.json`:

```json
"companion_backend": "https://SUA-URL.up.railway.app"
```

O merge na `main` republica o site, e o widget deixa de ser inerte.

## Passo 5 — provar que fecha

Não basta o `/health` responder. A prova é o laço no navegador: abrir um capítulo publicado,
mandar uma pergunta, e a resposta voltar sem erro de CORS no console. Isso eu faço e colo a
saída — é o mesmo padrão do `verifica-ilha.mjs`.

---

## O que este documento NÃO cobre

- **A prova com nota.** O backend hoje serve o **tutor** e a **correção de exercício**, que são
  anônimos. A prova identificada por matrícula é outra coisa: exige decisão sobre retenção,
  aviso ao aluno e **emenda à constituição**, que hoje promete anonimato. Rodada própria.
- **Domínio próprio e custo em escala.** As camadas gratuitas do Neon e do Railway têm limite.
  Enquanto for turma, cabem; a conta muda com a audiência.
