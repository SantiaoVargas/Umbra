"""Tests del modelo de hallazgos y su regla dura de confianza."""

import pytest
from pydantic import ValidationError

from umbra.core.findings import Confidence, Finding, Severity


def test_finding_valido_se_crea():
    f = Finding(
        module="header_checker",
        title="Falta la cabecera HSTS",
        severity=Severity.MEDIUM,
        confidence=Confidence.CONFIRMED,
        evidence="La respuesta no incluye Strict-Transport-Security.",
        remediation="Agregar la cabecera HSTS en el servidor.",
    )
    assert f.severity is Severity.MEDIUM
    assert f.confidence is Confidence.CONFIRMED


def test_critical_sin_verificar_es_rechazado():
    # La regla dura del producto: un 'critical' jamás puede ser 'por-revisar'.
    with pytest.raises(ValidationError):
        Finding(
            module="demo",
            title="Algo sospechoso",
            severity=Severity.CRITICAL,
            confidence=Confidence.NEEDS_REVIEW,
            evidence="Solo un patrón, sin verificar.",
            remediation="Revisar manualmente.",
        )


def test_critical_confirmado_si_se_permite():
    # Un 'critical' SÍ puede existir, pero solo si está confirmado.
    f = Finding(
        module="demo",
        title="Vulnerabilidad verificada",
        severity=Severity.CRITICAL,
        confidence=Confidence.CONFIRMED,
        evidence="Verificado con una prueba activa.",
        remediation="Corregir de inmediato.",
    )
    assert f.severity is Severity.CRITICAL
