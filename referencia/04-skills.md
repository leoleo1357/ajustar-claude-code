# Fase 4 — Skills: la lista corta y los pesados partidos

Dos costos (ver `scripts/peso-skills.py`):
- **La lista**: la descripción de cada skill va en CADA chat y CADA agente general, se use o no.
- **La carga**: un skill invocado mete su SKILL.md entero, que se relee en cada paso siguiente.

## 4.1 La lista
- Descripción ideal: 1–2 frases (qué hace + «Usar cuando…» con las frases que dice la persona). ≤ 350 caracteres.
- Skills que no se usaron en 30 días: proponer **archivarlos** (mover a `~/.claude/skills-archivo/`, nunca borrar).
  Ojo: hay skills que se usan poco pero importan; la persona decide uno por uno.
- Familias de skills sueltos (p. ej. ocho de correo, veinte de un framework): **empaquetarlos** dentro de un
  skill dueño, que diga «para X, lee `<ruta>/SKILL.md`». Desaparecen de la lista y siguen disponibles.
- Medir antes y después cuántos tokens pesa la lista (en el equipo de origen: 10,1k → 4,1k).

## 4.2 Partir un SKILL.md pesado (núcleo + referencia)
Candidatos: más de ~8 KB y cargado seguido (lo dice `peso-skills.py`). Procedimiento, probado:
1. Respaldo: `cp SKILL.md SKILL.md.bak-<fecha>-antes-de-partir`.
2. Un ejecutor corta las secciones (`##`) a `referencia/<tema>.md` **con un script, tal cual**: no
   reescribe, no resume, no corrige. Cada archivo empieza con «# <tema> — referencia de <skill>».
3. El nuevo SKILL.md: el frontmatter **idéntico**; debajo el núcleo (≤ 5–8 KB): qué es, la orden
   principal, y **toda regla que valga en CADA uso**, en una línea cada una, sin suavizar («nunca»
   sigue siendo «nunca»); al final una tabla «Si pasa X → lea referencia/Y.md» que cubra todo.
4. Verificación: `python3 scripts/cobertura.py SKILL.md.bak-… SKILL.md referencia/` → **faltan 0**.
5. Certifica otro agente que no lo partió: ¿alguna regla que hace falta en cada uso quedó sólo en
   referencia? ¿la tabla lleva al archivo correcto? ¿bloques de código cerrados? En el equipo de
   origen el certificador encontró en las dos pasadas reglas de uso diario que se habían ido a
   referencia: es el paso que no se salta.
6. Busca scripts que lean o escriban el SKILL.md (`grep -rn 'SKILL.md' ~/.claude --include=*.py
   --include=*.mjs --include=*.sh`): si alguno inyecta un bloque al principio, ese bloque se queda
   en el núcleo.
Resultado medido allá: 86 KB → 4,6 KB y 61 KB → 8,2 KB, 0 líneas perdidas.
