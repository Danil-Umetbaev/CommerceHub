from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import OrderCreateSchema, OrderSchema
from app.services import OrderService
from app.database import get_db
router = APIRouter(prefix='/orders')

@router.get("", response_model=list[OrderSchema])
def get_orders(
    db: Session=Depends(get_db)
):
    return OrderService(db).get_orders()


@router.get("/{id_order}", response_model=OrderSchema)
def get_order(
    id_order: str,
    db: Session=Depends(get_db)
):
    return OrderService(db).get_order_or_none(id_order)


@router.post("")
def add_order(
    order: OrderCreateSchema,
    db: Session=Depends(get_db),

):
    print(order, type(order))
    return OrderService(db).add_order(order)





@router.delete("/{id_order}")
def delete_order(
    id_product: str,
    db: Session=Depends(get_db)
):
    return None




