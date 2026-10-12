# Fase 6 — Caché y hábitos del chat principal

La caché de contexto hace que releer cueste ~10 %. Cuando se rompe, el chat entero se vuelve a
escribir como **nuevo** (precio completo). `gasto.py` cuenta esas «reescrituras de caché» por chat.

## Lo que la rompe (medido en el equipo de origen: 35 caídas sin pausa en 7 días)
| Causa | Cuánto pesó | Regla |
|---|---|---|
| **cambiar de modelo dentro del chat** (`/model`) | 21 de 35 | en un chat pesado no se cambia de modelo: **se lanza un agente con ese modelo** y un prompt autocontenido |
| reanudar un chat viejo | la mayoría del resto | para un tema viejo, mejor un chat nuevo que pregunte al viejo (fase 7) o busque con `grep` en su `.jsonl` |
| pausas de más de ~1 hora (vence la caché) | 100 eventos / 42 % de la caché escrita | el chat largo pausado se paga entero al volver: cerrar o relevar antes de una pausa larga |

## Hábitos que suman
- **Un chat por tema**. Un chat que mezcla todo crece sin fin: miles de pasos × cientos de miles de
  contexto. En el equipo de origen, los 4 chats más largos releyeron más que todos los agentes juntos.
- **Contar, medir, comparar: con un script**, nunca leyendo archivos enteros en el chat.
- **Leer sólo la parte** de un archivo grande (rango de líneas, `grep -n`), no el archivo entero.
- **No pegar volcados** (logs, JSON enormes) al chat: resumir con un script y pegar la conclusión.
- **Los agentes devuelven conclusiones**, no volcados (el informe entra al contexto del chat).
- **No delegar en agentes la lectura de historiales viejos** ni pedir «resúmeme todo»: `grep` de la palabra exacta.
