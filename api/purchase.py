from fastapi import APIRouter, Depends

from models.purchase import Purchase
from services.purchase import PurchaseService
router = APIRouter(
    prefix="/shop/purchases"
)


@router.post("/purchase/")
async def create_purchase(
        purchase: Purchase,
        service: PurchaseService = Depends()
):
    return await service.make_purchase(
        buyer_number=purchase.buyer_number,
        products_to_buy=purchase.products
    )

@router.get("/all")
async def get_all_purchase(
        service: PurchaseService = Depends(),
):
    return await service.get_list()

@router.post("/purchase/delete_by_id/{purchase_id}")
async def del_purchase(
        purchase_id: int,
        service: PurchaseService = Depends(),

):
    return await service.delete_purchase_by_id(purchase_id)
