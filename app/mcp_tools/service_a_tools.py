from __future__ import annotations

from pydantic import ValidationError

from app.context import get_request_id, new_request_id
from app.exceptions import AppError, ErrorCode
from app.logging import get_logger
from app.schemas.common import ErrorInfo
from app.schemas.tools import (
    CreateServiceAOrderToolInput,
    CreateServiceAOrderToolOutput,
    QueryServiceADataToolInput,
    QueryServiceADataToolOutput,
)
from app.services.service_a_service import ServiceAService

logger = get_logger(__name__)


def register_service_a_tools(mcp, service: ServiceAService) -> None:
    @mcp.tool(
        name="query_service_a_data",
        description="查询服务A的数据，支持关键字和分页参数",
    )
    async def query_service_a_data(input: QueryServiceADataToolInput) -> QueryServiceADataToolOutput:
        request_id = new_request_id()
        try:
            logger.info(
                "tool query_service_a_data called",
                extra={
                    "extra_data": {
                        "event": "tool_called",
                        "tool_name": "query_service_a_data",
                        "tool_input": input.model_dump(),
                    }
                },
            )
            result = await service.query_data(
                keyword=input.keyword,
                page=input.page,
                size=input.size,
            )
            return QueryServiceADataToolOutput(
                success=True,
                data=result,
                error=None,
                request_id=request_id,
            )
        except ValidationError as e:
            logger.exception("tool query_service_a_data validation failed")
            return QueryServiceADataToolOutput(
                success=False,
                data=None,
                error=ErrorInfo(code=ErrorCode.VALIDATION_ERROR, message=str(e)),
                request_id=get_request_id(),
            )
        except AppError as e:
            logger.exception("tool query_service_a_data failed")
            return QueryServiceADataToolOutput(
                success=False,
                data=None,
                error=ErrorInfo(code=e.error_code, message=e.message),
                request_id=get_request_id(),
            )
        except Exception as e:
            logger.exception("tool query_service_a_data unexpected failed")
            return QueryServiceADataToolOutput(
                success=False,
                data=None,
                error=ErrorInfo(code=ErrorCode.INTERNAL_ERROR, message=str(e)),
                request_id=get_request_id(),
            )

    @mcp.tool(
        name="create_service_a_order",
        description="调用服务A创建订单",
    )
    async def create_service_a_order(input: CreateServiceAOrderToolInput) -> CreateServiceAOrderToolOutput:
        request_id = new_request_id()
        try:
            logger.info(
                "tool create_service_a_order called",
                extra={
                    "extra_data": {
                        "event": "tool_called",
                        "tool_name": "create_service_a_order",
                        "tool_input": input.model_dump(),
                    }
                },
            )
            result = await service.create_order(
                name=input.name,
                amount=input.amount,
            )
            return CreateServiceAOrderToolOutput(
                success=True,
                data=result,
                error=None,
                request_id=request_id,
            )
        except ValidationError as e:
            logger.exception("tool create_service_a_order validation failed")
            return CreateServiceAOrderToolOutput(
                success=False,
                data=None,
                error=ErrorInfo(code=ErrorCode.VALIDATION_ERROR, message=str(e)),
                request_id=get_request_id(),
            )
        except AppError as e:
            logger.exception("tool create_service_a_order failed")
            return CreateServiceAOrderToolOutput(
                success=False,
                data=None,
                error=ErrorInfo(code=e.error_code, message=e.message),
                request_id=get_request_id(),
            )
        except Exception as e:
            logger.exception("tool create_service_a_order unexpected failed")
            return CreateServiceAOrderToolOutput(
                success=False,
                data=None,
                error=ErrorInfo(code=ErrorCode.INTERNAL_ERROR, message=str(e)),
                request_id=get_request_id(),
            )
