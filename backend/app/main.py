from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.include_router(api_router)

    @app.get("/")
    def read_root() -> dict[str, str]:
        return {"message": "ForestTalk backend is running."}

    return app


app = create_app()
