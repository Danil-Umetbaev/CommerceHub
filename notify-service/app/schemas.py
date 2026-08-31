import datetime

from pydantic import BaseModel, ConfigDict


class NotifyCreateSchema(BaseModel):
    order_id: str
    title: str
    message: str
    model_config = ConfigDict(from_attributes=True)


class NotifyUpdateSchema(NotifyCreateSchema):
    pass


class NotifySchema(NotifyCreateSchema):
    id: str
    order_id: str
    title: str
    message: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

