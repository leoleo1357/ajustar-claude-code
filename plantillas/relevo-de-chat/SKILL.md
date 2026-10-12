---
name: relevo-de-chat
description: "Pasa un chat pesado a uno nuevo sin perder nada: el nuevo interroga al viejo, repite el plan y el viejo sólo se cierra con IDÉNTICO. Usar con «relevo», «pásalo a un chat nuevo», «este chat ya está pesado», o cuando el aviso diga que el chat pasó el umbral."
---

# Relevo de chat

Dos papeles: **VIEJO** (el chat pesado) y **NUEVO** (el que arranca con «Eres el RELEVO…»).
Misma carpeta de trabajo siempre. Nada de commits ni push por el relevo.

## Papel VIEJO
1. Si hay agentes propios corriendo, esperar a que terminen. Avisar en una línea: «Este chat ya está pesado: paso a uno nuevo.»
2. Averiguar cómo se le escribe a este chat (nombre de sesión o socket de mensajería, si existe) y la ruta de su historial: `~/.claude/projects/<carpeta>/<id de sesión>.jsonl`.
3. Nombre del nuevo: `R<n> <nombre del chat>` (si el viejo ya es `R<k> …`, n = k+1).
4. Darle a la persona, para pegar como PRIMER mensaje de un chat nuevo en la misma carpeta:
   «R<n> <nombre> — Eres el RELEVO del chat «<nombre>» (dirección: <cómo escribirle>; historial: <ruta del .jsonl>). Carga el skill relevo-de-chat y sigue su papel de NUEVO.»
5. Cuando lleguen las preguntas: contestar TODO en un solo mensaje, con hechos medidos y las palabras de la persona citadas literal.
6. Cuando llegue «CÓMO VOY A CONTINUAR»: responder exactamente `IDÉNTICO` o la lista de correcciones (máximo 2 rondas; si no cuadra, avisar a la persona y no cerrar).
7. Tras `IDÉNTICO`: dejar de trabajar (ni herramientas ni respuestas).

## Papel NUEVO
No tocar nada del repositorio hasta certificar.
1. Mandar al viejo (por mensajería entre sesiones; si no hay, pedir a la persona que lo copie) UN mensaje:
   «Soy el RELEVO. Respóndeme en UN solo mensaje: 1 objetivo · 2 qué se decidió y quién · 3 qué está a medias · 4 pendientes con su dueño · 5 archivos y ramas tocados (rutas completas) · 6 las palabras EXACTAS de la persona que mandan · 7 qué NO hacer · 8 el próximo paso concreto · 9 agentes o procesos vivos.»
2. Verificar en disco lo que se pueda (git status, archivos) en vez de volver a preguntar. Ante una duda, `grep` de la palabra exacta en el historial del viejo; nunca resumirlo entero ni leerlo con agentes.
3. Devolver al viejo, ≤ 15 líneas: «CÓMO VOY A CONTINUAR (ronda n): Objetivo… · Primero… · Después… · Respetaré (palabras textuales)… · No haré… · Archivos/ramas…»
4. Con `IDÉNTICO`: avisar a la persona «Relevo certificado. Soy R<n> <nombre>. Sigo con: <próximo paso>.» Si la pestaña no tomó el nombre, que lo ponga con `/rename`.
