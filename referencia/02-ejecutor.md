# Fase 2 — El agente ejecutor (la palanca más grande; minutos de trabajo)

## Por qué
El agente `general-purpose` trae todas las herramientas de la sesión (publicar páginas, flujos,
lanzar agentes, MCP…), y sus descripciones pesan ~30k tokens. Un agente que sólo lee, edita y corre
comandos no las usa, pero las relee en **cada paso**. Medido en el equipo de origen: general 45,8k
fijos → ejecutor 15,5k; mediana releída por Sonnet 4,6M → 1,4M; minutos 6,7 → 2,6.

## Cómo
1. Propón el cambio (cinco renglones) y espera el «sí».
2. Copia `plantillas/ejecutor.md` a `~/.claude/agents/ejecutor.md`. Ajusta `model` al modelo
   intermedio que use la persona. Las herramientas: `Bash, Read, Edit, Write, Grep, Glob`.
3. Los tipos de agente se leen **al abrir un chat**: en el chat actual no aparece hasta que se
   reabre (o hasta que Claude Code lo anuncia).
4. Comprueba en un chat que ya lo conozca: lanza un ejecutor con «corre `echo ok` y responde OK» y
   mide su primer paso (`gasto.py` → fila `ejecutor`, columna «fijo»). Debe quedar alrededor de un
   tercio del general. Si no, revisa que `tools:` esté bien escrito.

## Cuándo NO usar el ejecutor
Cuando el agente necesita navegador (MCP de Chrome, Playwright vía MCP) u otro servidor MCP: ahí va el
general, y el prompt lo dice. Para buscar sin editar existe además `Explore` (~23k fijos).
