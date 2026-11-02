# Tasks 001: Guardia (allowlist)

Bloques de 15–30 min. TDD: test rojo, código mínimo, refactor. La persona responsable aprueba antes de ejecutar.
Modo de trabajo acordado: **Santiago escribe la lógica** de `allowlist.py`; la IA guía con pistas, escribe los tests con él y revisa.

| # | Tarea | Ruta | Test que la cubre | Estado |
|---|---|---|---|---|
| 1 | Modelo `Objetivo` con validación de `host`, `puerto`, `incluir_subdominios` | `src/umbra/core/allowlist.py` | `tests/test_allowlist.py::test_objetivo_*` | pendiente |
| 2 | `cargar_config`: leer JSON y dar errores claros | `src/umbra/core/allowlist.py` | `tests/test_allowlist.py::test_config_*` | pendiente |
| 3 | Parsear URL y normalizar host (minúsculas, punto final, esquema http/https) | `src/umbra/core/allowlist.py` | `tests/test_allowlist.py::test_normalizacion_*` | pendiente |
| 4 | `is_allowed`: coincidencia exacta de host + regla de puertos | `src/umbra/core/allowlist.py` | `tests/test_allowlist.py::test_host_*`, `test_puerto_*` | pendiente |
| 5 | Subdominios con `incluir_subdominios` (frontera del punto) | `src/umbra/core/allowlist.py` | `tests/test_allowlist.py::test_subdominio_*` | pendiente |
| 6 | Casos hostiles (`@`, `evil-`, `.evil.test`, basura) | `src/umbra/core/allowlist.py` | `tests/test_allowlist.py::test_hostil_*` | pendiente |
| 7 | Ejemplo `umbra.config.example.json` y `.gitignore` (si Iker aprueba) | raíz | — | pendiente |
| 8 | Cierre documental: ficha `guardia`, `decisiones.md`, `backlog.md`, `metricas-adopcion.md` | `docs/`, `backlog.md` | — | pendiente |

Estados: pendiente / en curso / hecha. Lo que no termina en la sesión se deja aquí como pendiente (o como nueva historia/mejora en `backlog.md`) para que el otro dev lo pueda retomar.

**Antes de abrir el PR:** `pytest` ✔ · `ruff check .` ✔ · criterios de la spec marcados V/F · cierre documental (ficha, decisiones, backlog, métricas).
