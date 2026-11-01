# Métricas de adopción del marco (revisar a los 3 meses)

Objetivo: decidir con datos si el flujo SDD + IA de a dos funciona, qué sobra y qué falta.

## Registro por slice (la IA agrega una fila al cerrar)

| Fecha | ID | Dominio | Responsable | Tareas plan/real | Tests añadidos | Bugs hallados por tests antes del PR | Preguntas a la persona | Discrepancias doc-código | Decisiones nuevas | Horas aprox. | Notas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-01 | 000 | (base) | Iker + Claude | montaje de SDD (docs, backlog, specs, skill) | 0 | n/a | 0 | 1 (leyenda ✅ del backlog marcaba "confirmado" y parecía "hecho") | 4 | n/d | adopción del marco; backlog reorganizado en 008 historias + ideas + mejoras |

## Preguntas para la revisión trimestral

1. ¿La IA de cada dev arrancó cada slice leyendo la ficha/spec correcta sin re-explicar el contexto?
2. ¿Hubo colisiones entre los dos devs (misma historia, mismo ID, conflictos en archivos calientes)? ¿Qué las causó?
3. ¿Cuántas mejoras `M-NNN` se cerraron vs. cuántas se abrieron?
4. ¿Se rompió alguna regla del producto (P1–P6)? ¿La detectó un test, la revisión o nadie?
5. ¿Las specs aprobadas en PR draft evitaron retrabajo? (contar PRs con cambios grandes después de la spec)
6. ¿Una persona nueva podría tomar una historia leyendo solo `docs/` y `specs/`, sin IA ni chat?
7. ¿Qué secciones de la plantilla de spec quedan siempre vacías?

## Señales de que algo sobra

- Secciones de plantilla que siempre quedan vacías.
- Archivos que nadie lee en dos meses (ver fecha de modificación).
- Pasos del flujo que se saltan sistemáticamente.
