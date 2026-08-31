from fastapi import APIRouter
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))
from app.api.routers.auth import router as authRouter
from app.api.routers.catalog import router as catalogRouter
from app.api.routers.orders import router as orderRouter
router = APIRouter(prefix='/api')


router.include_router(authRouter)
router.include_router(catalogRouter)
router.include_router(orderRouter)