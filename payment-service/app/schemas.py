import datetime

from pydantic import BaseModel, ConfigDict


class PaymentCreateSchema(BaseModel):
    order_id: str
    user_id: str
    amount: int
    model_config = ConfigDict(from_attributes=True)


class PaymentSchema(PaymentCreateSchema):
    id: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


