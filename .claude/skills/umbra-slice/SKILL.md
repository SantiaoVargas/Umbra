---
name: umbra-slice
description: Ejecutar un desarrollo de Umbra como vertical slice con SDD (historia → ficha de dominio → spec → tasks → TDD en rama → cierre documental), pensado para dos devs con su propia IA. Usar al implementar una historia del backlog, una mejora M-NNN o cualquier cambio de código, o al documentar un dominio.
---

# Vertical slice de Umbra

Raíz = la del repo (contiene `CLAUDE.md`, `docs/constitution.md`, `backlog.md`, `specs/`). Todo es relativo a ella.

**Leer antes de empezar:** `docs/constitution.md` (reglas del producto P1–P6), `docs/flujo-de-trabajo-ia.md`, `docs/repo_rules.md`, `docs/DISENO-MOTOR.md` y la ficha en `docs/architecture/dominios/<dominio>.md` (si no existe, crearla desde `_plantilla.md` solo con lo necesario).

**Tamaño del slice**
- **Ligero** (fix/mejora C de 1–2 archivos): spec de 5 líneas en el chat o el PR, sin `tasks.md`, test obligatorio, cierre normal.
- **Completo** (historia nueva, mejora A/B, cualquier cosa que toque P1 allowlist/cliente HTTP, P2 modelo `Finding`, P4 peticiones activas, o la API): los 6 pasos con aprobación.

**Pasos**
1. **Historia y reclamo.** Confirmar el ID en `backlog.md`. Verificar que **Responsable** esté vacío o sea la persona que habla, y que sus dependencias estén `hecho`. Si el otro dev la tiene, parar y avisar. Crear la rama `feature/<NNN>-<tema>` desde `main` actualizado y poner Responsable + estado `en spec` en el backlog.
2. **Contexto.** Seguir el flujo en el código real. Marcar **observado** (ruta/línea) / **<persona>** (fecha) / **hipótesis**. Preguntar solo lo que cambia una decisión.
3. **Spec.** `specs/<NNN>_<tema>/spec.md` desde `specs/_plantilla/spec.md`, incluyendo las secciones **Honestidad (severidad/confianza)** y **Seguridad del producto**. Modo plan. Esperar aprobación de la persona; sugerirle abrir PR draft para que la otra persona apruebe la spec antes de codear.
4. **Tasks.** `tasks.md` en bloques de 15–30 min con su test. Esperar aprobación.
5. **TDD.** Por task: test rojo → código mínimo → refactor → `pytest` y `ruff check .` con salida real. Módulos de detección solo contra la app vulnerable local o mocks (P3). Sin dependencias nuevas sin aprobación. **No** hacer push, PR ni merge; commit solo si la persona lo pide (mensaje convencional `feat(<dominio>): ...`).
6. **Cierre (mismo PR).** Criterios V/F con evidencia; resumen de `git diff`; actualizar ficha de dominio, `docs/architecture/decisiones.md`, `contratos/`, `datos/`, `backlog.md` (estado `en revisión` + mejoras `M-NNN`), `docs/repo_rules.md` si hay regla nueva, y una fila en `docs/metricas-adopcion.md`.

**Reglas que no se negocian:** nunca en `main`; la verdad vive en el repo (lo que se aclare en el chat se escribe en spec/ficha/decisiones); deuda detectada no se arregla de paso (va a `M-NNN`); una sesión, un slice.
