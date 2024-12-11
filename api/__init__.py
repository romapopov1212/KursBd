from fastapi import APIRouter
from api.products import router as prod_router
router = APIRouter()

router.include_router(prod_router)