# Fase 3 — Política de equipo y hooks (que se cumpla sola)

## 3.1 La política (va resumida en el hook; completa aquí)
| Papel | Quién | Hace | No hace |
|---|---|---|---|
| decide | el chat (modelo caro) | entiende, parte el trabajo, escribe el contrato, integra, commitea | lo que un barato hace igual en paralelo |
| ejecuta | modelo intermedio como `ejecutor` | una parte acotada: un área, un grupo de archivos | lanzar agentes, commits, tocar fuera de su parte |
| mecánico | un script; si no alcanza, el modelo más barato | contar, medir, comparar, renombrar | decidir |
| certifica | un agente que NO construyó (la persona elige el modelo; para producción o dinero, el mejor) | verifica contra la API o los archivos; puede reprobar | arreglar |

| El pedido es… | Equipo por omisión |
|---|---|
| una respuesta, una lectura, un arreglo de una línea | nadie: lo hace el chat |
| arreglar o construir en un área | 1 ejecutor + el chat integra + 1 certificador |
| varias áreas | 1 ejecutor por área en paralelo (2–4) + 1 certificador |
| investigar o documentar | 1–3 ejecutores por fuente; contar lo hace un script |

Reglas duras: **`model` siempre explícito** (sin él hereda el del chat, el más caro); **tope 4
agentes vivos**; **ninguno pasa de 20 minutos** (se parte en tandas); **antes de lanzar se dice en
una línea cuántos, de qué modelo y cuánto sale** (con las medianas reales).

## 3.2 Cómo se escribe un encargo (aquí se gana o se pierde)
Un ejecutor que tiene que adivinar da el doble de pasos. Cada encargo lleva, textual:
1. el objetivo en una frase y por qué;
2. **qué archivos puede tocar**, con nombre («nada más»); un archivo nunca está en dos encargos;
3. el contrato compartido si hay varias partes (firmas, formatos);
4. cómo se comprueba que quedó (comando, prueba, medida);
5. lo prohibido (push, borrar, producción, instalar);
6. «tienes 20 minutos; si no terminas, entrega lo que tengas y di qué faltó»;
7. qué devolver: conclusiones en ≤15 líneas, nunca volcados.
Si el trabajo toca un repositorio donde otros trabajan: un `git worktree` propio por agente.

## 3.3 Los hooks (en `~/.claude/settings.json` → `"hooks"`; respaldo antes)
| Evento | Script | Qué hace |
|---|---|---|
| `UserPromptSubmit` | `scripts/hook-equipo.py` | recuerda la política en cada mensaje (larga la primera vez, una línea después) con el gasto real |
| `PreToolUse`, matcher `Agent\|Task` | `scripts/hook-vigilante.py` | frena con el motivo: sin `model`, el caro ejecutando, el general sin necesitar navegador |
| `UserPromptSubmit` | `scripts/hook-relevo.py` | avisa cuando el chat pasa el umbral (250k) |
| `SessionEnd` | `python3 scripts/gasto.py --calibrar` | rehace `~/.claude/ajuste/calibracion.json` (medianas de 30 días) |

Va dentro de la clave `"hooks": { … }` de `~/.claude/settings.json`:
```json
"hooks": {
  "UserPromptSubmit": [{"hooks": [
    {"type": "command", "command": "python3 ~/.claude/skills/ajustar-claude-code/scripts/hook-equipo.py"},
    {"type": "command", "command": "python3 ~/.claude/skills/ajustar-claude-code/scripts/hook-relevo.py"}]}],
  "PreToolUse": [{"matcher": "Agent|Task", "hooks": [
    {"type": "command", "command": "python3 ~/.claude/skills/ajustar-claude-code/scripts/hook-vigilante.py"}]}],
  "SessionEnd": [{"hooks": [
    {"type": "command", "command": "python3 ~/.claude/skills/ajustar-claude-code/scripts/gasto.py --calibrar", "timeout": 60}]}]
}
```
**Fusionar, no pisar:** si `settings.json` ya tiene `"hooks"` o ya hay entradas en ese evento, se
agregan estos objetos a las listas existentes (leer el JSON, sumar, validar con
`python3 -m json.tool settings.json`). En Windows, `python3` puede llamarse `python` o `py -3`.
`--calibrar` lee todos los historiales de 30 días: en una máquina cargada tarda ~10 s (por eso el
`timeout`). Prueba de cada uno, a mano:
```bash
echo '{"tool_input":{"prompt":"x"}}' | python3 .../hook-vigilante.py      # debe frenar: falta model
echo '{"tool_input":{"prompt":"x","model":"sonnet","subagent_type":"ejecutor"}}' | python3 .../hook-vigilante.py   # nada
```
Ajusta a la instalación: nombres de modelo en el vigilante (`opus`, `sonnet`) y palabras que piden
navegador. Los hooks hacen poco, no tocan la red y ante cualquier error salen callados.
Las marcas `visto-<sesión>` de `hook-equipo.py` quedan en `~/.claude/ajuste/`; se pueden borrar
cuando se quiera.
