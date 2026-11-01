# Reglas técnicas del repo — Umbra

**Fecha:** 2026-11-01. Marcas: **observado** (ruta/comando), **hipótesis**, o casilla `[ ]` = pendiente de confirmar por los dos.

## Stack (observado en `pyproject.toml`)

- Python `>=3.11` (probado con 3.14). Build: hatchling, paquete en `src/umbra`.
- Runtime: `fastapi>=0.115`, `uvicorn[standard]>=0.30`, `httpx>=0.27`, `pydantic>=2.8`.
- Dev: `pytest>=8`, `pytest-asyncio>=0.23`, `ruff>=0.6` (línea máx. 100).
- Frontend React en `frontend/`: aún no existe (historia 007).

## Estructura (observado)

```
src/umbra/core/     motor, Python puro (hoy: findings.py)
src/umbra/api/      FastAPI, capa fina sobre core (hoy: main.py con /health)
tests/              pytest (TestClient para la API)
docs/  specs/  backlog.md     SDD (versionado)
```

Diseño completo de las piezas: `docs/DISENO-MOTOR.md`.

## Cómo compilar y probar en local

```bash
py -m venv .venv
.venv\Scripts\Activate.ps1          # PowerShell  (Git Bash: source .venv/Scripts/activate)
pip install -e ".[dev]"
pytest                               # todos los tests
ruff check .                         # lint
uvicorn umbra.api.main:app --reload --app-dir src   # http://127.0.0.1:8000/docs
```

## Reglas de código

- `core/` no importa nada de `api/` ni de `frontend/`. `api/` solo orquesta.
- Módulos de detección en `core/modules/`: no se importan entre sí; interfaz común (`id`, `name`, `description`, `run(ctx)` → `list[Finding]`).
- Los módulos obtienen red **solo** a través del cliente HTTP observador (nunca `httpx` directo).
- Modelos en fronteras con Pydantic; funciones públicas con type hints.
- Tests async con `pytest-asyncio` (ya configurado, scope de fixtures `function`).

## Pendientes de confirmar

- [x] CI en GitHub Actions (ruff + pytest en cada PR) — M-001, commit `c94d6e7`.
- [ ] Estrategia de merge a `main`: squash o merge normal.
- [ ] Protección de la rama `main` en GitHub (PR obligatorio + 1 aprobación + tests verdes).
- [ ] Formato de config de la allowlist (se decide en la spec de la historia 001).
- [ ] Python mínimo soportado en CI (3.11 vs 3.14).
- [ ] Gestor de tareas externo: por ahora ninguno; el backlog es `backlog.md`.
