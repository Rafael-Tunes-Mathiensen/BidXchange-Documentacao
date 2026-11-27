---
name: revisao-tcc
description: Use ao alterar a monografia ou qualquer documento de TCC deste repositório (.docx em Monografia/ ou cópias dela). Define como editar sem perder o original, o tom acadêmico esperado e o arquivo Markdown de Antes/Depois, com marca-texto, que deve acompanhar toda alteração.
---

# Revisão de documentos do TCC

Siga estas regras sempre que alterar a monografia ou outro documento do TCC, sem esperar que o usuário peça.

## 1. Nunca sobrescreva o original

- Trabalhe numa cópia com o sufixo ` - revisado` (por exemplo, `Monografia_BidXchange - revisado.docx`).
- Se a cópia revisada já existir, continue nela.
- Antes de cada rodada de edição, guarde uma cópia da versão atual fora do repositório. É ela que serve de "Antes" no MD.

## 2. Como editar o .docx

- Use `python-docx` e altere o texto **dentro dos runs** existentes, para manter negrito, estilo e hyperlinks.
- Um parágrafo pode ter hyperlinks, por exemplo para execuções de CI. Não reconstrua esse parágrafo a partir de `paragraph.text`, porque os links se perdem. Edite run por run.
- Ao mudar números (totais de testes, requisitos, casos), procure o mesmo número no documento todo: Resumo, Abstract, capítulos de testes e resultados, quadros de objetivos e Conclusão. Atualize tudo de forma consistente.
- Não invente fatos. Se uma reescrita depende de algo que você não sabe, escreva a versão mais provável e coloque o ponto em "Pontos para confirmação" (seção 4).

## 3. Tom acadêmico

Reescreva de forma impessoal e acadêmica os trechos com cara de documentação interna da equipe. Exemplos do que evitar:

- "Segundo os autores", quando os autores são quem escreve a monografia. A expressão vale só para citar outros autores, como em "Gefen, Karahanna e Straub (2003)... segundo os autores".
- Quem guarda arquivos e onde (o nome de um integrante, "no celular de...") e intenções pessoais ("não pretende apagar").
- "A documentação não informa...", "não está especificado...". Escreva o fato de forma direta ou leve o ponto para confirmação.
- Caminhos de arquivo (`Analise/arquivo.md`, `.agents/check.py`), hashes completos de commit, jargão como "gate" e "artefatos anexos". Hash curto e número de execução de CI são aceitáveis.
- Coloquialismos como "usuários de verdade".

## 4. Arquivo Markdown de Antes/Depois (obrigatório)

Toda alteração gera um `.md` salvo ao lado do documento editado, com o nome `<nome do documento> - alteracoes.md`.

**Escopo:**
- O MD cobre **só o último pedido** de alteração, e não o histórico inteiro da conversa. Um pedido novo de revisão gera um MD novo, que substitui o anterior.
- **Exceção:** se o usuário só refina uma alteração que já está no MD (por exemplo, ajustar uma frase já reescrita), atualize **apenas aquela entrada** no MD existente e mantenha as demais. O "Antes" continua sendo o texto original, e o "Depois" é a versão final.

**Formato:**
- Título com o assunto do pedido e a frase "Os trechos alterados estão destacados com marca-texto."
- Para cada parágrafo alterado:
  - `## <título da seção>`
  - `**Antes:**` e o parágrafo completo original
  - `**Depois:**` e o parágrafo completo novo
  - `---`
- Destaque com `<mark>…</mark>` **só o trecho que mudou**, nas duas versões. Os textos costumam ser quase idênticos, e o destaque mostra a diferença de imediato. Agrupe o destaque em trechos contínuos e não marque palavra por palavra.
- Em quadros e tabelas, mostre as linhas afetadas em tabela Markdown, com as colunas antes e depois.
- No fim, `## Pontos para confirmação dos autores`, com as suposições que você fez (omita a seção se não houver nenhuma).

**Script de apoio:** `scripts/gerar_md_alteracoes.py` compara duas versões do `.docx` e gera esse MD automaticamente:

```
python .claude/skills/revisao-tcc/scripts/gerar_md_alteracoes.py "antes.docx" "depois.docx" "saida - alteracoes.md" --titulo "Assunto do pedido"
```

Revise o resultado e acrescente à mão os pontos para confirmação.

Exemplo de entrada:

```markdown
## RESUMO

**Antes:**

… Dos 39 casos documentados para os requisitos, <mark>27 foram aprovados.</mark> A verificação técnica …

**Depois:**

… Dos 39 casos documentados para os requisitos, <mark>27 tiveram o cenário aprovado; quanto à cobertura, 20 cobrem integralmente o requisito, 9 parcialmente e 10 ficaram sem cobertura.</mark> A verificação técnica …
```

## 5. Ao terminar

Diga ao usuário quais seções mudaram, onde está o `.docx` revisado e o `.md`, e quais pontos ele precisa confirmar.
