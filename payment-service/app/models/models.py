from datetime import datetime

from .base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func


class PaymentORM(Base):
    __tablename__ = 'payments'
    user_id : Mapped[str]
    order_id: Mapped[str]
    status: Mapped[str]
    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

