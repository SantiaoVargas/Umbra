"""Modelo de hallazgos (Finding) y su sistema de confianza.

Este es el corazón honesto de Umbra. Cada hallazgo lleva DOS etiquetas:

- `severity`: qué tan grave es el impacto.
- `confidence`: qué tan seguro está el motor de que es REAL.

El principio rector del producto ("nunca prometer más de lo que se verificó")
se hace cumplir acá, con código, no con buena voluntad.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, model_validator


class Severity(str, Enum):
    """Qué tan grave es el hallazgo (impacto)."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Confidence(str, Enum):
    """Qué tan seguro está el motor de que el hallazgo es real."""

    CONFIRMED = "confirmado"  # el motor lo verificó de verdad
    NEEDS_REVIEW = "por-revisar"  # solo encontró un patrón sospechoso


class Finding(BaseModel):
    """Un hallazgo del escaneo.

    Es inmutable en espíritu: se crea ya validado. Si rompe la regla dura de
    abajo, Pydantic no lo deja nacer.
    """

    module: str  # qué módulo lo encontró (ej: "header_checker")
    title: str  # resumen corto y legible
    severity: Severity
    confidence: Confidence
    evidence: str  # la prueba: qué se vio en la request/response
    remediation: str  # cómo arreglarlo

    @model_validator(mode="after")
    def _no_critical_sin_verificar(self) -> Finding:
        """Regla dura: un `critical` nunca puede ir como `por-revisar`.

        Si el motor no lo verificó, no tiene derecho a gritar "crítico". O se
        confirma, o se reporta con una severidad menor. Así el reporte no le
        miente al cliente.
        """
        if self.severity is Severity.CRITICAL and self.confidence is Confidence.NEEDS_REVIEW:
            raise ValueError(
                "Un hallazgo 'critical' no puede ser 'por-revisar': "
                "o se verifica (confirmado) o se reporta con severidad menor."
            )
        return self
