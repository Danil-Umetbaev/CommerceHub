from typing import Any

from pymongo import AsyncMongoClient

from app.config import settings

mongodb_client = AsyncMongoClient[Any](settings.mongodb_url)
events_collection = mongodb_client[settings.mongodb_database][settings.mongodb_collection]


