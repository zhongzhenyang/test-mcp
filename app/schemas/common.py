from __future__ import annotations

from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorInfo(BaseModel):
    code: str = Field(..., description="错误码")
    message: str = Field(..., description="错误信息")


class ToolResponse(BaseModel, Generic[T]):
    success: bool = Field(..., description="是否成功")
    data: Optional[T] = Field(default=None, description="成功时返回的数据")
    error: Optional[ErrorInfo] = Field(default=None, description="失败时返回的错误信息")
    request_id: str = Field(..., description="请求ID，便于日志排查")
