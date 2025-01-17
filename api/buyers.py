from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from services.admin_token import AdminService
from services.buyers import http_bearer
from models.buyers import Buyers
from services.buyers import BuyersService

templates = Jinja2Templates(directory="templates")

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

@router.delete("/buyer/delete/{buyer_number}")
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

@router.get("/buyers_page", response_class=HTMLResponse)
async def get_page(
    request: Request,
    service: BuyersService = Depends(),
    admin_service: AdminService = Depends()
):
    t = admin_service.get_cooks_and_check_is_admin(request=request)
    buyers = await service.get_list(t)
    return templates.TemplateResponse("buyer.html", {"request" : request, "buyers" : buyers})