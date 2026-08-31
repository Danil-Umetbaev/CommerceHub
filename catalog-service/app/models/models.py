from .base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class ProductORM(Base):
    __tablename__ = "products"

    name: Mapped[str]= mapped_column(String)
    description: Mapped[str]= mapped_column(String)
    price: Mapped[int]
    image: Mapped[str] = mapped_column(String)
    category: Mapped[str]= mapped_column(String)