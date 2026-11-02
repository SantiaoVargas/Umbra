# Dominio guardia: allowlist fail-closed

**Fecha ficha:** 2026-11-02 · **Versión:** v1 (diseño) · **Rama leída:** `feature/001-allowlist` · **Cobertura:** solo diseño; **no existe código todavía** (todo lo de abajo es el plan de `specs/001_allowlist/spec.md`).
Marcas: **observado**, **<persona>** (fecha), **hipótesis**.

## 1. Propósito
Decide si una URL puede recibir tráfico de Umbra. Protege la regla **P1**: un typo o un host ajeno nunca debe ser escaneado. (`docs/constitution.md` §2.)

## 2. Recorrido
Config (`umbra.config.json`) → `Allowlist` → `is_allowed(url)` → `True`/`False`. Sin código aún. — **hipótesis** (spec 001, borrador).

## 3. Componentes
- Módulos/archivos: `src/umbra/core/allowlist.py` (por crear).
- Tests: `tests/test_allowlist.py` (por crear).

## 4. Contratos y datos
Formato de config y firmas en `specs/001_allowlist/spec.md` (sección Contrato). Todavía no hay contrato estable en `../contratos/`.

## 5. Reglas de negocio e invariantes
- Lo que no está en la lista se bloquea (fail-closed). — Santiago (2026-11-02). Protege P1.
- Subdominios solo con `incluir_subdominios: true`. — Santiago (2026-11-02).
- La identidad es host + puerto; sin puerto en la entrada solo 80 y 443. — Santiago (2026-11-02).
- Comparar siempre el host parseado por partes, nunca por texto contenido. — Santiago (2026-11-02), caso `evil-example.com`.

## 6. Tests existentes
Ninguno todavía.

## 7. Discrepancias doc vs código
Ninguna (no hay código).

## 8. Riesgos y deuda
- La 002 debe revalidar cada redirección con `is_allowed` (P1). Va como criterio de la spec 002.

## 9. Decisiones y pendientes
Ver spec 001 §Decisiones abiertas. Al cerrar la historia se anota en `decisiones.md`.
