#!/usr/bin/env python3
"""Hook UserPromptSubmit: avisa cuando el chat pasó el umbral de contexto y conviene el relevo.
Umbral: variable RELEVO_UMBRAL (por omisión 250000). Nunca falla ruidosamente."""
import json, os, sys
try:
    d = json.load(sys.stdin)
    umbral = int(os.environ.get('RELEVO_UMBRAL', '250000'))
    ultimo = 0
    with open(d['transcript_path'], errors='ignore') as f:
        for linea in f:
            if '"usage"' not in linea:
                continue
            try:
                m = json.loads(linea)
            except ValueError:
                continue
            if m.get('isSidechain'):
                continue
            u = (m.get('message') or {}).get('usage') or {}
            ultimo = u.get('input_tokens', 0) + u.get('cache_read_input_tokens', 0) + u.get('cache_creation_input_tokens', 0)
    if ultimo > umbral:
        txt = (f'RELEVO: este chat ya carga {ultimo / 1000:.0f}k tokens en cada paso (umbral {umbral / 1000:.0f}k). '
               'Al terminar este pedido, propón el relevo a un chat nuevo (referencia/07-relevo.md del skill ajustar-claude-code).')
        print(json.dumps({'hookSpecificOutput': {'hookEventName': 'UserPromptSubmit', 'additionalContext': txt}}))
except Exception:
    sys.exit(0)
