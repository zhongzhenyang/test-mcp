from __future__ import annotations

from enum import StrEnum


class ErrorCode(StrEnum):
    INTERNAL_ERROR = "INTERNAL_ERROR"
    CONFIG_ERROR = "CONFIG_ERROR"
    SERVICE_A_ERROR = "SERVICE_A_ERROR"
    SERVICE_A_AUTH_ERROR = "SERVICE_A_AUTH_ERROR"
    SERVICE_A_REQUEST_ERROR = "SERVICE_A_REQUEST_ERROR"
    SERVICE_A_RESPONSE_ERROR = "SERVICE_A_RESPONSE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"


class AppError(Exception):
    error_code: ErrorCode = ErrorCode.INTERNAL_ERROR

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ConfigError(AppError):
    error_code = ErrorCode.CONFIG_ERROR


class ServiceAError(AppError):
    error_code = ErrorCode.SERVICE_A_ERROR


class ServiceAAuthError(ServiceAError):
    error_code = ErrorCode.SERVICE_A_AUTH_ERROR


class ServiceARequestError(ServiceAError):
    error_code = ErrorCode.SERVICE_A_REQUEST_ERROR


class ServiceAResponseError(ServiceAError):
    error_code = ErrorCode.SERVICE_A_RESPONSE_ERROR
