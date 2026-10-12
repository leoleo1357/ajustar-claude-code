# ajustar-claude-code

Un skill para Claude Code que deja tu instalación **más rápida y más barata sin bajar la calidad**.
Te conoce, mide tu gasto real de tokens, revisa tus skills y tu memoria, instala un agente
«ejecutor» liviano, una política de equipo con hooks, el relevo de chats pesados y las reglas de
caché, y al final vuelve a medir. Nada se cambia sin tu «sí», y antes de tocar hace respaldo.

## Instalar
```bash
git clone https://github.com/leoleo1357/ajustar-claude-code ~/.claude/skills/ajustar-claude-code
```
Abre un chat nuevo de Claude Code y dile: **«ajusta mi Claude»**.

## Qué necesitas
- Claude Code con historiales en `~/.claude/projects` (vienen por omisión).
- `python3` (los scripts no usan librerías externas).
- Una o dos horas para las fases 0–4, que son las que más ahorran.

## Qué lee y qué escribe
Lee (sólo en tu máquina): `~/.claude/CLAUDE.md`, tus skills, tu memoria y los historiales de
`~/.claude/projects` para medir. Escribe, siempre con tu permiso y con respaldo antes:
`~/.claude/agents/ejecutor.md`, hooks en `~/.claude/settings.json`, y los cambios que apruebes en
tus skills, memoria y CLAUDE.md. Sus mediciones van a `~/.claude/ajuste/`.

## Qué no hace
No baja de modelo, no borra nada tuyo sin permiso, no sube código y no manda tus datos a ningún lado:
todo se lee y se mide en tu máquina.
