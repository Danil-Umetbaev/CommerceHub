from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine
from app.routers import router as PaymentRouter
from app.rabbitmq import declare_payment_exchange, connect_rabbitmq
from app.config import get_settings
from app.kafka import create_kafka_producer
settings = get_settings()

@asynccontextmanager
async def lifespan(_app: FastAPI):
    from app.models.base import Base
    async with engine.begin() as database_connection:
        await database_connection.run_sync(Base.metadata.create_all)
    rabbitmq_connection = await connect_rabbitmq(settings.rabbitmq_url)
    rabbitmq_channel = await rabbitmq_connection.channel()
    _app.state.payment_exchange = await declare_payment_exchange(rabbitmq_channel, settings.payment_exchange_name)

    kafka_producer = create_kafka_producer()
    await kafka_producer.start()
    _app.state.kafka_producer = kafka_producer

    try:
        yield
    finally:
        kafka_producer.stop()
        rabbitmq_channel.close()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["127.0.0.1"],
        allow_methods=["*"],
        allow_headers=['*'],
        allow_credentials=True
    )
    app.include_router(PaymentRouter)

    return app

app = create_app()

