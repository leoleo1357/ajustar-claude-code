#!/usr/bin/env python3
"""peso-skills.py — qué cuesta cada skill instalado.

Uso:  python3 peso-skills.py [días]      (por omisión, 7)

Dos costos distintos:
  1. LA LISTA: la descripción de cada skill va en el contexto de TODOS los chats y subagentes,
     se use o no. Se mide en caracteres (~4 por token).
  2. LA CARGA: cuando un skill se invoca, su SKILL.md entero entra al chat y se relee en cada paso
     que sigue. Se estima como tokens del SKILL.md × pasos que quedaban en ese chat.
"""
import glob, json, os, re, sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

DIAS = int(sys.argv[1]) if len(sys.argv) > 1 else 7
CORTE = datetime.now(timezone.utc) - timedelta(days=DIAS)
CASA = os.path.expanduser('~/.claude')
RAICES = [f'{CASA}/skills', os.path.join(os.getcwd(), '.claude/skills')]

skills = {}
for raiz in RAICES:
    for md in glob.glob(f'{raiz}/*/SKILL.md'):
        nombre = os.path.basename(os.path.dirname(md))
        texto = open(md, errors='ignore').read()
        m = re.search(r'^description:\s*(.+?)(?=^\w[\w-]*:|^---)', texto, re.S | re.M)
        desc = m.group(1).strip() if m else ''
        skills[nombre] = {'bytes': len(texto.encode()), 'desc': len(desc), 'cargas': 0, 'releido': 0,
                          'enlace': os.path.islink(os.path.dirname(md))}

# cargas: el mensaje que inyecta el skill dice «Base directory for this skill: …/<nombre>»
patron = re.compile(r'Base directory for this skill: [^\s"\\]*/([\w.-]+)')
for path in glob.glob(f'{CASA}/projects/*/*.jsonl'):
    if datetime.fromtimestamp(os.path.getmtime(path), timezone.utc) < CORTE:
        continue
    pasos, cargas, vistos = 0, [], set()
    for linea in open(path, errors='ignore'):
        if '"usage"' in linea:
            try:
                msg = json.loads(linea).get('message') or {}
            except ValueError:
                continue
            if msg.get('id') not in vistos:
                vistos.add(msg.get('id'))
                pasos += 1
        elif 'Base directory for this skill' in linea:
            for nombre in set(patron.findall(linea)):
                cargas.append((nombre, pasos))
    for nombre, en in cargas:
        if nombre in skills:
            s = skills[nombre]
            s['cargas'] += 1
            s['releido'] += s['bytes'] / 4 * (pasos - en)

lista = sum(s['desc'] for s in skills.values())
print(f'{len(skills)} skills · la lista de descripciones pesa ~{lista / 4 / 1000:.1f}k tokens en CADA chat y subagente')
print(f'Releído estimado por cargar skills en {DIAS} días: {sum(s["releido"] for s in skills.values()) / 1e6:.0f}M tokens\n')
print(f'{"skill":40} {"SKILL.md":>9} {"descr.":>7} {"cargas":>7} {"releído":>9}')
for nombre, s in sorted(skills.items(), key=lambda x: (-x[1]['releido'], -x[1]['bytes'])):
    marca = ' (enlace)' if s['enlace'] else ''
    print(f'{(nombre + marca)[:40]:40} {s["bytes"] / 1024:7.1f}KB {s["desc"]:7} {s["cargas"]:7} {s["releido"] / 1e6:8.0f}M')
print('\nLectura: un SKILL.md de más de ~8 KB que se carga seguido se parte (núcleo + referencia).'
      '\nUn skill con 0 cargas en 30 días es candidato a archivarse (con permiso de la persona).')
