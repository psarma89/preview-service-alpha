from fastapi import Depends, FastAPI

from .core.auth import AuthContext, get_auth_context
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

    @app.get("/info")
    def info(
        settings: Settings = Depends(get_settings),
        auth: AuthContext = Depends(get_auth_context),
    ):
        return {
            "service": settings.service_name,
            "environment": settings.environment,
            "git_branch": settings.git_branch,
            "git_sha": settings.git_sha,
            "image_tag": settings.image_tag,
        }

    return app


app = create_app()
