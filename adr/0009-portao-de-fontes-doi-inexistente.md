# ADR 0009 — O que o portão de fontes faz com um DOI que não resolve

**Data:** 2026-08-12 · **Status:** aceito na branch, **pendente de ratificação do autor no gate
de merge** · **Rodada:** 007 · **Consulta:** especialista de arquitetura, recomendação integral
revisada e verificada antes de gravar

## Contexto

A rodada 007 cria `publicar/verifica-fontes.mjs`, portão do `npm run build` que confere os
identificadores de objeto digital (DOI, *Digital Object Identifier*) declarados em
`livro/bibliografia.md`. São **12 DOIs** em **31 obras distintas** — 39% (a contagem está na spec, com o comando).

O objetivo declarado: **um DOI inventado quebra o build.** O motivo é um incidente real — na
rodada 004 uma URL de vídeo foi **inventada**, e só foi descoberta por acidente, ao tentar
abri-la.

A tensão registrada na spec: reprovar quando o DOI não resolve pega o inventado, mas pode punir
obra real não indexada; avisar sem reprovar preserva o segundo caso e **esvazia o portão**. O
exemplo com que eu havia justificado a segunda posição — Hoffman, *NBS Report* 2974, 1953 —
**não tem DOI**, e portanto nunca esteve ao alcance do portão. O guardião do processo apontou
isso: a exceção foi aberta por um caso que não a exige.

## Diagnóstico: o enquadramento das duas posições estava errado

As duas posições compartilhavam uma premissa falsa — **que "resolver um DOI" é pergunta feita a
uma base bibliográfica.** Não é.

- **Crossref e OpenAlex são índices de metadados**, com cobertura parcial por construção. Um DOI
  registrado na DataCite, na mEDRA ou na JaLC legitimamente **não está no Crossref**. Perguntar
  existência a eles produz falso negativo por desenho.
- **A existência de um DOI é decidida pelo *Handle System*, via `doi.org`.** Se o resolvedor diz
  que o *handle* não existe, não existe esse DOI — não é lacuna de cobertura, é ausência de
  registro.

Com a distinção, "obra real, DOI real, não indexada" deixa de ser exceção e vira **estado normal
e aprovável**. Não precisa de allowlist. Precisa de um terceiro estado no travamento.

E o caso que sobra — *o DOI não existe no registro* — **não tem instância legítima**, porque o
autor sempre pode remover o DOI da entrada. Hoffman é a prova disso, não a exceção a isso.

### A assimetria explorável, e onde ela está

| Modo de fabricação | Exemplo | Existência pega? | Metadados pegam? |
|---|---|---|---|
| Prefixo inventado | `10.99999/xyz` | **sim** | sim |
| **Sufixo inventado sob prefixo real** | `10.1287/opre.99.9.9.99999` | **sim** | sim |
| **DOI deslocado** — DOI real de outro trabalho | — | **não, resolve verde** | **sim, e só ele** |

O prefixo serve para **diagnóstico e mensagem**, não para veredito. A assimetria decisiva é
dupla: **existência** pega os dois primeiros modos, **correspondência de metadados** pega o
terceiro. Um portão que só pergunta "resolve?" fica verde apontando para o artigo errado — falha
pior que a atual, porque vem carimbada.

### T0 — o contrato foi verificado antes de a decisão ser gravada

O especialista não conseguiu confirmar os endpoints no ambiente dele. Foram confirmados aqui, e a
saída está colada em [`verificacao.md`](../specs/007-portao-de-fontes/verificacao.md):

```
10.1287/inte.20.4.43        responseCode = 1     existe
10.1287/opre.99.9.9.99999   responseCode = 100   NÃO existe  ← prefixo real, sufixo inventado
10.99999/xyz                responseCode = 100   NÃO existe
prefixo 10.1287 → Institute for Operations Research and the Management Sciences (INFORMS)
```

A degradação prevista para o caso de o `handles` não servir **não foi necessária**.

## Decisão

### D1 — DOI que não existe no registro **reprova**. Sem allowlist.

O portão sai diferente de zero e nomeia entrada, DOI, prefixo e registrante do prefixo.

**O escape legítimo não é exceção: é remoção do identificador.** Se o DOI não existe, o reparo é
apagá-lo e manter a obra com o localizador que ela de fato tem — URL, ISBN, número de relatório,
identificador do arXiv. Custa uma linha, é honesto, e **não serve para contrabandear
identificador fabricado**.

Não haverá `fontes.allow.json`, nem campo `ignorar`, nem comentário mágico no Markdown.

### D2 — Três estados no travamento, decididos por perguntas distintas

O gerador (`publicar/atualiza-fontes.mjs`, com rede, sob demanda) pergunta em cascata:

1. **Existe?** — `GET https://doi.org/api/handles/{doi}` · `responseCode 1` existe, `100` não.
2. **De quem é o prefixo?** — `GET https://api.crossref.org/prefixes/10.NNNN`, só para a mensagem.
3. **Que trabalho é?** — Crossref `/works/{doi}`; falhando, OpenAlex `/works/doi:{doi}`.

