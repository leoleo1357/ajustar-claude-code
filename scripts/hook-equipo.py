#!/usr/bin/env python3
"""Hook UserPromptSubmit: recuerda la política de equipo y el gasto real en cada mensaje.
Versión larga la primera vez de cada chat; después, una línea. Nunca falla ruidosamente."""
import json, os, re, sys
try:
    d = json.load(sys.stdin)
    cifras = ''
    try:
        cal = json.load(open(os.path.expanduser('~/.claude/ajuste/calibracion.json')))
        cifras = ' · '.join(f"{m}: {v['nuevo'] / 1e3:.0f}k nuevos + {v['relee'] / 1e6:.1f}M releídos, {v['min']:.1f} min"
                            for m, v in cal.items() if v.get('n', 0) >= 3)
    except Exception:
        pass
    sid = re.sub(r'[^\w-]', '', str(d.get('session_id', 'x'))) or 'x'
    marca = os.path.expanduser(f'~/.claude/ajuste/visto-{sid}')
    if os.path.exists(marca):
        txt = ('EQUIPO: decide tú (nadie/script/barato/ejecutor); `model` siempre explícito; '
               'Sonnet con `subagent_type: "ejecutor"`. ' + (f'Gasto real: {cifras}' if cifras else ''))
    else:
        os.makedirs(os.path.dirname(marca), exist_ok=True)
        open(marca, 'w').close()
        txt = ('EQUIPO (política en ~/.claude/skills/ajustar-claude-code/referencia/03-equipo.md). Antes de trabajar, '
               'decide el equipo por lo que el pedido ES, no por sus palabras:\n'
               '• nadie: respuesta, lectura, arreglo chico → lo haces tú.\n'
               '• script: contar, medir, comparar → bash/python, cero agentes.\n'
               '• haiku: mecánico con criterio mínimo.\n'
               '• sonnet: SIEMPRE `subagent_type: "ejecutor"`; una parte acotada (≲15 min), en paralelo, máx. 4 vivos.\n'
               '• el modelo caro: decide y certifica; NUNCA ejecuta. Todo Agent lleva `model` explícito.\n'
               'Si lanzas, di en una línea cuántos, de qué modelo y cuánto sale. '
               + (f'Gasto real por agente: {cifras}.' if cifras else ''))
    print(json.dumps({'hookSpecificOutput': {'hookEventName': 'UserPromptSubmit', 'additionalContext': txt}}))
except Exception:
    sys.exit(0)
