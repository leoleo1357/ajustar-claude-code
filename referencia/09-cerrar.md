# Fase 9 — Volver a medir y cerrar

1. Deja pasar uso real (ideal: un día de trabajo; mínimo, unos cuantos agentes nuevos).
2. Corre `gasto.py` y `peso-skills.py` otra vez y compara con `~/.claude/ajuste/antes-<fecha>.txt`:

| Medida | Antes | Después | Meta orientativa |
|---|---|---|---|
| contexto fijo del agente barato | | | ≤ 1/3 del general |
| releído mediano por agente barato | | | −50 % o más |
| minutos medianos por agente; agentes > 20 min | | | casi ninguno |
| agentes caros ejecutando o sin `model` | | | 0 |
| tokens de la lista de skills | | | ≤ 5k |
| arranque de los chats | | | ≤ ~50k |
| reescrituras de caché por chat largo | | | bajando |

3. Cuéntaselo a la persona con los números, en pocas líneas: qué bajó, qué no, qué sigue.
4. Si `~/.claude` está en git: commits chicos por tema (gitignore primero: credenciales, perfiles de
   navegador, historiales, caché, respaldos `.bak*`; después skills, hooks, reglas). Nada de push sin
   que lo pida. Revisa secretos antes de cada commit (`grep -E 'sk-ant-|AKIA|BEGIN .*PRIVATE KEY|ghp_'`).
5. Deja anotado en la memoria qué se hizo, cuándo, y cómo revertir cada cambio (los respaldos).
6. Propón una revisión en 1–2 semanas: los próximos skills a partir (los de arriba de
   `peso-skills.py`) y si el umbral del relevo puede bajar.
