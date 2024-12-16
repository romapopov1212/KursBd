from fastapi import APIRouter, Depends
from models.purchase import Purchase
from services.products import ProductsService
router = APIRouter(
    prefix="/shop/purchases"
)


@router.post("/purchase/")
async def create_purchase(
        purchase: Purchase,
        service: ProductsService = Depends()
):
    return await service.make_purchase(
        buyer_number=purchase.buyer_number,
        products_to_buy=purchase.products
    )
