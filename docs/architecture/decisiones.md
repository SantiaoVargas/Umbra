# Decisiones fechadas

Formato: fecha, decisión, quién. Las decisiones vigentes mandan sobre cualquier otro documento. Solo se agregan filas (no reescribir las anteriores; si una cambia, se agrega una fila nueva que la reemplaza).

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-11-01 | Stack: Python + FastAPI (API), motor en Python puro (`core/`), httpx, Pydantic, pytest; frontend React en una fase posterior. Reemplaza el stack anterior de los docs iniciales (commit `8502e40`). | Santiago |
| 2026-11-01 | Principio rector: nunca prometer más de lo que se verificó. Se hace cumplir en código (`Finding`: `critical` ⇒ `confirmado`). | Santiago |
| 2026-11-01 | Se construye en orden: guardia → cliente HTTP → modelo de confianza → `header_checker` → reporte → endpoints → React. Primero la seguridad del sistema mismo. | Santiago |
| 2026-11-01 | Se adopta el marco SDD + Vertical Slice con IA (modelo LogiGho adaptado a un repo de dos devs). `docs/`, `specs/`, `backlog.md`, `CLAUDE.md` y `AGENTS.md` se versionan en git. | Iker |
| 2026-11-01 | Backlog reorganizado: historias `NNN`, mejoras `M-NNN`, ideas `I-NNN`; columna Responsable y dependencias para trabajar en paralelo sin pisarse. | Iker |
| 2026-11-01 | La aprobación de una spec es la revisión del otro dev sobre el PR draft, antes de escribir código. | Iker |
| 2026-11-01 | **Propuesta de la IA, pendiente de ratificar por Iker y Santiago:** reglas del producto P1–P6 de `docs/constitution.md` (en especial P4: solo peticiones de lectura hasta que exista modo activo). Mientras no se ratifiquen, se aplican como vigentes por prudencia. | IA (propone) |
