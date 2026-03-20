from fastapi import Depends, FastAPI

from .routes import users_router
from .settings import Settings, get_settings


def create_app() -> FastAPI:
    app = FastAPI(title="service-alpha")

    app.include_router(users_router)

    @app.get("/health")
    def health(settings: Settings = Depends(get_settings)):
        return {
            "service": settings.service_name,
            "environment": settings.environment,
            "status": "ok",
        }

    return app


app = create_app()
