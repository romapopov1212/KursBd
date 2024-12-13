from fastapi import APIRouter
from fastapi import Depends
from models.buyers import Buyers
from services.buyers import BuyersService

router = APIRouter(
    prefix="/shop/buyers"
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
):
    return await service.delete(buyer_number)

@router.get("/all")
async def get_all_buyers(service:BuyersService=Depends()):
    return await service.get_list()