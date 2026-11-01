# Dominio confianza: modelo `Finding` (severidad vs. confianza)

**Fecha ficha:** 2026-11-01 · **Versión:** v1 · **Commit leído:** `8502e40` (main) · **Cobertura:** solo `core/findings.py`; el uso desde módulos y reporte está **sin verificar** (aún no existe).
Marcas: **observado**, **<persona>** (fecha), **hipótesis**.

## 1. Propósito
Cada hallazgo dice qué tan grave es (`severity`) y qué tan seguro está Umbra de que es real (`confidence`). Protege la regla **P2** y el principio rector: no prometer más de lo verificado. (README, `docs/DISENO-MOTOR.md` §4.)

## 2. Recorrido
Un módulo construye un `Finding`; Pydantic lo valida al crearse. Si es `critical` + `por-revisar`, lanza `ValidationError` y el hallazgo no nace. — observado: `src/umbra/core/findings.py` (`_no_critical_sin_verificar`).

## 3. Componentes
- `src/umbra/core/findings.py`: `Severity`, `Confidence`, `Finding`.
- Tests: `tests/test_findings.py` (3 tests).

## 4. Contratos y datos
`Finding`: `module`, `title`, `severity` (`info|low|medium|high|critical`), `confidence` (`confirmado|por-revisar`), `evidence`, `remediation`. — observado.
Sin esquema persistido todavía (ver idea I-006).

## 5. Reglas e invariantes
- `critical` ⇒ `confirmado` (observado: validador + `test_critical_sin_verificar_es_rechazado`, `test_critical_confirmado_si_se_permite`).
- Los valores de `Confidence` están en español (`confirmado`, `por-revisar`) y el JSON de la API los expondrá tal cual — **hipótesis**, confirmar en la spec 005/006.

## 6. Tests existentes
3 tests en `tests/test_findings.py`: hallazgo válido, `critical`+`por-revisar` rechazado, `critical`+`confirmado` permitido.

## 7. Discrepancias doc vs código
Ninguna observada.

## 8. Riesgos y deuda
- `evidence` es texto libre: un módulo podría volcar cookies/tokens (P5). Se define la redacción en la spec 002. **Hipótesis**, no hay M-NNN todavía.

## 9. Decisiones y pendientes
Ver `decisiones.md` (2026-11-01, principio rector).
