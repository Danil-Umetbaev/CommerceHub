from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine
from app.routers import router as NotifyRouter
from app.rabbitmq import declare_payment_exchange, connect_rabbitmq, start_payment_consume
from app.config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(_app: FastAPI):
    from app.models.base import Base
    async with engine.begin() as database_connection:
        await database_connection.run_sync(Base.metadata.create_all)
    connection = await connect_rabbitmq(settings.rabbitmq_url)
    channel = await connection.channel()
    await start_payment_consume(connection)
    _app.state.payment_exchange = await declare_payment_exchange(channel, settings.payment_exchange_name)
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
    app.include_router(NotifyRouter)

    return app

app = create_app()

