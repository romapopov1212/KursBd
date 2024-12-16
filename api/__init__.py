from fastapi import APIRouter
from api.products import router as prod_router
from api.buyers import router as buyer_router
from api.purchase import router as pur_router

router = APIRouter()

router.include_router(prod_router)
router.include_router(buyer_router)
router.include_router(pur_router)