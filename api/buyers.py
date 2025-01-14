from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from services.admin_token import AdminService
from services.buyers import http_bearer
from models.buyers import Buyers
from services.buyers import BuyersService

router = APIRouter(
    prefix="/shop/buyers",
    tags=['buyers']
)

@router.post("/buyer/add")
async def add_buyer(
        buyer_data: Buyers,
        service: BuyersService=Depends(),
):
    return await service.add_buyers(buyer_data)

@router.delete("/buyer/delete")
async def delete(
        buyer_number: str,
        service: BuyersService=Depends(),
        request: Request = None,
        admin_serice: AdminService = Depends(),
        #credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    t = admin_serice.get_cooks_and_check_is_admin(request=request)
    return await service.delete(buyer_number, t)

@router.get("/all")
async def get_all_buyers(
        service:BuyersService=Depends(),
        request: Request = None,
        admin_serice: AdminService = Depends(),
        #credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    t = admin_serice.get_cooks_and_check_is_admin(request=request)
    return await service.get_list(t)