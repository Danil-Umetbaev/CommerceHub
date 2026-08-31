from app.repositories.repositories import NotifyRepository
from app.schemas import NotifyCreateSchema, NotifyUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import get_settings
settings = get_settings()
class NotifyService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_notifyes(self):
        return await NotifyRepository(self.db).get_all()

    async def get_notify_or_none(self, id_order: str):
        return await NotifyRepository(self.db).get_one_or_none(id_order)

    async def create_notify(self, obj: NotifyCreateSchema):
        notify = await NotifyRepository(self.db).add(obj)
        await self.db.commit()
        return notify


    async def update_notify(self, obj: NotifyUpdateSchema, exclude_unset=True, **filter_by):
        result = await NotifyRepository(self.db).update(obj, exclude_unset=exclude_unset, **filter_by)
        await self.db.commit()
        return result

    async def delete_notify(self, id_obj: str):
        result = await NotifyRepository(self.db).delete(id_obj)
        await self.db.commit()
        return result
