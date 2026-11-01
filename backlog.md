# Backlog — Umbra

Fuente única de qué se construye, en qué orden y quién lo tiene. Cada historia se desarrolla con `/umbra-slice` (spec y tasks en `specs/<NNN>_<tema>/`).
Última actualización: 2026-11-01.

**Objetivo de AHORA:** historias 001–006 = **motor funcional servido por una API** (el MVP del motor). Frontend, producto y más módulos son posteriores.

## Cómo se usa este backlog (somos dos)

- **Tres listas, tres prefijos:** historias `NNN` (funcionalidad, se hacen en orden), mejoras `M-NNN` (deuda técnica, no funcionalidad), ideas `I-NNN` (sin decidir; se promueven a historia cuando los dos lo acuerdan).
- **Reclamar:** poner tu nombre en **Responsable** y el estado `en spec` *en tu rama*, y abrir PR draft con la spec. Una historia con Responsable no se toca por el otro.
- **Estados de una historia:** `pendiente` → `en spec` → `en curso` → `en revisión` (PR abierto) → `hecho` (mergeado a `main`). Además: `bloqueada` (con motivo) y `🔎 por validar` (falta decidir si va).
- **Prioridad:** **A** = bloquea el MVP o toca seguridad/honestidad del producto, **B** = necesaria para el MVP, **C** = conveniente.
- **Dependencias:** una historia solo se empieza si las suyas están `hecho`; si no, se puede escribir la spec pero no codear.
- **Detalle, no tareas:** aquí va el "qué y para qué". El desglose en bloques de 15–30 min vive en `tasks.md` de cada spec.
- Cambios a este archivo: pequeños y solo agregando filas (evita conflictos entre los dos).

## Historias

| ID | Historia | Dominio | Fase | Prio | Depende de | Estado | Responsable | Spec |
|---|---|---|---|---|---|---|---|---|
| 000 | Como equipo quiero un esqueleto Python/FastAPI con el modelo `Finding` y sus tests para empezar sobre una base verde | base | 0 | A | — | **hecho** (commit `8502e40`) | Santiago | — |
| 001 | Como dueño de un sistema quiero que Umbra solo escanee objetivos que autoricé explícitamente, para que un typo o un host ajeno nunca reciban tráfico | guardia | 1 | A | 000 | pendiente | — | `specs/001_allowlist/` (por crear) |
| 002 | Como dev de módulos quiero un cliente HTTP observador que respete la allowlist, los redirects, el `429` y un límite de concurrencia, y registre la evidencia, para detectar sin dañar ni salirme de lo autorizado | cliente-http | 2 | A | 001 | pendiente | — | `specs/002_cliente_http/` (por crear) |
| 003 | Como dev de módulos quiero una interfaz común de módulo y una app web vulnerable local, para escribir y probar módulos de forma segura y en paralelo | modulos | 3 | B | 000 | pendiente | — | `specs/003_interfaz_modulos/` (por crear) |
| 004 | Como usuario quiero que Umbra detecte cabeceras de seguridad faltantes (HSTS, CSP, anti-clickjacking, etc.) con confianza alta, para corregir lo básico sin falsos positivos | modulos | 3 | A | 002, 003 | pendiente | — | `specs/004_header_checker/` (por crear) |
| 005 | Como usuario quiero un reporte que separe lo confirmado de lo por revisar y priorice qué arreglar primero, en Markdown y JSON, para actuar sobre lo que importa | reporte | 4 | B | 004 | pendiente | — | `specs/005_reporte/` (por crear) |
| 006 | Como usuario quiero lanzar un escaneo y obtener su reporte por la API, con errores claros (host no autorizado, etc.), para consumirlo desde un front o un script | api | 5 | B | 005 | pendiente | — | `specs/006_api_escaneo/` (por crear) |
| 007 | Como usuario quiero una pantalla donde ingreso el host y veo el reporte, para no usar la API a mano | frontend | 6 | C | 006 | 🔎 por validar | — | `specs/007_frontend/` (por crear) |

**Paralelismo posible hoy:** 001 y 003 no dependen entre sí → pueden tomarlas una persona cada una. 002 espera a 001; 004 espera a 002 y 003.

## Detalle de lo que entra (preliminar, se afina en cada spec)

### 001. El guardia (allowlist) — A
- **Entra:** formato de config de objetivos autorizados (archivo, p. ej. `umbra.config.json`); parser con validación y errores claros; `is_allowed(url)` *fail-closed*; normalización de host/URL (puerto, mayúsculas, trailing slash, subdominios); tests (autorizado pasa; typo, host ajeno, esquema distinto → bloqueado).
- **No entra:** verificación de propiedad del dominio (idea I-005), cuentas de usuario.
- **Por decidir en la spec:** formato exacto de la config; si se permiten comodines/subdominios; si el puerto forma parte de la identidad del objetivo.
- **Aceptación (borrador):** un host fuera de la lista nunca pasa; una config inválida impide arrancar con mensaje claro; ninguna ruta de código permite saltarse `is_allowed`.

