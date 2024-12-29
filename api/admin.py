from fastapi import APIRouter, Depends
from services.admin_token import AdminService
router = APIRouter(
    prefix="/shop/admin",
    tags=['admin']
)

@router.post("/login")
async def login(
        admin_name: str,
        admin_password: str,
        service: AdminService = Depends()
):
    return await service.login_admin(admin_name, admin_password)
