from pydantic import BaseModel, ConfigDict
from datetime import datetime


class OrderCreateSchema(BaseModel):
    items: list[OrderItemCreateSchema]
    model_config = ConfigDict(from_attributes=True)

class OrderUpdateSchema(BaseModel):
    items: list[OrderItemSchema]
    model_config = ConfigDict(from_attributes=True)

class OrderSchema(BaseModel):
    id: str
    user_id: str
    status: str
    total_amount: int
    created_at: datetime
    items: list[OrderItemSchema]
    model_config = ConfigDict(from_attributes=True)


class OrderItemSchema(BaseModel):
    id: str
    order_id: str
    product_id: str
    quantity: int
    unit_price: int
    model_config = ConfigDict(from_attributes=True)

class OrderItemCreateSchema(BaseModel):
    product_id: str
    quantity: int
    model_config = ConfigDict(from_attributes=True)

class OrderItemUpdateSchema(BaseModel):
    quantity: int



