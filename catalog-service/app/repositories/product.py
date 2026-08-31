from app.models.models import ProductORM
from app.repositories.base import BaseRepository
from app.repositories.mappers import ProductDataMapper

class ProductRepository(BaseRepository):
    model = ProductORM
    mapper = ProductDataMapper