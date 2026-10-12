#!/usr/bin/env python3
"""gasto.py — cuánto gasta Claude Code, leído de los historiales locales (~/.claude/projects).

Uso:  python3 gasto.py [días]               informe (por omisión, 7 días)
      python3 gasto.py --calibrar [días]   sólo escribe ~/.claude/ajuste/calibracion.json (para el hook)

Separa tres cosas porque cuestan distinto y mezclarlas engaña:
  nuevo   = input_tokens + cache_creation_input_tokens  (lo que entra por primera vez o se reescribe)
  relee   = cache_read_input_tokens                     (el contexto que se vuelve a leer en CADA paso)
  escribe = output_tokens
"""
import json, glob, os, sys, statistics
from collections import defaultdict
from datetime import datetime, timedelta, timezone

CALIBRAR = '--calibrar' in sys.argv
_args = [a for a in sys.argv[1:] if a != '--calibrar']
DIAS = int(_args[0]) if _args else (30 if CALIBRAR else 7)
CORTE = datetime.now(timezone.utc) - timedelta(days=DIAS)
BASE = os.path.expanduser('~/.claude/projects')


def fecha(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))


def medir(path):
    r = {'modelo': '', 'nuevo': 0, 'relee': 0, 'escribe': 0, 'pasos': 0, 'fijo': 0,
         'min': 0.0, 'reescrituras': 0, 'ultimo': None}
    vistos, t0, t1 = set(), None, None
    for linea in open(path, errors='ignore'):
        try:
            m = json.loads(linea)
        except ValueError:
            continue
        ts = m.get('timestamp')
        if ts:
            t0, t1 = t0 or ts, ts
        msg = m.get('message') or {}
        u = msg.get('usage')
        if not u or str(msg.get('model', '')).startswith('<'):
            continue
        mid = msg.get('id')                      # un mensaje puede repetirse en el historial
        if mid in vistos:
            continue
        vistos.add(mid)
        crea = u.get('cache_creation_input_tokens', 0)
        lee = u.get('cache_read_input_tokens', 0)
        nuevo = u.get('input_tokens', 0) + crea
        if not r['pasos']:
            r['fijo'] = nuevo + lee              # contexto con el que arranca, antes de trabajar
        elif crea > 50_000 and lee < crea:
            r['reescrituras'] += 1               # la caché se perdió y se reescribió el contexto entero
        r['modelo'] = r['modelo'] or next((k for k in ('opus', 'sonnet', 'haiku') if k in msg.get('model', '')), msg.get('model', '?'))
        r['nuevo'] += nuevo
        r['relee'] += lee
        r['escribe'] += u.get('output_tokens', 0)
        r['pasos'] += 1
    if t0 and t1:
        r['min'] = round((fecha(t1) - fecha(t0)).total_seconds() / 60, 1)
        r['ultimo'] = fecha(t1)
    return r


def tipo(path):
    try:
        return json.load(open(path[:-6] + '.meta.json')).get('agentType', '?')
    except (OSError, ValueError):
        return '?'


chats = [(p, medir(p)) for p in glob.glob(f'{BASE}/*/*.jsonl')]
chats = [(p, r) for p, r in chats if r['pasos'] and r['ultimo'] and r['ultimo'] >= CORTE]
agentes = [(p, medir(p)) for p in glob.glob(f'{BASE}/*/*/subagents/agent-*.jsonl')]
agentes = [(p, r) for p, r in agentes if r['pasos'] and r['ultimo'] and r['ultimo'] >= CORTE]

if CALIBRAR:
    cal = {}
    por = defaultdict(list)
    for p, r in agentes:
        por[r['modelo']].append(r)
    for mod, rs in por.items():
        cal[mod] = {k: statistics.median(x[k] for x in rs) for k in ('nuevo', 'relee', 'min', 'fijo')}
        cal[mod]['n'] = len(rs)
        cal[mod]['pasados_20min'] = sum(x['min'] > 20 for x in rs)
    destino = os.path.expanduser('~/.claude/ajuste/calibracion.json')
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    json.dump(cal, open(destino, 'w'), indent=1)
    sys.exit(0)

M = lambda x: f'{x / 1e6:.1f}M'
K = lambda x: f'{x / 1e3:.0f}k'
total_c = sum(r['relee'] for _, r in chats)
total_a = sum(r['relee'] for _, r in agentes)
print(f'Últimos {DIAS} días · {len(chats)} chats · {len(agentes)} subagentes')
print(f'Releído: chats {M(total_c)} · subagentes {M(total_a)}\n')

print('SUBAGENTES por modelo y tipo (mediana por agente)')
grupos = defaultdict(list)
for p, r in agentes:
    grupos[(r['modelo'], tipo(p))].append(r)
for (mod, t), rs in sorted(grupos.items(), key=lambda x: -len(x[1])):
    med = lambda k: statistics.median(x[k] for x in rs)
    largos = sum(x['min'] > 20 for x in rs)
    print(f'  {mod:7} {t[:16]:16} n={len(rs):4}  fijo {K(med("fijo")):>5}  pasos {med("pasos"):4.0f}  '
          f'nuevo {K(med("nuevo")):>5}  relee {M(med("relee")):>6}  {med("min"):4.1f} min  >20min: {largos}')

print('\nCHATS que más releen')
for p, r in sorted(chats, key=lambda x: -x[1]['relee'])[:10]:
    nombre = os.path.basename(p)[:8]
    print(f'  {nombre}  {r["modelo"]:7} pasos {r["pasos"]:5}  arranque {K(r["fijo"]):>5}  '
          f'relee {M(r["relee"]):>7}  reescrituras de caché {r["reescrituras"]}')