### 002. Cliente HTTP observador — A
- **Entra:** wrapper async sobre httpx; **no seguir redirects a ciegas** (revalidar cada salto contra la allowlist); backoff con `429`/`Retry-After`; límite de concurrencia y de tasa; registro de request/response como evidencia; tests con servidor mock.
- **No entra:** pruebas activas (payloads) → regla P4 de la constitución.
- **Por decidir en la spec:** cómo se **redacta la evidencia** (cookies, `Authorization`, tokens) antes de guardarla (P5); límites por defecto de tasa y timeouts.
- **Aceptación (borrador):** un redirect hacia un host no autorizado se corta y se registra; con `429` el cliente espera; el módulo nunca recibe un `httpx` crudo.

### 003. Interfaz de módulos + app vulnerable local — B
- **Entra:** contrato de módulo (`id`, `name`, `description`, `run(ctx)` → `list[Finding]`); `ctx` con el cliente protegido y el objetivo; registro/descubrimiento de módulos; app web local con cabeceras faltantes a propósito (para tests de punta a punta).
- **No entra:** módulos reales de detección (004 en adelante).
- **Aceptación (borrador):** un módulo de ejemplo corre contra la app local y devuelve `Finding`; agregar un módulo no exige tocar los existentes.

### 004. `header_checker` — A
- **Entra:** HSTS, CSP, anti-clickjacking (`X-Frame-Options`/`frame-ancestors`), `X-Content-Type-Options`, `Referrer-Policy`, etc.; severidad y confianza justificadas por cabecera; remediación por hallazgo. Elegido primero porque la cabecera **está o no está** (confianza altísima).
- **Aceptación (borrador):** la app vulnerable local produce los hallazgos esperados; una app con todas las cabeceras no produce ninguno; ningún `critical` por-revisar (P2).

### 005. Reporte — B
- **Entra:** Markdown con secciones "confirmado" y "por revisar"; plan priorizado (qué arreglar primero); salida JSON para la API; tests.
- **Aceptación (borrador):** el reporte no mezcla confirmados con por-revisar; el orden del plan es determinista y testeable.

### 006. Endpoints FastAPI — B
- **Entra:** endpoint para lanzar un escaneo (recibe el host autorizado); respuesta con el reporte estructurado; schemas Pydantic de request/response; errores claros (host no autorizado → error explícito); tests con `TestClient`.
- **Por decidir en la spec:** síncrono vs. job asíncrono con id; contrato JSON (`docs/architecture/contratos/`).

### 007. Frontend React — C (🔎 por validar)
- **Entra:** proyecto en `frontend/`; pantalla para ingresar host y ver el reporte; consume la API de 006.
- **Decisión pendiente:** si va en este repo o en uno aparte; librería de UI.

## Ideas (sin decidir — NO se construyen todavía)

Se promueven a historia `NNN` cuando los dos lo acuerdan (queda fechado en `docs/architecture/decisiones.md`).

| ID | Idea | Área | Notas |
|---|---|---|---|
| I-001 | Módulo: autenticación faltante (endpoints que deberían pedir login) | modulos | Más difícil de confirmar → mucho cuidado con la confianza (P2) |
| I-002 | Módulo: datos sensibles expuestos | modulos | Evidencia sin guardar el dato sensible (P5) |
| I-003 | Más módulos de detección, según lo que pida el mercado | modulos | — |
| I-004 | Cuentas de usuario | producto | Sub-proyecto 2 |
| I-005 | Verificación de propiedad del objetivo | producto | Clave legal y comercial; refuerza P1/P6 |
| I-006 | Guardado de resultados / historial de escaneos | producto | Define esquema en `docs/architecture/datos/` |
| I-007 | Billing / planes (monetización) | producto | — |
| I-008 | Integración con el CI de los usuarios / GitHub App | integraciones | — |
| I-009 | Modo "solo pasivo" vs "activo" | motor | Al decidirlo se revisa la regla P4 |

## Oportunidades de mejora (deuda técnica)

Etiqueta **mejora**: mantenimiento, seguridad y calidad; no son funcionalidad nueva. Se toman de a una, con spec corta y tests. Prioridad: A (seguridad/honestidad), B (robustez), C (limpieza).

| ID | Dominio | Prio | Mejora | Evidencia |
|---|---|---|---|---|
| M-001 | base | B | ~~CI en GitHub Actions~~ **hecha** (commit `c94d6e7`, `.github/workflows/ci.yml`). Falta solo proteger `main` exigiendo ese check | observado 2026-11-01 |
| M-002 | base | C | Definir y fijar en `ruff` el conjunto de reglas (hoy solo `line-length = 100`) | `pyproject.toml` `[tool.ruff]` |

## Hecho

- **Fase 0 — Cimientos** (historia 000): entorno Python y `pyproject.toml`, estructura `src/umbra/{core,api}`, pytest con tests en verde, modelo `Finding` con su regla dura (`critical` ⇒ `confirmado`), FastAPI con `/health` y `/docs`, `.gitignore`, `CONTRIBUTING.md`.
