from app.models.base import Base
from app.repositories.mappers import BaseDataMapper
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from pydantic import BaseModel
from typing import Type

class BaseRepository:
    model = Type[Base]
    mapper: Type[BaseDataMapper]

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, *args, **kwargs):
        stmt = (
            select(self.model)
            .filter(*args)
            .filter_by(**kwargs)
        )
        result = self.db.scalars(stmt).all()
        return [self.mapper.map_orm_to_schema(obj) for obj in result]

    def get_one_or_none(self, id: int | str):
        result = self.db.get(self.model, id)
        if result:
            return self.mapper.map_orm_to_schema(result)
        return None

    def add(self, obj: BaseModel):
        obj_orm = self.mapper.map_schema_to_orm(obj)
        self.db.add(obj_orm)
        self.db.flush()
        return self.mapper.map_orm_to_schema(obj_orm)

    def update(self, obj: BaseModel, exclude_unset=True, **filter_by):
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**obj.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = self.db.scalars(stmt).one_or_none()
        self.db.flush()
        if result is None:
            return None
        return self.mapper.map_orm_to_schema(result)

    def delete(self, id_obj: str):
        obj = self.db.get(self.model, id_obj)
        self.db.delete(obj)
        self.db.flush()
        return self.mapper.map_orm_to_schema(obj)




