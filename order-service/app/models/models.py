from datetime import datetime, time

from .base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, func


class OrderORM(Base):
    __tablename__ = "orders"

    user_id: Mapped[str]
    status: Mapped[str]
    total_amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    items: Mapped[list[OrderItemORM]] = relationship('OrderItemORM', back_populates='order')

class OrderItemORM(Base):
    __tablename__ = 'order_items'

    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[str]
    product_name: Mapped[str]
    quantity: Mapped[int]
    unit_price: Mapped[int]
    order: Mapped[OrderORM] = relationship('OrderORM', back_populates='items')