# Backlog — Umbra (Motor)

Lista de tareas por fases. Se construyen **en orden** (cada fase se apoya en la
anterior). Marcá con `[x]` lo hecho.

**Leyenda:**
- ✅ **Confirmado** — acordado, va sí o sí.
- 🔎 **Por validar** — idea sobre la mesa; se decide si entra mientras
  desarrollamos.

El objetivo de AHORA es cerrar las Fases 0–6 = **motor funcional por CLI**. Todo
lo que está en _Parking lot_ es para después.

---

## Fase 0 — Cimientos del proyecto ✅

- [ ] Inicializar Node.js + TypeScript (`package.json`, `tsconfig.json`)
- [ ] Linter + formatter (ESLint + Prettier)
- [ ] Framework de tests (Vitest)
- [ ] Estructura de carpetas (`src/`, `tests/`)
- [ ] `CONTRIBUTING.md` para dos devs: ramas, PRs, cómo correr/testear
- [ ] CI básico en GitHub Actions: correr tests en cada PR
- [ ] `.gitignore` (node_modules, dist, etc.)

## Fase 1 — El guardia (allowlist) ✅

- [ ] Definir formato de `umbra.config.json`
- [ ] Parser + validación de la config (errores claros si está mal)
- [ ] `isAllowed(url)` con _fail-closed_
- [ ] Normalización de host/URL (puertos, mayúsculas, trailing slash)
- [ ] Tests: objetivo autorizado pasa; typo / host no autorizado → bloqueado

## Fase 2 — Cliente HTTP observador ✅

- [ ] Wrapper sobre `undici` / `fetch`
- [ ] No seguir redirecciones a ciegas: revalidar cada salto contra allowlist
- [ ] Respetar `429` / `Retry-After` (backoff)
- [ ] Rate-limit / límite de concurrencia
- [ ] Registrar request/response como evidencia
- [ ] Tests con servidor mock (redirecciones, 429, límites)

## Fase 3 — Modelo de hallazgo + confianza ✅

- [ ] Tipo `Finding` (`severity`, `confidence`, `evidence`, `remediation`)
- [ ] Reglas de confianza: `confirmado` vs `por-revisar`
- [ ] Regla dura: no `critical` confirmado sin verificación
- [ ] Tests de las reglas

## Fase 4 — Primer módulo: cabeceras de seguridad ✅

- [ ] Interfaz común de módulo: `{ id, name, description, run(ctx) }`
- [ ] Módulo `security-headers` (HSTS, CSP, anti-clickjacking, etc.)
- [ ] App web vulnerable local para testear (cabeceras faltantes a propósito)
- [ ] Tests de punta a punta → **la base queda validada**

## Fase 5 — Generador de reporte ✅

- [ ] Reporte en Markdown: separar "confirmado" de "por revisar"
- [ ] Plan priorizado (qué arreglar primero)
- [ ] 🔎 Salida JSON (para integraciones futuras) — por validar
- [ ] Tests

## Fase 6 — CLI ✅

- [ ] Comando `umbra scan --config <archivo>`
- [ ] Orquestar: leer config → correr módulos en orden → generar reporte
- [ ] Manejo de errores y códigos de salida claros
- [ ] Tests end-to-end

---

## Parking lot (ideas — NO ahora) 🔎

Se capturan para no perderlas; se validan más adelante.

**Más módulos de detección:**
- [ ] 🔎 Autenticación faltante (endpoints que deberían pedir login)
- [ ] 🔎 Datos sensibles expuestos
- [ ] 🔎 Otros, según lo que pida el mercado

**Capa de producto (sub-proyecto 2):**
- [ ] 🔎 Dashboard web para usuarios no técnicos
- [ ] 🔎 Cuentas de usuario
- [ ] 🔎 Verificación de propiedad del objetivo (clave legal y comercial)
- [ ] 🔎 Guardado de resultados / historial de escaneos
- [ ] 🔎 Billing / planes (monetización)

**Integraciones y modos:**
- [ ] 🔎 Integración con el CI de los usuarios / GitHub App
- [ ] 🔎 Modo "solo pasivo" vs "activo"

---

## Hasta dónde llegamos AHORA

Fases 0–6 = **motor funcional por CLI** que:

1. Solo escanea objetivos autorizados (allowlist).
2. Pega de forma controlada (cliente HTTP observador).
3. Detecta cabeceras de seguridad faltantes (web y API).
4. Reporta con **confianza honesta** (confirmado vs por revisar).
5. Entrega un reporte legible con plan de qué arreglar primero.

Ese es el MVP del motor. Todo lo demás es _parking lot_.
