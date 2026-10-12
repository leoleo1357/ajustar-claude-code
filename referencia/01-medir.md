# Fase 1 — Medir (obligatoria, antes de cambiar nada)

## 1.1 Dónde están los datos
- `~/.claude/projects/<carpeta>/<sesión>.jsonl` — cada chat; cada respuesta trae `message.usage`.
- `~/.claude/projects/<carpeta>/<sesión>/subagents/agent-*.jsonl` — cada subagente; al lado, `agent-*.meta.json` con su tipo.
- En `usage`: `input_tokens` + `cache_creation_input_tokens` = **nuevo**; `cache_read_input_tokens` = **releído**; `output_tokens` = escrito.
  Lo releído cuesta ~10 % del precio de lo nuevo, pero en volumen es cientos o miles de veces más: es lo que infla.
- Un mismo mensaje puede aparecer repetido en el historial: se cuenta una vez por `message.id`.

## 1.2 Los dos scripts
```bash
python3 ~/.claude/skills/ajustar-claude-code/scripts/gasto.py 7        # chats y subagentes, 7 días
python3 ~/.claude/skills/ajustar-claude-code/scripts/peso-skills.py 7  # qué cuesta cada skill
```

## 1.3 Qué buscar (y contárselo a la persona en 6–8 líneas)
| Señal | Qué significa | Fase que lo ataca |
|---|---|---|
| subagentes `general-purpose` con «fijo» ~45k | cada agente arrastra herramientas que no usa | 2 |
| agentes con el modelo caro ejecutando, o sin `model` (heredan el del chat) | el más caro haciendo trabajo barato | 3 |
| muchos agentes de más de 20 min o más de ~50 pasos | tareas demasiado grandes | 3 |
| la lista de skills pesa más de ~5k tokens | descripciones largas o skills que no usa | 4 |
| un SKILL.md de más de ~8 KB que se carga seguido | se relee entero en cada paso posterior | 4 |
| «arranque» de los chats por encima de ~50k | CLAUDE.md, memoria o skills muy pesados | 4–5 |
| chats con miles de pasos y cientos de millones releídos | chats que nunca se cierran | 6–7 |
| muchas «reescrituras de caché» | cambio de modelo, pausas largas, reanudar chats viejos | 6 |

Los modelos que el script no reconoce (nuevos o de otra familia) salen con su nombre completo: está
bien. Anota los nombres reales que usa la persona, porque los hooks de la fase 3 se ajustan a ellos.

## 1.4 Guardar la foto
Guarda la salida en `~/.claude/ajuste/antes-<fecha>.txt`. En la fase 9 se compara contra ella.
