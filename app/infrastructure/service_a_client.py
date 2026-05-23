from __future__ import annotations

import time
from typing import Any, Optional

import httpx

from app.config import Settings
from app.exceptions import (
    ServiceAAuthError,
    ServiceARequestError,
    ServiceAResponseError,
)
from app.logging import get_logger
from app.schemas.service_a_auth import ServiceALoginResponse
from app.schemas.service_a_api import (
    ServiceACreateOrderRequest,
    ServiceACreateOrderResponse,
    ServiceAQueryDataResponse,
)

logger = get_logger(__name__)


class ServiceAClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._token: Optional[str] = None
        self._client = httpx.AsyncClient(
            base_url=settings.service_a_base_url,
            timeout=settings.http_timeout,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def login(self) -> str:
        payload = {
            "username": self._settings.service_a_username,
            "password": self._settings.service_a_password,
        }

        logger.info(
            "login service_a start",
            extra={"extra_data": {"event": "service_a_login_start"}},
        )

        start = time.perf_counter()
        try:
            response = await self._client.post("/login", json=payload)
        except httpx.HTTPError as e:
            logger.exception(
                "login service_a http error",
                extra={"extra_data": {"event": "service_a_login_http_error"}},
            )
            raise ServiceAAuthError(f"调用服务A登录接口失败: {e}") from e

        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        if response.status_code != 200:
            logger.error(
                "login service_a failed",
                extra={
                    "extra_data": {
                        "event": "service_a_login_failed",
                        "status_code": response.status_code,
                        "duration_ms": duration_ms,
                        "response_text": response.text,
                    }
                },
            )
            raise ServiceAAuthError(
                f"服务A登录失败, status={response.status_code}, body={response.text}"
            )

        try:
            parsed = ServiceALoginResponse.model_validate(response.json())
        except Exception as e:
            logger.exception(
                "login service_a parse response failed",
                extra={"extra_data": {"event": "service_a_login_parse_failed"}},
            )
            raise ServiceAResponseError(f"解析服务A登录响应失败: {e}") from e

        self._token = parsed.token

        logger.info(
            "login service_a success",
            extra={
                "extra_data": {
                    "event": "service_a_login_success",
                    "duration_ms": duration_ms,
                }
            },
        )
        return self._token

    async def _ensure_token(self) -> str:
        if self._token:
            return self._token
        return await self.login()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> Any:
        token = await self._ensure_token()
        headers = {"Authorization": f"Bearer {token}"}

        start = time.perf_counter()
        try:
            response = await self._client.request(
                method=method,
                url=path,
                params=params,
                json=json,
                headers=headers,
            )
        except httpx.HTTPError as e:
            logger.exception(
                "service_a request http error",
                extra={
                    "extra_data": {
                        "event": "service_a_request_http_error",
                        "method": method,
                        "path": path,
                    }
                },
            )
            raise ServiceARequestError(f"调用服务A接口失败: {e}") from e

        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        if response.status_code == 401:
            logger.warning(
                "service_a request got 401, retry after relogin",
                extra={
                    "extra_data": {
                        "event": "service_a_request_401",
                        "method": method,
                        "path": path,
                        "duration_ms": duration_ms,
                    }
                },
            )

            new_token = await self.login()
            retry_headers = {"Authorization": f"Bearer {new_token}"}

            retry_start = time.perf_counter()
            try:
                response = await self._client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json,
                    headers=retry_headers,
                )
            except httpx.HTTPError as e:
                logger.exception(
                    "service_a retry request http error",
                    extra={
                        "extra_data": {
                            "event": "service_a_retry_http_error",
                            "method": method,
                            "path": path,
                        }
                    },
                )
                raise ServiceARequestError(f"重试调用服务A接口失败: {e}") from e

            duration_ms = round((time.perf_counter() - retry_start) * 1000, 2)

        if response.status_code >= 400:
            logger.error(
                "service_a request failed",
                extra={
                    "extra_data": {
                        "event": "service_a_request_failed",
                        "method": method,
                        "path": path,
                        "status_code": response.status_code,
                        "duration_ms": duration_ms,
                        "response_text": response.text,
                    }
                },
            )
            raise ServiceARequestError(
                f"服务A请求失败, method={method}, path={path}, status={response.status_code}, body={response.text}"
            )

        logger.info(
            "service_a request success",
            extra={
                "extra_data": {
                    "event": "service_a_request_success",
                    "method": method,
                    "path": path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                }
            },
        )

        try:
            return response.json()
        except Exception as e:
            logger.exception(
                "service_a response parse failed",
                extra={
                    "extra_data": {
                        "event": "service_a_response_parse_failed",
                        "method": method,
                        "path": path,
                    }
                },
            )
            raise ServiceAResponseError(f"解析服务A响应JSON失败: {e}") from e

    async def get_data(
        self,
        keyword: str,
        page: int = 1,
        size: int = 10,
    ) -> ServiceAQueryDataResponse:
        data = await self._request(
            "GET",
            "/api/data",
            params={"keyword": keyword, "page": page, "size": size},
        )
        try:
            return ServiceAQueryDataResponse.model_validate(data)
        except Exception as e:
            raise ServiceAResponseError(f"解析查询数据响应失败: {e}") from e

    async def create_order(
        self,
        req: ServiceACreateOrderRequest,
    ) -> ServiceACreateOrderResponse:
        data = await self._request(
            "POST",
            "/api/orders",
            json=req.model_dump(),
        )
        try:
            return ServiceACreateOrderResponse.model_validate(data)
        except Exception as e:
            raise ServiceAResponseError(f"解析创建订单响应失败: {e}") from e
