from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import ProductCreateSchemas, ProductSchemas, ProductPartialUpdateSchemas, ProductUpdateSchemas
from app.services import ProductServices
from app.database import get_db
router = APIRouter(prefix='/products')

@router.get("", response_model=list[ProductSchemas])
def get_products(
    db: Session=Depends(get_db)
):
    return ProductServices(db).get_products()


@router.get("/{id_product}", response_model=ProductSchemas)
def get_product(
    id_product: str,
    db: Session=Depends(get_db)
):
    return ProductServices(db).get_product_or_none(id_product)


@router.post("/")
def add_product(
    product: ProductCreateSchemas,
    db: Session=Depends(get_db)
):
    return ProductServices(db).add_product(product)


@router.put("/{id_product}")
def update_product(
    id_product: str,
    product: ProductUpdateSchemas,
    db: Session=Depends(get_db)
):
    return ProductServices(db).update_product(product, exclude_unset=False, id=id_product)


@router.patch("/{id_product}")
def partial_update_product(
    id_product: str,
    product: ProductPartialUpdateSchemas,
    db: Session=Depends(get_db)
):
    return ProductServices(db).update_product(product, exclude_unset=True, id=id_product)

@router.delete("/{id_product}")
def delete_product(
    id_product: str,
    db: Session=Depends(get_db)
):
    return ProductServices(db).delete_product(id_product)




