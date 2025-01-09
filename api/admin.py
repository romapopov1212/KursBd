from fastapi import APIRouter, Depends, Form
from services.admin_token import AdminService
from pydantic import BaseModel
router = APIRouter(
    prefix="/shop/admin",
    tags=['admin']
)


class AdminLogin(BaseModel):
    admin_name: str
    admin_password: str

@router.post("/login")
async def login(
        loginData: AdminLogin,
        service: AdminService = Depends()
):
    return await service.login_admin(loginData.admin_name, loginData.admin_password)
