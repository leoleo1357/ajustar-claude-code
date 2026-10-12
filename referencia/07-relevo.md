# Fase 7 — El relevo: pasar un chat pesado a uno nuevo sin perder nada

Compactar resume con paráfrasis y pierde detalle. El relevo pasa el contexto por preguntas y
respuestas, y el viejo sólo se cierra cuando el nuevo repite el plan sin errores.

**Cuándo:** el chat pasó ~250k tokens de contexto por paso (lo avisa `hook-relevo.py`), o la persona
dice «este chat ya está pesado». Si hay agentes corriendo, se espera a que terminen.

## El procedimiento
1. El viejo avisa en una línea y le da a la persona el texto para abrir el nuevo (o lo abre solo si
   hay una extensión que lo haga). El primer mensaje del nuevo empieza con su nombre,
   `R<n> <nombre del chat>` (R1, R2… por relevo), y dice: «Eres el RELEVO del chat <nombre>
   (dirección para escribirle: <socket o nombre de sesión>; historial: <ruta del .jsonl>)».
2. El nuevo manda **un** mensaje (con `SendMessage` entre sesiones; si no existe, la persona copia y pega):
   1 objetivo · 2 qué se decidió y quién · 3 qué está a medias · 4 pendientes con su dueño ·
   5 archivos y ramas tocados (rutas completas) · 6 las palabras **exactas** de la persona que mandan ·
   7 qué NO hacer · 8 el próximo paso concreto · 9 agentes o procesos vivos.
3. El viejo responde todo en un solo mensaje, con hechos medidos y citas literales.
4. El nuevo verifica en disco lo que pueda (git, archivos) y devuelve «CÓMO VOY A CONTINUAR» en ≤ 15
   líneas: objetivo, primero, después, lo que respetará (palabras textuales), lo que no hará, archivos.
5. El viejo responde exactamente `IDÉNTICO` o la lista de correcciones (máximo 2 rondas; si no
   cuadra, se avisa a la persona y no se cierra).
6. Con `IDÉNTICO`, el viejo deja de trabajar. Ante una duda futura, el nuevo hace `grep` en el
   `.jsonl` del viejo; nunca lo resume entero.

## Para instalarlo
Copia `plantillas/relevo-de-chat/` a `~/.claude/skills/relevo-de-chat/` (papel VIEJO y papel NUEVO)
y suma `hook-relevo.py` en `UserPromptSubmit`. Sin mensajería entre sesiones, la persona copia y pega
cada mensaje entre los dos chats: funciona igual, sólo más lento. Revisión tras 3–4 relevos: si no se perdió nada, se
puede bajar el umbral a 200k.
