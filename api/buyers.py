from fastapi import APIRouter
from fastapi import Depends
from models.buyers import Buyers
from services.buyers import BuyersService

router = APIRouter(
    prefix="/shop/buyers"
)

@router.post("/add")
async def add_buyer(
        buyer_data: Buyers,
        service: BuyersService=Depends(),
):
    return await service.add_buyers(buyer_data)