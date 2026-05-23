from __future__ import annotations

from pydantic import BaseModel, Field


class ServiceALoginRequest(BaseModel):
    username: str = Field(..., description="服务A登录用户名")
    password: str = Field(..., description="服务A登录密码")


class ServiceALoginResponse(BaseModel):
    token: str = Field(..., description="服务A认证token")
