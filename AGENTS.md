# Instruções para agentes de IA

Antes de alterar a monografia ou qualquer documento do TCC (`Monografia/` e cópias da monografia), leia e siga [`.claude/skills/revisao-tcc/SKILL.md`](.claude/skills/revisao-tcc/SKILL.md).

Resumo:
- Nunca sobrescreva o original; trabalhe numa cópia ` - revisado`.
- Escreva em tom acadêmico e impessoal, sem linguagem de documentação interna.
- Toda alteração gera um `<documento> - alteracoes.md` com **Antes/Depois** e o trecho alterado destacado com `<mark>`. O MD cobre só o último pedido; num refinamento, atualize só a entrada afetada.
- Use `.claude/skills/revisao-tcc/scripts/gerar_md_alteracoes.py` para gerar o MD.
