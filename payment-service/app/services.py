import asyncio
from uuid import uuid4
from aio_pika.abc import AbstractExchange
from fastapi import Request
from app.repositories.repositories import PaymentRepository
from app.schemas import PaymentCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import get_settings
from app.models.models import PaymentORM
from app.rabbitmq import event_publish_json
from app.events import build_payment_succeeded_event
from app.kafka import publish_kafka_event, create_kafka_producer
from aiokafka import AIOKafkaProducer
settings = get_settings()
class PaymentService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_payments(self):
        return await PaymentRepository(self.db).get_all()

    async def get_payment_or_none(self, id_order: int | str):
        return await PaymentRepository(self.db).get_one_or_none(id_order)

    async def create_payment(self,  obj: PaymentCreateSchema):
        payment = PaymentORM(**obj.model_dump(), status='created')
        await PaymentRepository(self.db).add(payment)
        await self.db.commit()
        return payment

    async def complete_payment(self,payment: PaymentORM, exchange: AbstractExchange, kafka_producer: AIOKafkaProducer):
        await asyncio.sleep(3)
        payment.status = 'succeeded'
        await self.db.commit()

        event = build_payment_succeeded_event(payment.id, payment.order_id, payment.user_id, payment.amount)
        await event_publish_json(exchange, settings.payment_succeeded_routing_key, event)

        await publish_kafka_event(kafka_producer, settings.kafka_analytic_payment_topic, event)
