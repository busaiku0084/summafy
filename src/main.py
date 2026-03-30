from fastapi import FastAPI

from src.routers import translate

app = FastAPI(title="Summafy", version="0.1.0")
app.include_router(translate.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
