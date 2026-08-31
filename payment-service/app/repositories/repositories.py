from app.models.models import PaymentORM
from app.repositories.base import BaseRepository
from app.repositories.mappers import PaymentDataMapper

class PaymentRepository(BaseRepository):
    model = PaymentORM
    mapper = PaymentDataMapper

    async def add(self, obj: PaymentORM):
        self.db.add(obj)
        await self.db.flush()
        return self.mapper.map_orm_to_schema(obj)

