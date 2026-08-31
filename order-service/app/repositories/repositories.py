from app.models.models import OrderORM, OrderItemORM
from app.repositories.base import BaseRepository
from app.repositories.mappers import OrderDataMapper, OrderItemDataMapper
from app.models.base import Base

class OrderRepository(BaseRepository):
    model = OrderORM
    mapper = OrderDataMapper

    def add(self, obj: Base):
        self.db.add(obj)
        self.db.flush()
        return self.mapper.map_orm_to_schema(obj)


class OrderItemRepository(BaseRepository):
    model = OrderItemORM
    mapper = OrderItemDataMapper