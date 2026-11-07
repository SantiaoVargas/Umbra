import pytest
from pydantic import ValidationError

from umbra.core.allowlist import Objetivo


def test_objetivo_rechaza_host_con_esquema():
    with pytest.raises(ValidationError):
        Objetivo(host="https://example.com")


def test_objetivo_rechaza_host_con_ruta_login():
    with pytest.raises(ValidationError):
        Objetivo(host="example.com/login")


def test_objetivo_rechaza_host_puerto():
    with pytest.raises(ValidationError):
        Objetivo(host="example.com:8080")
