from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials

from models.purchase import Purchase
from services.purchase import PurchaseService
from services.admin_token import http_bearer


router = APIRouter(
    prefix="/shop/purchases",
    tags=['purchase']
)


@router.post("/purchase/")
async def create_purchase(
        purchase: Purchase,
        service: PurchaseService = Depends(),
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return await service.make_purchase(
        buyer_number=purchase.buyer_number,
        products_to_buy=purchase.products,
        credentials=credentials
    )

@router.get("/all")
async def get_all_purchase(
        service: PurchaseService = Depends(),
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return await service.get_list(credentials)

@router.get("/allPurcashedProduct")
async def get_all_purchaseProducts(
        service: PurchaseService = Depends(),
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return await service.get_purchaseProduct_list(credentials)

@router.delete("/purchase/delete_by_id/{purchase_id}")
async def del_purchase(
        purchase_id: int,
        service: PurchaseService = Depends(),
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return await service.delete_purchase_by_id(purchase_id, credentials)
