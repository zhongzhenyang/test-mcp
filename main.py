from __future__ import annotations

import asyncio

from app.server import create_server


async def _run() -> None:
    mcp, resources = create_server()
    try:
        await mcp.run_async()
    finally:
        await resources.aclose()


if __name__ == "__main__":
    asyncio.run(_run())
