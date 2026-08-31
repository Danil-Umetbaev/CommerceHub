from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))
from app.api.router import router as MainRouter

def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin,
        allow_methods=["*"],
        allow_headers=['*'],
        allow_credentials=False
    )
    app.include_router(MainRouter)

    return app

app = create_app()

