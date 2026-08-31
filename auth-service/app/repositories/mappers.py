from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from app.models.models import UserORM
from app.schemas import UserReadSchema

class BaseDataMapper:
    schema = BaseModel
    model = DeclarativeBase
    @classmethod
    def map_orm_to_schema(cls, orm_obj: DeclarativeBase):
        return cls.schema.model_validate(orm_obj, from_attributes=True)

    @classmethod
    def map_schema_to_orm(cls, schema_obj: BaseModel):
        return cls.model(**schema_obj.model_dump())


class PaymentDataMapper(BaseDataMapper):
    schema =  UserReadSchema
    model = UserORM
