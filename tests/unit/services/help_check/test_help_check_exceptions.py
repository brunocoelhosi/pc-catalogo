import pytest
from app.services.health_check.exceptions import (
    HealthCheckException,
    ServiceWarning,
    ServiceUnavailable,
    ServiceReturnedUnexpectedResult,
    InvalidConfigurationException,
)

def test_health_check_invalid_configuration():
    exc = InvalidConfigurationException(HealthCheckException)
    assert str(exc) == "unexpected configuration: <class 'app.services.health_check.exceptions.HealthCheckException'>"
    assert exc.message_type == "unexpected configuration" 

def test_health_check_exception_str():
    exc = HealthCheckException("erro genérico")
    assert str(exc) == "unknown error: erro genérico"
    assert exc.message == "erro genérico"

def test_service_warning_str():
    exc = ServiceWarning("serviço instável")
    assert str(exc) == "warning: serviço instável"
    assert exc.message_type == "warning"

def test_service_unavailable_str():
    exc = ServiceUnavailable("serviço fora do ar")
    assert str(exc) == "unavailable: serviço fora do ar"
    assert exc.message_type == "unavailable"

def test_service_returned_unexpected_result_str():
    exc = ServiceReturnedUnexpectedResult("resposta inesperada")
    assert str(exc) == "unexpected result: resposta inesperada"
    assert exc.message_type == "unexpected result"