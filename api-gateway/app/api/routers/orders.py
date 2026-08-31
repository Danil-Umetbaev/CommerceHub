from fastapi import APIRouter, HTTPException, status

from app.config import settings
from app.auth import userIdDep
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))
from app.schemas.orders import  OrderCreateSchema, OrderSchema
from app.api_client import request_service
router = APIRouter(prefix='/orders')


@router.get("/{id_order}", response_model=OrderSchema)
async def get_order(
    id_order: str,
    cur_user: userIdDep
):
    order = await request_service('GET', f'{settings.ORDER_SERVICE_URL}/orders/{id_order}')
    ensure_order_owner(order, cur_user)
    return order

async def ensure_order_owner(order, cur_user_id: str):
    if not isinstance(order, dict) or order.get('user_id') != cur_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

@router.post("")
async def add_order(
    order: OrderCreateSchema,
    cur_user_id: userIdDep
):
    order_payload = order.model_dump(mode='json')
    order_payload["user_id"] = cur_user_id
    return await request_service('POST', f'{settings.ORDER_SERVICE_URL}/orders', json_data=order_payload)

