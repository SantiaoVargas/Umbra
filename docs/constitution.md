# Constitución del Proyecto Umbra

**Versión:** 2026-11-01. **Estado:** vigente. Toda regla aquí es innegociable. Se cambia solo con una decisión fechada en `docs/architecture/decisiones.md` aprobada por **los dos devs**.

## 1. Alcance y equipo

- Un solo repositorio: `github.com/SantiaoVargas/Umbra` (rama principal `main`). Sin carpetas ni clones paralelos del mismo repo.
- Equipo: **Iker** y **Santiago**. Cada uno trabaja con su propia IA, en su máquina y en su propia rama.
- A diferencia de otros proyectos, aquí **`docs/`, `specs/`, `backlog.md`, `CLAUDE.md` y `AGENTS.md` van versionados**: son el canal por el que los dos devs (y sus IAs) comparten contexto.

## 2. Reglas del producto (no se rompen nunca)

Umbra es una herramienta de escaneo de seguridad; el daño posible es real. Estas reglas protegen a terceros y a la credibilidad del producto.

- **P1. Allowlist fail-closed.** Ningún request sale hacia un host que no esté explícitamente autorizado. Se aplica también a cada salto de redirección. El control vive en **un solo punto** (el cliente HTTP observador); los módulos de detección nunca reciben un cliente `httpx` crudo.
- **P2. Confianza honesta.** Cada hallazgo lleva `severity` **y** `confidence`. Un `critical` solo existe si está `confirmado` (regla hecha cumplir en código por el validador de `Finding`). Un módulo nuevo no puede saltarse esto.
- **P3. Los tests nunca atacan objetivos reales.** Solo servidores locales de prueba (app vulnerable local) o transportes simulados. Ningún test, ejemplo ni doc apunta a un dominio de terceros.
- **P4. Peticiones no destructivas por defecto.** Hasta que exista la historia de "modo pasivo/activo" (ver `backlog.md`, ideas), los módulos solo hacen peticiones de lectura (`GET`/`HEAD`/`OPTIONS`) a ritmo controlado y respetando `429`/`Retry-After`. Cualquier prueba activa (enviar payloads) requiere spec propia aprobada por los dos.
- **P5. Sin secretos ni datos reales.** Nunca credenciales, tokens, cookies, `.env` ni reportes de objetivos reales en git ni en `docs/`. La evidencia que Umbra guarda no debe conservar credenciales de terceros (cómo se redacta se define en la spec del cliente HTTP).
- **P6. Uso autorizado.** La documentación de cara al usuario conserva la advertencia de uso autorizado (README).

## 3. Marco de trabajo: SDD + Vertical Slice con IA

- **Gobernanza (SDD):** esta constitución, `docs/repo_rules.md`, `specs/<NNN>_<tema>/spec.md` + `tasks.md` por funcionalidad, y `docs/architecture/` como memoria acumulada.
- **Entrega (Vertical Slice):** cada historia entrega un flujo probado de extremo a extremo (core → API cuando aplique), aunque sea chico. Historias en `backlog.md`: "Como [rol] quiero [acción] para [beneficio]".
- **Pair programming humano–IA:** la IA es DRIVER (escribe tests, código y docs, corre comandos). La **persona responsable** de la historia es NAVIGATOR (aprueba spec y tasks, revisa `git diff`, hace commit/push/PR).
- **Revisión cruzada:** la otra persona es REVISORA del PR. Su aprobación de la **spec** (antes de codear) y del **PR** (antes de mergear) es el control de calidad entre los dos.
- **Ciclo por feature:** historia → contexto/ficha → spec → tasks → rama + TDD → cierre documental. Detalle en `docs/flujo-de-trabajo-ia.md`.
- **Una sesión, un slice. Una historia, un responsable.**

## 4. Conocimiento: verdad verificada, no heredada

- Toda afirmación se marca como **observada** (ruta/línea o salida de un comando), **explicada por <persona>** (fecha) o **hipótesis**.
- Contradicción entre fuentes (doc vs código): se muestran ambas versiones con evidencia, se decide entre los dos y la decisión queda fechada.
- Lo que solo existe en el chat o en la memoria privada de una IA **no existe** para el equipo: se escribe en el repo.
- Cada slice cerrado actualiza fichas, contratos, esquemas y decisiones. El sistema aprende en cada desarrollo.

## 5. Ramas, commits y revisión

- `main` siempre verde (tests pasan). Nadie trabaja ni hace push directo a `main`.
- Una rama por historia: `feature/<NNN>-<tema>`, `fix/<tema>`, `chore/<tema>`, `docs/<tema>`. Minúsculas, guiones, sin tildes.
- Commits chicos, estilo `feat(<dominio>): ...`, `fix(...)`, `docs(...)`, `test(...)`, `chore(...)`.
- PR a `main`, revisado por la otra persona, merge por squash o merge normal (acordar). Plantilla en `.github/pull_request_template.md`.
- La IA no hace push, PR ni merge. Hace commit solo si su persona se lo pide.

## 6. Calidad de código

- SOLID y KISS: una razón de cambio por módulo; sin abstracciones prematuras; reutilizar antes de crear.
- Defensive programming: validar en los bordes (config, respuestas HTTP, entrada de la API), errores explícitos y mensajes claros.
- Tipado: modelos Pydantic en las fronteras, type hints en funciones públicas.
- Tests (pytest): todo slice trae tests; TDD cuando se pueda (rojo → verde → refactor). Un cambio sin test que lo cubra no está terminado.
- `ruff` limpio antes de abrir el PR.
- Sin dependencias nuevas sin aprobación de los dos (se agregan en `pyproject.toml` en el mismo PR, con justificación).
- Los módulos del core son independientes: no se importan entre sí; se comunican por la interfaz común.

## 7. Organización por dominios

El motor se sectoriza por dominios (ver `docs/architecture/dominios/README.md`): `guardia`, `cliente-http`, `modulos`, `confianza`, `reporte`, `api`, `frontend`. Cada historia declara su dominio y, si existe, se lee su ficha antes de tocar código.

## 8. Deuda técnica e ideas

- Deuda detectada durante un slice **no se arregla de paso**: va a `backlog.md` como mejora (`M-NNN`) con prioridad A/B/C.
- Ideas aún no decididas viven en la sección Ideas (`I-NNN`) y se promueven a historia cuando los dos lo acuerdan.
