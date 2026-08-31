from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine
from app.routers import router as UserRouter
from app.config import settings


@asynccontextmanager
async def lifespan(_app: FastAPI):
    from app.models.base import Base
    async with engine.begin() as database_connection:
        await database_connection.run_sync(Base.metadata.create_all)
    yield

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["127.0.0.1"],
        allow_methods=["*"],
        allow_headers=['*'],
        allow_credentials=True
    )
    app.include_router(UserRouter)

    return app

app = create_app()

