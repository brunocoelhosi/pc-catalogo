import json
import traceback

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pclogging import LoggingBuilder
from pydantic_core import ValidationError

from app.common.app_error_codes import ErrorCodes, ErrorInfo
from app.common.error_schema import ErrorDetail, ErrorResponse
from app.common.exceptions import ApplicationException

logger = LoggingBuilder.get_logger(__name__)


def get_error_response(error: ErrorInfo, details: list[ErrorDetail] | None = None) -> ErrorResponse:
    return ErrorResponse(slug=error.slug, message=error.message, details=details)


async def _get_request_body(request: Request) -> dict | None:
    request_body = None
    try:
        request_body = await request.body()
        request_output = json.loads(await request.body())
    except Exception as ex:
        logger.error("⚠ Falha ao decodificar o corpo da requisicao", extra={"exception": str(ex)})
        # XXX Revisar este aqui
        request_output = str(request_body) if request_body is not None else None
    return request_output


async def _get_request_info(request: Request) -> dict:
    return {
        "method": request.method,
        "url": request.url,
        "query": request.query_params,
        "content": await _get_request_body(request),
    }


def add_error_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_, exc: HTTPException):
        logger.error("⚠ Falha HTTP: ", extra={"exception": str(exc)})
        response = get_error_response(ErrorCodes.SERVER_ERROR.value)
        return JSONResponse(
            status_code=exc.status_code,
            headers=exc.headers,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        logger.warning("⚠ Falha na validacao da requisicao", extra={"exception": str(exc)})
        errors = exc.errors()
        details: list[ErrorDetail] = []
        for error in errors:
            ctx = error.get("ctx", {})

            details.append(
                ErrorDetail(
                    **{
                        "message": error["msg"],
                        "location": error["loc"][0],
                        "slug": error["type"],
                        "field": ", ".join(map(str, error["loc"][1:])),
                        "ctx": ctx,
                    }
                )
            )

        response = get_error_response(ErrorCodes.UNPROCESSABLE_ENTITY.value, details=details)

        return JSONResponse(
            status_code=ErrorCodes.UNPROCESSABLE_ENTITY.http_code,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    @app.exception_handler(ValidationError)
    async def request_pydantic_validation_error_handler(request: Request, exc: RequestValidationError):
        """Handler para erros de validação do Pydantic"""
        
        errors = []
        for error in exc.errors():

            # ✅ Debug: Mostrar valores
            logger.error(f"🔍 Error location: {error.get('loc')}")
            logger.error(f"🔍 Error type: {error.get('type')}")
            logger.error(f"🔍 Error msg: {error.get('msg')}")

            # ✅ CORREÇÃO: Criar dict diretamente sem validação Pydantic
            try:
                error_detail = {
                    "location": "body",  # ✅ Valor fixo válido
                    "message": error.get('msg', 'Validation error'),
                    "type": error.get('type', 'validation_error'),
                    "field": error.get('loc', [])
                }
                errors.append(error_detail)
            except Exception as e:
                logger.error(f"❌ Erro ao criar ErrorDetail: {e}")
                # ✅ Fallback seguro
                errors.append({
                    "location": "body",
                    "message": str(error.get('msg', 'Validation error')),
                    "type": str(error.get('type', 'validation_error'))
                })
        
        return JSONResponse(
            status_code=422,
            content={
                "detail": errors
            }
        )

    @app.exception_handler(Exception)
    async def default_validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        response = get_error_response(ErrorCodes.SERVER_ERROR.value)
        # XXX
        logger.error("🪲 Falha nao capturada", extra={"exception": str(exc)})
        traceback.print_exc()

        return JSONResponse(
            status_code=ErrorCodes.SERVER_ERROR.http_code,
            content=response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )

    @app.exception_handler(ApplicationException)
    async def application_exception_handler(_, exc: ApplicationException):
        logger.error("⚠ Falha na aplicacao", extra={"status_code": exc.status_code, "trace": exc.details})
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.error_response.model_dump(mode="json", exclude_none=True, exclude_unset=True),
        )