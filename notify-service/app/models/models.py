from datetime import datetime
from .base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func


class NotifyORM(Base):
    __tablename__ = 'notifyes'
    order_id: Mapped[str]
    title: Mapped[str]
    message: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False
    )


