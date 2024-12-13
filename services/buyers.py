from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import status


from db import tables
from database import get_session
from models.buyers import Buyers

class BuyersService:
    def __init__(
            self,
            session: Session = Depends(get_session)
    ):
        self.session = session

    async def add_buyers(
            self,
            buyers_data: Buyers,
    ):
        buyer = tables.Buyers(
            telephone_number = buyers_data.telephone_number,
            name = buyers_data.firstname,
            surname = buyers_data.surname,
            lastname = buyers_data.lastname
        )
        self.session.add(buyer)
        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Пользователь {buyers_data.firstname} добавлен"}
        )