# Fase 8 — Velocidad y permisos

- **Menos preguntas de permiso**: si existe el skill `fewer-permission-prompts`, córrelo; si no,
  busca en los historiales las órdenes de lectura que más se aprobaron
  (`grep -ho '"command":"[a-z]* ' ~/.claude/projects/*/*.jsonl | sort | uniq -c | sort -rn | head -30`)
  y propón reglas `Bash(<orden>:*)` sólo para las de lectura (ls, cat, grep, git status, git log…); agrega a
  `~/.claude/settings.json` (global, no al repo del equipo) sólo permisos de **lectura** que la
  persona usa seguido. Respaldo antes. Nunca permisos de escritura amplios.
- **Modo rápido** (`/fast`, si su plan lo tiene): probarlo **un día en un solo chat** y medir la
  velocidad de salida antes y después (tokens de salida ÷ segundos de cada respuesta, del `.jsonl`).
  Se prende y se apaga a mano; la persona decide con el número.
- **Agentes en paralelo** (hasta 4) en vez de uno largo: el reloj baja más que la factura sube.
- **Esfuerzo de razonamiento**: no se baja para ahorrar; si una tarea es mecánica, va a un script o
  al modelo barato, que es lo que de verdad ahorra.
