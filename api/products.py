from fastapi import APIRouter
from fastapi import Depends

from services.products import ProductsService
from models.products import Product
router = APIRouter(
    prefix="/shop/products"
)

@router.post("/add_product")
async def add_product(
        prod_data: Product,
        service: ProductsService=Depends()
):
    return await service.add_product(prod_data)