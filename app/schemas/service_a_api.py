from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ServiceAQueryDataItem(BaseModel):
    id: str = Field(..., description="数据ID")
    name: str = Field(..., description="名称")
    extra: Optional[Dict[str, Any]] = Field(default=None, description="扩展字段")


class ServiceAQueryDataResponse(BaseModel):
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页数量")
    items: List[ServiceAQueryDataItem] = Field(default_factory=list, description="数据列表")


class ServiceACreateOrderRequest(BaseModel):
    name: str = Field(..., min_length=1, description="订单名称")
    amount: int = Field(..., ge=1, description="订单数量")


class ServiceACreateOrderResponse(BaseModel):
    order_id: str = Field(..., description="订单ID")
    status: str = Field(..., description="订单状态")
