from __future__ import annotations

from contextvars import ContextVar
from uuid import uuid4

_request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")


def set_request_id(request_id: str) -> None:
    _request_id_ctx.set(request_id)


def get_request_id() -> str:
    value = _request_id_ctx.get()
    if value:
        return value
    new_id = uuid4().hex
    _request_id_ctx.set(new_id)
    return new_id


def new_request_id() -> str:
    request_id = uuid4().hex
    _request_id_ctx.set(request_id)
    return request_id
