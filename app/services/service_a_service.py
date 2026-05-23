from __future__ import annotations

from app.infrastructure.service_a_client import ServiceAClient
from app.schemas.service_a_api import (
    ServiceACreateOrderRequest,
    ServiceACreateOrderResponse,
    ServiceAQueryDataResponse,
)


class ServiceAService:
    def __init__(self, client: ServiceAClient) -> None:
        self._client = client

    async def query_data(
        self,
        keyword: str,
        page: int = 1,
        size: int = 10,
    ) -> ServiceAQueryDataResponse:
        return await self._client.get_data(keyword=keyword, page=page, size=size)

    async def create_order(
        self,
        name: str,
        amount: int,
    ) -> ServiceACreateOrderResponse:
        req = ServiceACreateOrderRequest(name=name, amount=amount)
        return await self._client.create_order(req)
