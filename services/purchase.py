from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_session
from models.purchase import Purchase
from db import tables
from fastapi.responses import JSONResponse
from fastapi import status

class PurchaseService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def add_purchase(self, pur_date:Purchase):
        purch = tables.Purchase(
            buyer_number = pur_date.buyer_number,
            date = pur_date.date,
            full_price = pur_date.full_price
        )
        self.session.add(purch)
        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Покупатель {buyers_data.firstname} добавлен"}
        )