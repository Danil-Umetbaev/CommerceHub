from fastapi import APIRouter
from app.schemas.catalog import ProductSchemas

from app.api_client import request_service
from app.config import settings
router = APIRouter(prefix='/products')

@router.get("", response_model=list[ProductSchemas])
async def get_products():
    return await request_service('GET', url=f'{settings.CATALOG_SERVICE_URL}/products')


@router.get("/{id_product}", response_model=ProductSchemas)
async def get_product(
    id_product: str,
):
    return await request_service('GET', url=f'{settings.CATALOG_SERVICE_URL}/products/{id_product}')


