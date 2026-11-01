# Cómo trabajar en Umbra

Guía rápida para los dos devs. El objetivo: que ambos levanten el proyecto igual
y no nos pisemos en Git.

## Requisitos

- Python 3.11+ (probado con 3.14)
- Node 18+ (para el frontend React, más adelante)

## Puesta en marcha (una sola vez)

```bash
# 1. Crear el entorno virtual (aísla las dependencias de este proyecto)
py -m venv .venv

# 2. Activarlo
#    PowerShell:
.venv\Scripts\Activate.ps1
#    Git Bash:
source .venv/Scripts/activate

# 3. Instalar el proyecto en modo editable + dependencias de desarrollo
pip install -e ".[dev]"
```

## Día a día

```bash
# Correr los tests
pytest

# Levantar la API (abre http://127.0.0.1:8000/docs para la documentación automática)
uvicorn umbra.api.main:app --reload --app-dir src
```

## Flujo de trabajo (somos dos, cada uno con su IA)

El detalle completo está en [docs/flujo-de-trabajo-ia.md](docs/flujo-de-trabajo-ia.md). En corto:

1. Elegí una historia **libre** de [backlog.md](backlog.md) (sin Responsable, con dependencias `hecho`) y avisale al otro.
2. Rama desde `main` actualizado: `git checkout -b feature/001-allowlist`. Nunca trabajar directo sobre `main`.
3. Spec + tasks primero (`/umbra-slice` en Claude Code, o `AGENTS.md` en Codex/Cursor). Abrí un **PR en borrador**: la otra persona aprueba la spec antes de codear.
4. Código con TDD; `pytest` y `ruff check .` en verde.
5. Cierre documental en el mismo PR (ficha, decisiones, backlog, métricas). Plantilla de PR en `.github/`.
6. La otra persona revisa y aprueba; merge a `main`. La IA nunca hace push/PR/merge.

Preferencias personales de tu IA van en `CLAUDE.local.md` (no se sube). Todo lo que el equipo deba saber se escribe en el repo.
