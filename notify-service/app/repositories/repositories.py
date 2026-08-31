from app.models.models import NotifyORM
from app.repositories.base import BaseRepository
from app.repositories.mappers import NotifyDataMapper

class NotifyRepository(BaseRepository):
    model = NotifyORM
    mapper = NotifyDataMapper

    # async def add(self, obj: NotifyORM):
    #     self.db.add(obj)
    #     await self.db.flush()
    #     return self.mapper.map_orm_to_schema(obj)

