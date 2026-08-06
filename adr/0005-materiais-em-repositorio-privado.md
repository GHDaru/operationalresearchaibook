# ADR 0005 — Materiais de terceiros em repositório privado separado

**Data:** 2026-08-06 · **Status:** aceito

## Contexto

Em 2026-08-06, dois livros didáticos em formato PDF (cerca de 28 MB somados) foram
commitados na branch padrão deste repositório, que é **público**. A intenção declarada era
tornar o repositório privado para acomodá-los.

Três fatos tornaram essa saída inadequada:

1. **Tornar privado não retrai o que já foi público.** O commit já havia sido servido pelo
   GitHub. Fechar o repositório reduz exposição futura, não a passada.
2. **O repositório é o veículo de publicação do livro.** O merge na branch padrão é o que
   publica o site. Fechá-lo trocaria a publicação da obra por armazenamento de arquivo.
3. **Contradiz o Princípio X**, ratificado no mesmo dia: livros-texto de terceiros não são
   reproduzidos neste repositório.

Havia ainda um custo técnico: 28 MB de binário em histórico Git são clonados por todos,
para sempre, e a informação útil das obras — estrutura e paginação — cabe em uma tabela.

## Decisão

**O repositório do handbook permanece público. Materiais de terceiros vivem fora dele, em
repositório privado separado.**

1. Os dois arquivos foram **purgados do histórico** com `git filter-repo`, seguido de
   *force-push* da branch padrão e da branch de trabalho. O `.git` caiu de 27 MB para 1,3 MB.
2. Antes da purga, foi extraído o que é **legítimo versionar**: ficha bibliográfica, estrutura
   declarada de cada obra e a tabela de correspondência com as vagas do
   [Mapa do handbook](../livro/mapa-do-handbook.md). Está em
   [`livro/bibliografia.md`](../livro/bibliografia.md), edição 0.2 do livro.
3. Os arquivos passam a viver em repositório privado do autor — o mesmo padrão já usado no
   livro *Teoria das Restrições*, que mantém seus materiais em repositório privado próprio.
4. `materiais/` continua no `.gitignore` (exceto o `README.md`), para que trabalhar com os
   arquivos localmente não crie risco de commit acidental.

## Alternativas avaliadas

| Alternativa | Por que não |
|---|---|
| Tornar o repositório privado | Quebra a publicação do livro, não retrai a exposição passada, e contraria o Princípio X |
| Remover os arquivos num commit novo, sem reescrever | Os blobs continuam alcançáveis por identificador no histórico: é meia solução que *parece* completa |
| Manter os PDFs e aceitar o risco | Redistribuição de obra protegida em repositório público. Não é uma opção |
| Git LFS | Resolve o peso do clone, não o direito autoral. O problema não era tamanho |

## Consequências

**Boas.** O handbook segue público e publicável. O clone volta a ser leve. A informação
realmente útil das obras — o mapa de correspondência — está versionada e é o que o aluno
precisa para transitar entre o handbook e o livro impresso.

**Ruins, e assumidas.** A reescrita de histórico **mudou os identificadores de todos os
commits**. Qualquer clone anterior a 2026-08-06 diverge e precisa ser refeito. Além disso, o
GitHub pode reter objetos inalcançáveis em cache por algum tempo; a purga elimina o acesso
pela árvore, não garante remoção imediata de toda cópia já servida. **A exposição passada é
tratada como ocorrida**, não como desfeita.

**Regra que fica.** Antes de qualquer commit, a pergunta do
[`materiais/README.md`](../materiais/README.md) vale como teste: *se um advogado da editora
abrir este repositório, ele encontra referências ao livro dela ou pedaços do livro dela?*
Se for a segunda, não commite.