| Estado | Condição | Portão |
|---|---|---|
| `resolvido` | existe **e** metadados obtidos | **passa** |
| `registrado-sem-metadados` | existe, nenhum índice tem metadado | **passa**, e imprime a lista |
| `inexistente` | o registro diz que não existe | **reprova** |
| `indeterminado` | timeout, 5xx, DNS, proxy | **nunca é gravado** (D5) |

`registrado-sem-metadados` é o que a allowlist protegeria, obtido sem abrir buraco: a aprovação
vem de **prova positiva de existência**, não da palavra de quem escreveu a entrada.

### D3 — O portão compara o trabalho declarado com o registrado, não só a existência

Para cada DOI `resolvido`, o travamento guarda **título**, **ano** e **sobrenome do primeiro
autor**.

| Campo | Divergência | Por quê |
|---|---|---|
| **título** | **reprova** | Critério medido: contenção antes de bigramas, limiar 0,78 |
| **ano** | **reprova** | É exato, e é o erro de citação mais comum |
| **primeiro autor** | **avisa** | A ordem de autoria diverge entre índices com frequência suficiente para que exigir posição gerasse falso vermelho — e falso vermelho crônico ensina a desligar o portão |

> **Esta tabela corrige o ADR, não o código.** A primeira versão escrevia "divergência
> **reprova**" para os três campos, enquanto o portão sempre avisou no autor. A revisão
> independente apontou que era o **ADR** — o documento que vai à ratificação — que estava errado.
> O comportamento do código é o defensável; a promessa é que estava larga.

E **`resolvido` exige conteúdo**: título ou ano nulos reprovam. Sem isso, `null == null` virava
acordo tácito e um travamento vazio passava contado como "12 resolvidos".

O **título** é comparado com o critério medido nesta rodada — **contenção antes de bigramas,
limiar 0,78** — e não com o 0,70 que o plano trazia sem procedência. A calibração está em
[`calibracao.json`](../specs/007-portao-de-fontes/calibracao.json): 12 pares legítimos em 1,000,
melhor impostor em 0,560, janela de 0,440.

> **Por que contenção antes de similaridade.** A divergência legítima tem forma: o registro
> **corta o subtítulo**. Spielman & Teng é declarado com o subtítulo inteiro e registrado como
> *"Smoothed analysis of algorithms"* — 0,517 por bigramas, abaixo do melhor impostor (0,560,
> dois títulos diferentes que compartilham *"simplex method"*). **Nenhum limiar único separa
> os dois.** Truncamento produz contenção; jargão compartilhado, não.

### D4 — Ausência no travamento **reprova**. O silêncio nunca é verde.

Todo DOI da bibliografia tem entrada no travamento; sem entrada, falha. O portão **sempre**
imprime a contagem — `N na bibliografia · N no travamento · N resolvidos · N sem metadados ·
N inexistentes`. Portão que não diz o que verificou é portão que se engana sem perceber.

### D5 — Defesas do gerador contra o falso verde por indisponibilidade

1. **"Não encontrei" ≠ "não consegui perguntar".** `indeterminado` **não é gravado**.
2. **Canários.** Antes de gravar, o gerador resolve DOIs de controle fixos, sabidamente
   existentes. **Canário falhou, gerador aborta sem escrever.** É a resposta direta a "as bases
   caíram" — o cenário que de fato ocorreu nesta sessão, com o Semantic Scholar em `429`.
3. **Limiar de degradação em massa.** Mais de 20% das entradas, ou mais de duas, virando
   `inexistente` numa execução aborta. Doze fabricações simultâneas não acontecem; queda de
   serviço acontece.
4. **Fusão, nunca truncamento.** Entrada já `resolvido` não é rebaixada por consulta que falhou;
   rebaixar exige `--repor` explícito, e o diff passa pelo olho do autor.

`verificado_em` acima de 180 dias **avisa**, não reprova: reprovar por calendário quebraria o
build de *commits* antigos e trocaria determinismo por relógio.

### D6 — O portão verifica identificadores. Nunca escreve selo.

Somente leitura; jamais edita `bibliografia.md`. O travamento **não tem campo de selo**, para que
a promoção nem seja expressável. Ver [ADR 0010](0010-a-semantica-do-selo.md).

### D7 — Princípio X aplicado mecanicamente, não prometido

Lista **fechada** de chaves por entrada: `doi`, `estado`, `prefixo`, `registrante`, `titulo`,
`primeiro_autor`, `ano`, `container`, `fonte`, `verificado_em`. Todo o resto da resposta da
interface de programação de aplicações (API) é **descartado na leitura** — com destaque para
`abstract`, `reference`, `license` e `funder`.

E vira teste: o portão **reprova** se o travamento contiver chave fora da lista ou campo de texto
acima de 300 caracteres. Título, autor, ano e periódico são metadado bibliográfico, que o
Princípio X autoriza versionar; resumo é conteúdo de terceiro, e não entra.

