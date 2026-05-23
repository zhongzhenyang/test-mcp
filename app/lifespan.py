from __future__ import annotations

from app.infrastructure.service_a_client import ServiceAClient


class AppResources:
    def __init__(self, service_a_client: ServiceAClient) -> None:
        self.service_a_client = service_a_client

    async def aclose(self) -> None:
        await self.service_a_client.aclose()
