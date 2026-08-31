from app.repositories.repositories import OrderItemRepository, OrderRepository
from app.schemas import OrderSchema, OrderCreateSchema, OrderItemSchema, OrderItemCreateSchema, OrderUpdateSchema
from sqlalchemy.orm import Session
from app.catalog_client import CatalogClient
from app.payment_client import PaymentClient
from app.config import get_settings
from app.models.models import OrderItemORM, OrderORM
import httpx
from fastapi import HTTPException
settings = get_settings()
class OrderService:

    def __init__(self, db: Session):
        self.db = db

    def get_orders(self):
        return OrderRepository(self.db).get_all()

    def get_order_or_none(self, id_order: int | str):
        return OrderRepository(self.db).get_one_or_none(id_order)

    def add_order(self, obj: OrderCreateSchema):
        catalog_client = CatalogClient(settings.base_url_catalog_client)
        products = []
        total_amount = 0
        try:
            for item in obj.items:
                product = catalog_client.get_product(item.product_id)
                products.append(
                    {
                        "product_id" : item.product_id,
                        "product_name": product['name'],
                        "quantity" : item.quantity,
                        "unit_price" : product['price'],
                    }
                )
                total_amount += product['price'] * item.quantity
            order_orm = OrderORM(user_id=obj.user_id, total_amount=total_amount, status='created')
            order = OrderRepository(self.db).add(order_orm)
            self.db.flush()

            order_items = [OrderItemORM(order_id=order.id, **data) for data in products]
            self.db.add_all(order_items)
            self.db.commit()
            PaymentClient(settings.base_url_payment_client).create_payment(order_orm.id, order_orm.user_id, order_orm.total_amount)
            return order
        except httpx.HTTPStatusError as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Ошибка сервиса товаров: {e.response.text}")
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")

    # def update_order(self, obj: OrderUpdateSchema, exclude_unset=True, **filter_by):
    #     result = OrderRepository(self.db).update(obj, exclude_unset=exclude_unset, **filter_by)
    #     self.db.commit()
    #     return result

    # def delete_order(self, id_obj: str):
    #     result = OrderRepository(self.db).delete(id_obj)
    #     self.db.commit()
    #     return result
