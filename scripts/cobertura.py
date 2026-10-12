#!/usr/bin/env python3
"""cobertura.py — comprueba que al partir o acortar un archivo no se perdió ninguna línea.

Uso:  python3 cobertura.py <respaldo-original> <archivo-o-carpeta-nueva> [más archivos o carpetas…]

Toda línea no vacía del original (sin espacios a los lados) tiene que aparecer en alguno de los
archivos nuevos (.md dentro de las carpetas). Los enlaces que sólo cambiaron de prefijo «../» se
comparan normalizados. Sale con código 1 y muestra las líneas que faltan si falta alguna.
"""
import glob, os, sys

if len(sys.argv) < 3:
    sys.exit(__doc__)
norm = lambda l: l.strip().replace('../', '')
nuevos = set()
for destino in sys.argv[2:]:
    archivos = glob.glob(os.path.join(destino, '**/*.md'), recursive=True) if os.path.isdir(destino) else [destino]
    for f in archivos:
        nuevos.update(norm(l) for l in open(f, errors='ignore'))
original = [norm(l) for l in open(sys.argv[1], errors='ignore') if l.strip()]
faltan = [l for l in original if l not in nuevos]
print(f'faltan {len(faltan)} de {len(original)} líneas')
for l in faltan[:30]:
    print('  ✗', l[:120])
sys.exit(1 if faltan else 0)
