from app.repositories.product import ProductRepository
from app.schemas import ProductCreateSchemas, ProductPartialUpdateSchemas
from sqlalchemy.orm import Session

class ProductServices:

    def __init__(self, db: Session):
        self.db = db

    def get_products(self):
        return ProductRepository(self.db).get_all()
    def get_product_or_none(self, id_product: int | str):
        return ProductRepository(self.db).get_one_or_none(id_product)

    def add_product(self, obj: ProductCreateSchemas):
        result = ProductRepository(self.db).add(obj)
        self.db.commit()
        return result

    def update_product(self, obj: ProductPartialUpdateSchemas, exclude_unset=True, **filter_by):
        result = ProductRepository(self.db).update(obj, exclude_unset=exclude_unset, **filter_by)
        self.db.commit()
        return result

    def delete_product(self, id_obj: str):
        result = ProductRepository(self.db).delete(id_obj)
        self.db.commit()
        return result




