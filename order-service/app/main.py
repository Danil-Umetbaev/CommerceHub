from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine
from app.routers import router as OrderRouter
from app.config import get_settings
from app.rabbitmq import connect_rabbitmq, start_payment_consume


settings = get_settings()

@asynccontextmanager
async def lifespan(_app: FastAPI):
    from app.models.base import Base
    Base.metadata.create_all(bind=engine)
    connection = await connect_rabbitmq()
    await start_payment_consume(connection)

    try:
        yield
    finally:
        await connection.close()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["127.0.0.1"],
        allow_methods=["*"],
        allow_headers=['*'],
        allow_credentials=True
    )
    app.include_router(OrderRouter)

    return app

app = create_app()


