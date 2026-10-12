#!/usr/bin/env python3
"""Hook PreToolUse (matcher «Agent|Task»): frena el agente mal pedido, con el motivo, para que el
chat lo vuelva a lanzar bien. Nunca falla ruidosamente."""
import json, sys
try:
    d = json.load(sys.stdin)
    t = d.get('tool_input') or {}
    modelo = str(t.get('model') or '').lower()
    tipo = t.get('subagent_type') or 'general-purpose'
    texto = (str(t.get('prompt', '')) + ' ' + str(t.get('description', ''))).lower()
    necesita_general = any(p in texto for p in ('navegador', 'browser', 'chrome', 'playwright', 'pantalla', 'mcp', 'captura'))
    motivo = None
    if not modelo and tipo in ('general-purpose', 'ejecutor'):
        motivo = 'Falta `model`: sin él el agente hereda el modelo del chat (el más caro). Decláralo.'
    elif 'opus' in modelo and ('certific' not in texto or tipo == 'ejecutor'):
        motivo = 'El modelo caro sólo decide y certifica. Para ejecutar: `model: "sonnet"`, `subagent_type: "ejecutor"`.'
    elif 'sonnet' in modelo and tipo == 'general-purpose' and not necesita_general:
        motivo = ('Usa `subagent_type: "ejecutor"`: arranca con un tercio del contexto. '
                  'El general sólo si necesita navegador u otro MCP (dilo en el prompt).')
    if motivo:
        print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse',
                                                 'permissionDecision': 'deny',
                                                 'permissionDecisionReason': motivo}}))
except Exception:
    sys.exit(0)
