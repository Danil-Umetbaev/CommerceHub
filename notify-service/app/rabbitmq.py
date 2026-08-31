import aio_pika
import json
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractExchange, AbstractIncomingMessage, AbstractConnection
from app.database import SessionLocal
from app.schemas import NotifyCreateSchema
from app.services import NotifyService
from app.config import get_settings


settings = get_settings()


async def handle_payment_events(message: AbstractIncomingMessage):
    async with message.process():
        event = json.loads(message.body.decode("utf-8"))
        data = {'order_id': event['order_id'], 'title': 'Ваш заказ оформлен', 'message': 'My ego sobiryaem'}
        notify = NotifyCreateSchema.model_validate(data)
        async with SessionLocal() as db:
            await NotifyService(db).create_notify(notify)
            print('✅ Уведомление создано в БД')

async def connect_rabbitmq(url: str) -> AbstractRobustConnection:
    return await aio_pika.connect_robust(url)

async def declare_payment_exchange(channel: AbstractChannel, exchange_name: str):
    return await channel.declare_exchange(exchange_name)

async def event_publish_json(exchange: AbstractExchange, routing_key: str, data: dict):
    message = aio_pika.Message(json.dumps(data).encode())
    await exchange.publish(message, routing_key)


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
    print(f"✅ Очередь {settings.payment_queue_name} готова к приёму сообщений в notify-service")