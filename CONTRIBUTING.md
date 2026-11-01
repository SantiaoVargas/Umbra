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

## Flujo de Git (importante, somos dos)

1. Nunca trabajar directo sobre `main`.
2. Una rama por tarea: `git checkout -b fase-1-allowlist`.
3. Commits chicos y claros.
4. Abrir Pull Request y que el otro lo revise antes de mergear.
5. Como los módulos del motor son independientes, cada uno puede tomar una
   pieza distinta sin conflictos.
