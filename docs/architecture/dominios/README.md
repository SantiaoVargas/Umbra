# Índice de dominios

Un dominio = una pieza del motor con una sola responsabilidad (ver `docs/DISENO-MOTOR.md`). La ficha de cada uno se crea/actualiza **cuando una historia lo toca**, desde `_plantilla.md`, solo con lo necesario.

| Dominio | Qué cubre | Código | Historias | Ficha |
|---|---|---|---|---|
| base | Esqueleto, tooling, CI | `pyproject.toml`, `src/umbra/__init__.py` | 000, M-001, M-002 | — |
| guardia | Allowlist, `is_allowed`, fail-closed | `core/allowlist.py` (por crear) | 001 | pendiente |
| cliente-http | Cliente httpx observador, evidencia | `core/http_client.py` (por crear) | 002 | pendiente |
| modulos | Interfaz común + módulos de detección | `core/modules/` (por crear) | 003, 004, I-001..003 | pendiente |
| confianza | Modelo `Finding`, severidad vs. confianza | `core/findings.py` | 000 | [confianza.md](confianza.md) v1 2026-11-01 |
| reporte | Reporte MD/JSON, plan priorizado | `core/report.py` (por crear) | 005 | pendiente |
| api | FastAPI, endpoints, schemas | `src/umbra/api/` | 006 | pendiente |
| frontend | React | `frontend/` (por crear) | 007 | pendiente |

Marcas en las fichas: **observado**, **<persona>** (fecha), **hipótesis**.
