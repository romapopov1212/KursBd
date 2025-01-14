from fastapi import APIRouter, Depends, Form
from services.admin_token import AdminService
from fastapi.responses import Response

from models.admin import AdminLogin

router = APIRouter(
    prefix="/shop/admin",
    tags=['admin']
)


@router.post("/login")
async def login(
        loginData: AdminLogin,
        response: Response,
        service: AdminService = Depends()
):
    return await service.login_admin(loginData, response=response)