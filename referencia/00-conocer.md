# Fase 0 — Conocer a la persona

Un Claude que no sabe con quién trabaja explica de más, pregunta de más y repite errores. Antes de
optimizar, se arma la **identidad**: quién es, cómo trabaja, qué quiere, qué no tolera.

## 0.1 Lo que se lee solo (sin preguntar)

```bash
cat ~/.claude/CLAUDE.md 2>/dev/null | head -80          # sus reglas globales, si existen
ls ~/.claude/rules ~/.claude/skills ~/.claude/agents 2>/dev/null
ls ~/.claude/projects | head -50                        # carpetas donde trabaja (una por repo)
ls ~/.claude/projects/*/memory/MEMORY.md 2>/dev/null    # memorias por proyecto
```
Con eso ya sabes en qué repos trabaja, si tiene memoria, cuántos skills, si hay hooks
(`~/.claude/settings.json` → `"hooks"`).

## 0.2 La entrevista (corta, una pregunta por vez, con tu propuesta ya escrita)

1. ¿A qué te dedicas y en qué proyectos usas Claude? (para el mapa de proyectos)
2. ¿Cómo prefieres que te hable? Idioma, tú/usted, largo de las respuestas, si quiere el dato primero.
3. ¿Cómo le das los pedidos? (escrito, por voz con errores de transcripción, en ráfagas…)
4. ¿Qué te molesta de cómo trabaja hoy? (lento, caro, pregunta mucho, hace cosas sin permiso…)
5. ¿Qué no se toca nunca sin preguntarte? (producción, dinero, borrar datos, subir código…)
6. ¿Qué quieres mejorar tú con Claude este mes?

No pidas ni anotes credenciales, datos de clientes, cifras de negocio ni nada sensible.

## 0.3 El CLAUDE.md global (≤ 4 KB: se carga en CADA mensaje y en cada agente general)

Propón este esqueleto con lo que respondió, y que lo apruebe:

```markdown
# Quién soy
<2–4 líneas: a qué se dedica, en qué proyectos, qué disfruta y qué busca>

# Cómo trabajar conmigo
- Idioma y trato: …   · Largo: el dato primero, corto, una sola pregunta al final.
- Cómo dicto: … (entender la intención, no la letra).
- Decido yo: todo desarrollo nuevo se aprueba antes de escribirlo (cinco renglones).
- Lo que se reporta, se midió.

# Nunca sin preguntar
- …

# Mapa de proyectos
- <repo> — <qué es, en una línea>
```
Lo largo (procedimientos, historia, decisiones) NO va aquí: va a skills o a memoria, que se leen sólo
cuando hacen falta. Cada línea de este archivo se paga en cada paso de cada chat.

## 0.4 Cierre de la fase
Muestra el CLAUDE.md propuesto y su tamaño (`wc -c`). Con el «sí», respaldo del anterior y escritura.
