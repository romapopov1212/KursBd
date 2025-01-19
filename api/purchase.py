from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.requests import Request

from services.admin_token import AdminService
from fastapi.templating import Jinja2Templates
from models.purchase import Purchase
from services.purchase import PurchaseService
from services.admin_token import http_bearer


template = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/shop/products",
    tags=['purchase']
)


@router.post("/purchase")
async def create_purchase(
        purchase: Purchase,
        service: PurchaseService = Depends(),
        
):
    return await service.make_purchase(
        buyer_number=purchase.buyer_number,
        products_to_buy=purchase.products,
    )

@router.get("/Purchase/all")
async def get_all_purchase(
        service: PurchaseService = Depends(),
        admin_service: AdminService = Depends(),
        request: Request = None,
):
    t = admin_service.get_cooks_and_check_is_admin(request=request)
    return await service.get_list(t)

@router.get("/allPurcashedProduct")
async def get_all_purchaseProducts(
        service: PurchaseService = Depends(),
        admin_service: AdminService = Depends(),
        request: Request = None,
        
):
    t = admin_service.get_cooks_and_check_is_admin(request=request)
    return await service.get_purchaseProduct_list(t)

@router.delete("/purchase/delete_by_id/{purchase_id}")
async def del_purchase(
        purchase_id: int,
        service: PurchaseService = Depends(),
        admin_service: AdminService = Depends(),
        request: Request = None,
):
    t = admin_service.get_cooks_and_check_is_admin(request=request)
    return await service.delete_purchase_by_id(purchase_id, t)


@router.get("/purchase_page")
async def get_page(
    request: Request,
    service: PurchaseService = Depends(),
    admin_service: AdminService = Depends()
):
    t = admin_service.get_cooks_and_check_is_admin(request=request)
    pur = await service.get_list(t)
    purProd = await service.get_purchaseProduct_list(t)
    return template.TemplateResponse("purchase.html", {"request": request, "purchase" : pur, "purProds" : purProd})


@router.get("/report/{telephone_number}")
async def get_report(
    telephone_number: str,
    request: Request,
    service: PurchaseService = Depends(),
    admin_service: AdminService = Depends(),
):
    t = admin_service.get_cooks_and_check_is_admin(request=request)
    return await service.get_report(telephone_number, token=t)


@router.get("/report_page")
async def get_report_page(
    request: Request,
    service: PurchaseService = Depends(),
    admin_service: AdminService = Depends()
):
    t = admin_service.get_cooks_and_check_is_admin(request=request)
    return template.TemplateResponse("report.html", {"request": request})