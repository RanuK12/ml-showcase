from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.config import get_settings


def add_cors(app: FastAPI) -> None:
    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
