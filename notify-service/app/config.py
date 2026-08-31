import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    database_url: str
    rabbitmq_url: str
    payment_succeeded_routing_key: str
    payment_exchange_name: str
    payment_queue_name: str


def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/notify_microservices"
        ),
        rabbitmq_url=os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672"),
        payment_succeeded_routing_key=os.getenv("PAYMENT_SUCCEEDED_ROUTING_KEY", "payment.succeeded"),
        payment_exchange_name=os.getenv("PAYMENT_EXCHANGE_NAME", "payment.events"),
        payment_queue_name=os.getenv("PAYMENT_QUEUE_NAME", "payment.notify")
    )