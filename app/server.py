from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from app.config import load_settings
from app.infrastructure.service_a_client import ServiceAClient
from app.lifespan import AppResources
from app.logging import setup_logging
from app.mcp_tools.service_a_tools import register_service_a_tools
from app.services.service_a_service import ServiceAService


def create_server() -> tuple[FastMCP, AppResources]:
    settings = load_settings()
    setup_logging(settings.log_level)

    mcp = FastMCP(settings.app_name)

    service_a_client = ServiceAClient(settings)
    service = ServiceAService(service_a_client)

    register_service_a_tools(mcp, service)

    resources = AppResources(service_a_client=service_a_client)
    return mcp, resources
