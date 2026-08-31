import aio_pika
from aio_pika.abc import AbstractConnection, AbstractRobustConnection, AbstractIncomingMessage
import json
from app.database import SessionLocal
from app.models.models import OrderORM

from app.config import get_settings


async def handle_payment_events(message: AbstractIncomingMessage):
    async with message.process():
        event = json.loads(message.body.decode("utf-8"))
        with SessionLocal() as session:
            order = session.get(OrderORM, event["order_id"])
            order.status = 'paid'
            session.commit()

settings = get_settings()

async def connect_rabbitmq() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(
        settings.rabbitmq_url,
        client_properties={
            "capabilities": {
                "transient_nonexcl_queues": False
            }
        }
    )

async def start_payment_consume(connection: AbstractConnection):
    channel = await connection.channel()
    payment_exchange = await channel.declare_exchange(settings.payment_exchange_name)
    payment_queue = await channel.declare_queue(
        settings.payment_queue_name,
        durable=True,           # сохранять при перезапуске
        exclusive=False,        # не эксклюзивная
        auto_delete=False,      # не удалять автоматически
        arguments={
            "x-queue-type": "classic"   # или "quorum" – но classic работает всегда
        }
    )


    await payment_queue.bind(payment_exchange, routing_key=settings.payment_succeeded_routing_key)
    await payment_queue.consume(handle_payment_events)