### D8 — O gerador não roda no build, e não roda em integração contínua (CI)

`npm run build` encadeia apenas o portão. O gerador é `npm run fontes`, e **recusa execução
quando `CI` está definido**. O portão entra cedo, para falhar antes de gerar site:

```
verifica-espelho → verifica-fontes → verifica-referencias → build → verifica-capitulos
                 → verifica-exercicios → verifica-otimos
```

Sem isso, o caminho de menor esforço diante de um build vermelho vira "regenerar o travamento no
CI até ficar verde" — o mesmo esvaziamento da allowlist, por outra porta.

### D9 — A rede é falada por `curl`, não pelo `fetch` do Node

Diagnosticado nesta rodada: o `fetch` nativo do Node **não honra a variável de proxy do
ambiente**; a conexão cai no proxy sem a semântica de `CONNECT` e volta `403 Host not in
allowlist`. O `curl` usa o mesmo proxy e o mesmo pacote de certificados, e passa.

Nada de TLS foi afrouxado e nenhuma variável foi removida — trocou-se de cliente. Em ambiente sem
proxy os dois funcionam, então a escolha não custa portabilidade.

## Alternativas avaliadas

**A1 — Avisar sem reprovar.** *Rejeitada.* Falha no objetivo da rodada. Aviso em build verde é
aviso que ninguém lê depois da terceira vez; e o caso que a justificava está atendido por
`registrado-sem-metadados`. O incidente 004 foi descoberto **por acidente**: o repositório já tem
evidência de que aviso passivo não protege.

**A2 — Reprovar com allowlist datada e justificada.** *Rejeitada.* (a) O único caso legítimo já é
coberto por `registrado-sem-metadados`; (b) o caso restante tem reparo trivial — apagar o DOI;
(c) uma allowlist chaveada pelo identificador que **não pôde ser verificado** é artefato
**autocertificador**: a única evidência que carrega é a palavra de quem a escreveu — precisamente
o que o Princípio III recusa. Seria o esconderijo, com aparência de rigor.

**A3 — Verificar só o prefixo.** *Rejeitada.* Não pega o modo mais comum (sufixo inventado) nem o
mais perigoso (DOI deslocado). Aprovaria `10.1287/qualquer-coisa`.

**A4 — Reprovar também em `registrado-sem-metadados`.** *Rejeitada.* Puniria obra real: a agência
registradora não ser o Crossref é fato comum, não sintoma. Transformaria cobertura de índice em
critério editorial.

**A5 — Consultar em tempo de build, sem travamento.** *Rejeitada por restrição.* Quebra o
determinismo e faz o build depender de indisponibilidade alheia. O parecer do especialista **é a
demonstração**: o ambiente dele bloqueava `doi.org` e `api.crossref.org`.

**A6 — Quarentena com prazo.** *Não implementada; registrada como fallback.* Se algum dia
aparecer DOI que existe e cujo registro não resolve, a forma aceitável é estado `quarentena`
**dentro** do travamento, com `motivo`, `data` e `evidencia_url` obrigatórios, **validade de 90
dias** e **teto rígido de 2 entradas** no repositório inteiro. Concedida só pelo autor, no diff.
Enquanto o caso real não aparecer, não se constrói: **mecanismo de exceção sem instância é
convite**.

## Consequências

**Boas**

- DOI inventado quebra o build — e, por D3, DOI **deslocado** também, que é o modo que ninguém
  detecta lendo.
- "Existe e não está indexado" passa **sem exceção nenhuma**, por prova positiva. A tensão
  original se dissolve em vez de ser negociada.
- Não há superfície de esconderijo: nenhum arquivo, campo ou comentário diz "confie em mim".
- O build permanece determinístico e offline.
- A mensagem de erro **ensina**: nomeia o registrante do prefixo e diz que o sufixo é o suspeito.

**Custosas, e assumidas**

- **Este portão fecha o buraco de DOI, e não o de URL.** O incidente da rodada 004 foi uma **URL
  de vídeo inventada**, e ela **continuaria passando**. Está dito na spec, no `HISTORICO.md` e no
  `ROADMAP.md`: o item "Portão de URL externa" **continua aberto**, e é provavelmente mais urgente
  do que este. Portão que cria confiança maior que sua cobertura é pior do que portão nenhum.
- **Cobertura declarada:** 12 DOIs em 31 obras — **61% da bibliografia continua sendo afirmação
  humana** — livros, páginas institucionais e identificadores
  do arXiv ficam fora.
- Depende de serviço externo **no momento da geração**. D5 transforma indisponibilidade em aborto
  ruidoso, não a elimina.
- A extração de ano e autor acopla o portão à forma da prosa. Mitigação: **reprova se não
  conseguir interpretar** uma entrada que tem DOI — falha por ignorância é falha, nunca aprovação.
- Trabalho manual novo: entrada com DOI exige `npm run fontes` e leitura do diff. Com 12 é barato;
  a 200, este ADR precisa ser revisto.
