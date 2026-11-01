# Backlog — Umbra (Motor)

Lista de tareas por fases. Se construyen **en orden** (cada fase se apoya en la
anterior). Marcá con `[x]` lo hecho.

**Leyenda:**
- ✅ **Confirmado** — acordado, va sí o sí.
- 🔎 **Por validar** — idea sobre la mesa; se decide mientras desarrollamos.

**Stack:** Python + FastAPI (backend) · React (frontend, después). HTTP con
httpx, modelos con Pydantic, tests con pytest.

El objetivo de AHORA es cerrar las Fases 0–5 = **motor funcional servido por una
API**. Todo lo que está en _Parking lot_ es para después.

---

## Fase 0 — Cimientos del proyecto ✅ (HECHA)

- [x] Entorno Python + `pyproject.toml` (deps: fastapi, uvicorn, httpx, pydantic)
- [x] Estructura `src/umbra/` con `core/` y `api/`
- [x] Framework de tests (pytest) + primeros tests en verde
- [x] Modelo `Finding` con Pydantic (severity + confidence) y su regla dura
- [x] FastAPI corriendo con `/health` y `/docs`
- [x] `.gitignore` y `CONTRIBUTING.md` (para dos devs)
- [ ] 🔎 Linter en CI (ruff ya está como dep; falta GitHub Actions)

## Fase 1 — El guardia (allowlist) ✅

- [ ] Definir formato de config (objetivos autorizados)
- [ ] Parser + validación de la config (errores claros)
- [ ] `is_allowed(url)` con _fail-closed_
- [ ] Normalización de host/URL (puerto, mayúsculas, trailing slash)
- [ ] Tests: objetivo autorizado pasa; typo / host no autorizado → bloqueado

## Fase 2 — Cliente HTTP observador (httpx) ✅

- [ ] Wrapper sobre httpx (async)
- [ ] No seguir redirecciones a ciegas: revalidar cada salto contra allowlist
- [ ] Respetar `429` / `Retry-After` (backoff)
- [ ] Rate-limit / límite de concurrencia
- [ ] Registrar request/response como evidencia
- [ ] Tests con servidor mock

## Fase 3 — Primer módulo: cabeceras de seguridad ✅

- [ ] Interfaz común de módulo (`id`, `name`, `description`, `run(ctx)`)
- [ ] Módulo `header_checker` (HSTS, CSP, anti-clickjacking, etc.)
- [ ] App web vulnerable local para testear
- [ ] Tests de punta a punta → **la base queda validada**

## Fase 4 — Generador de reporte ✅

- [ ] Reporte en Markdown: separar "confirmado" de "por revisar"
- [ ] Plan priorizado (qué arreglar primero)
- [ ] Salida JSON (para que la API la devuelva)
- [ ] Tests

## Fase 5 — Endpoints FastAPI ✅

- [ ] Endpoint para lanzar un escaneo (recibe el host autorizado)
- [ ] Endpoint / respuesta con el reporte estructurado
- [ ] Schemas Pydantic de request/response
- [ ] Manejo de errores claro (host no autorizado, etc.)
- [ ] Tests con TestClient

## Fase 6 — Frontend React 🔎

- [ ] Proyecto React en `frontend/`
- [ ] Pantalla para ingresar el host y ver el reporte
- [ ] Consume la API de Umbra

---

## Parking lot (ideas — NO ahora) 🔎

**Más módulos de detección:**
- [ ] 🔎 Autenticación faltante (endpoints que deberían pedir login)
- [ ] 🔎 Datos sensibles expuestos
- [ ] 🔎 Otros, según lo que pida el mercado

**Capa de producto (sub-proyecto 2):**
- [ ] 🔎 Cuentas de usuario
- [ ] 🔎 Verificación de propiedad del objetivo (clave legal y comercial)
- [ ] 🔎 Guardado de resultados / historial de escaneos
- [ ] 🔎 Billing / planes (monetización)

**Integraciones y modos:**
- [ ] 🔎 Integración con el CI de los usuarios / GitHub App
- [ ] 🔎 Modo "solo pasivo" vs "activo"

---

## Hasta dónde llegamos AHORA

Fases 0–5 = **motor funcional servido por una API** que:

1. Solo escanea objetivos autorizados (allowlist).
2. Pega de forma controlada (cliente HTTP observador, httpx).
3. Detecta cabeceras de seguridad faltantes (web y API).
4. Reporta con **confianza honesta** (confirmado vs por revisar).
5. Entrega el reporte por un endpoint, listo para que React lo consuma.

Ese es el MVP del motor. El frontend React y todo lo demás viene después.
