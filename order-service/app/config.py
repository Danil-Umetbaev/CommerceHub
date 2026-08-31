import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    database_url: str
    base_url_catalog_client: str
    base_url_payment_client: str
    rabbitmq_url: str
    payment_succeeded_routing_key: str
    payment_exchange_name: str
    payment_queue_name: str


def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://orders:orders@order-db:5432/orders"
        ),
        base_url_catalog_client=os.getenv(
            "BASE_URL_CATALOG_CLIENT",
            "http://catalog-service:8000/products"
        ),
        base_url_payment_client=os.getenv(
            "BASE_URL_CATALOG_PAYMENT",
            "http://payment-service:8000/payments"
        ),
        rabbitmq_url=os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672"),
        payment_succeeded_routing_key=os.getenv("PAYMENT_SUCCEEDED_ROUTING_KEY", "payment.succeeded"),
        payment_exchange_name=os.getenv("PAYMENT_EXCHANGE_NAME", "payment.events"),
        payment_queue_name=os.getenv("PAYMENT_QUEUE_NAME", "payment.results")

    )