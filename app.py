from fastapi import FastAPI
from loguru import logger
from config import settings
from api.v1.routes import recommendations


def create_app() -> FastAPI:
    _app = FastAPI(**settings.fastapi_kwargs)
    logger.info("Starting application...")

    _app.include_router(recommendations.router, prefix="/api/v1")
    return _app


app: FastAPI = create_app()


@app.get("/")
async def root():
    return {"message": "Welcome to the Travel Recommendations API"}
