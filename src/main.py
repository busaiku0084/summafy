from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions import TranslationError, TranslationTimeoutError
from src.routers import translate

app = FastAPI(title="Summafy", version="0.1.0")
app.include_router(translate.router)


@app.exception_handler(TranslationTimeoutError)
async def timeout_handler(
    _request: Request, exc: TranslationTimeoutError
) -> JSONResponse:
    return JSONResponse(status_code=504, content={"detail": str(exc)})


@app.exception_handler(TranslationError)
async def translation_error_handler(
    _request: Request, exc: TranslationError
) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
