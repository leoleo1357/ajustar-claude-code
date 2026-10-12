# Fase 5 — Memoria y CLAUDE.md: lo que se carga en cada mensaje

## 5.1 Qué se carga siempre
- `~/.claude/CLAUDE.md` (global) y los `CLAUDE.md` del repo en que se trabaja.
- Los archivos que esos importan con `@ruta`.
- `~/.claude/projects/<carpeta>/memory/MEMORY.md` — el índice de memoria del proyecto.
Mídelos: `wc -c ~/.claude/CLAUDE.md ~/.claude/projects/*/memory/MEMORY.md | sort -n | tail`.
~4 bytes = 1 token. Un MEMORY.md de 21 KB son ~5k tokens en cada paso de cada chat de ese proyecto.

## 5.2 Acortar un MEMORY.md grande (probado: 21 KB → 4 KB, 0 entradas perdidas)
1. Respaldo: `cp MEMORY.md MEMORY.md.bak-<fecha>-antes-de-acortar`.
2. Un ejecutor clasifica cada renglón en 6–10 temas y crea `indice-<tema>.md` (con frontmatter de
   memoria, `type: reference`) con esos renglones **copiados tal cual**.
3. El nuevo MEMORY.md (≤ 5 KB): arriba «Siempre», ≤ 15 renglones copiados tal cual con lo que pesa en
   cualquier tarea (lo prohibido, los frenos, la forma de responder); debajo, un renglón por
   subíndice con palabras clave suficientes para saber cuándo abrirlo.
4. Verificación: `python3 scripts/cobertura.py MEMORY.md.bak-… indice-*.md` → faltan 0. Y que todo
   archivo de la carpeta siga enlazado desde algún índice.

## 5.3 CLAUDE.md
Mismo criterio que en la fase 0: lo que vale siempre, corto. Procedimientos y casos van a skills.
Si el CLAUDE.md global supera ~6 KB, proponer qué sale a un skill o a `~/.claude/rules/` (y si se
importa con `@`, también se carga siempre: no ahorra).
