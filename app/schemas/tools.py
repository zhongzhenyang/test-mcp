from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.common import ToolResponse
from app.schemas.service_a_api import (
    ServiceACreateOrderResponse,
    ServiceAQueryDataResponse,
)


class QueryServiceADataToolInput(BaseModel):
    keyword: str = Field(..., description="查询关键字")
    page: int = Field(1, ge=1, description="页码，从1开始")
    size: int = Field(10, ge=1, le=100, description="每页数量")


class QueryServiceADataToolOutput(ToolResponse[ServiceAQueryDataResponse]):
    pass


class CreateServiceAOrderToolInput(BaseModel):
    name: str = Field(..., min_length=1, description="订单名称")
    amount: int = Field(..., ge=1, description="订单数量")


class CreateServiceAOrderToolOutput(ToolResponse[ServiceACreateOrderResponse]):
    pass
