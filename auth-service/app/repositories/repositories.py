from app.models.models import UserORM
from app.repositories.base import BaseRepository
from app.repositories.mappers import PaymentDataMapper
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status
from app.schemas import UserReadSchemaWithPassword
class UserRepository(BaseRepository):
    model = UserORM
    mapper = PaymentDataMapper

    async def get_user_by_email_with_password(self, *args, **kwargs):

        stmt = (
            select(self.model)
            .filter(*args)
            .filter_by(**kwargs)
        )
        try:
            result = (await self.db.scalars(stmt)).one()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': "Нет такого пользователя"})

        return UserReadSchemaWithPassword.model_validate(result, from_attributes=True)
