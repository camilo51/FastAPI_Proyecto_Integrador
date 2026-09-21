"""Middleware HTTP para trazabilidad de las solicitudes."""

import logging
import time
from uuid import uuid4

from fastapi import Request
from starlette.responses import Response

logger = logging.getLogger("app.requests")


async def request_context_middleware(request: Request, call_next) -> Response:
    """Añade trazabilidad y registra el resultado de cada solicitud HTTP."""
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    started_at = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.exception(
            "%s %s -> 500 (%.2f ms) [request_id=%s]",
            request.method,
            request.url.path,
            elapsed_ms,
            request_id,
        )
        raise

    elapsed_ms = (time.perf_counter() - started_at) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
    logger.info(
        "%s %s -> %s (%.2f ms) [request_id=%s]",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
        request_id,
    )
    return response
