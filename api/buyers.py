from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from services.buyers import http_bearer
from models.buyers import Buyers
from services.buyers import BuyersService

router = APIRouter(
    prefix="/shop/buyers"
)

@router.post("/buyer/add")
async def add_buyer(
        buyer_data: Buyers,
        service: BuyersService=Depends(),
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return await service.add_buyers(buyer_data, credentials)

@router.delete("/buyer/delete")
async def delete(
        buyer_number: str,
        service: BuyersService=Depends(),
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return await service.delete(buyer_number, credentials)

@router.get("/all")
async def get_all_buyers(
        service:BuyersService=Depends(),
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return await service.get_list(credentials)