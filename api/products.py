from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import status

from settings import settings
from services.admin_token import AdminService
from services.admin_token import http_bearer
from services.products import ProductsService
from models.products import Product



templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/shop/products",
    tags=['products']
)


@router.post("/add_product")
async def add_product(
        prod_data: Product,
        request: Request = None,
        service: ProductsService=Depends(),
        
        #credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    t = request.cookies.get("token")
    return await service.add_product(prod_data, t)

@router.patch("/update_product/{product_id}")
async def update_product(
        product_id:int,
        new_product_data: Product,
        service: ProductsService=Depends(),
        request: Request = None,
        #credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    t = request.cookies.get("token")
    return await service.update_product(product_id, new_product_data, token=t)

#для отрисовки страниц(потом надо куда нибудь переместить в отдельный файл)
@router.get("/products_page", response_class=HTMLResponse)
async def get_page(
        request: Request,
        service: ProductsService = Depends()
):
    prod = await service.get_list()
    return templates.TemplateResponse("index.html", {"request": request, "products": prod})


@router.get("/admin_page", response_class=HTMLResponse)
async def get_admin_page(
        request: Request,
        service: ProductsService = Depends(),
        admin_service: AdminService = Depends(),
):
    t = admin_service.get_cooks_and_check_is_admin(request=request)
    prod = await service.get_list()
    return templates.TemplateResponse("index_admin.html", {"request" : request, "products" : prod})

##########
@router.get("/all")
async def get_products(
        #current_page: int,
        #number_prod: int,
        service: ProductsService=Depends(),
):
    return await service.get_list()

@router.get("/product/name/{product_name}")
async def get_product(
        product_name: str,
        service: ProductsService=Depends(),
):
    return await service.get_by_name(product_name)

@router.get("/product/id/{product_id}")
async def get_product_by_id(
        product_id: int,
        service: ProductsService=Depends(),
):
    return await service.get_product_by_id(product_id)

@router.delete("/delete_product/id/{product_id}")
async def delete_product_by_id(
        product_id: int,
        request: Request,
        service: ProductsService=Depends(),
        admin_service: AdminService = Depends(),
        #credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    t = admin_service.get_cooks_and_check_is_admin(request=request)
    return await service.delete_by_id(product_id, t)

@router.delete("/delete_product/name/{product_name}")
async def delete_product_by_name(
        product_name: str,
        request: Request,
        service: ProductsService=Depends(),
        admin_service: AdminService = Depends()
        #credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    t = admin_service.get_cooks_and_check_is_admin(request=request)

    return await service.delete_by_name(product_name, t)