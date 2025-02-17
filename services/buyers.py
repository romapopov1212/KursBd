from fastapi import Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.future import select
from fastapi.security import HTTPAuthorizationCredentials
from settings import settings
from services.admin_token import AdminService, http_bearer
from db import tables
from database import get_session
from models.buyers import Buyers

class BuyersService:
    def __init__(
            self,
            session: Session = Depends(get_session),
            admin_service: AdminService = Depends()
    ):
        self.session = session
        self.admin_service = admin_service

    # def exept_admin(
    #         self,
    #         credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    # ):
    #     current_user = self.admin_service.get_current_user(credentials)
    #     if current_user != "admin":
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="Недостаточно прав для выполнения действия"
    #         )

    async def add_buyers(
            self,
            buyers_data: Buyers,
    ):
        stmt = select(tables.Buyers).filter(tables.Buyers.telephone_number == buyers_data.telephone_number)
        result = await self.session.execute(stmt)
        buyer_by_number = result.scalars().first()
        if buyer_by_number is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пользователь с таким номером уже существует"
            )
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
            content={"message": f"Покупатель {buyers_data.firstname} добавлен"}
        )

    async def delete(
            self,
            buyer_number,
            token:str,
            #credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
        current_user = self.admin_service.get_current_user(token)
        if current_user != settings.admin_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения действия"
            )
        stmt = select(tables.Purchase).filter(tables.Purchase.buyer_number == buyer_number)
        res = await self.session.execute(stmt)
        buyer_by_number = res.scalars().first()
        if buyer_by_number is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Этот пользователь есть в данных о купленных товарах, удалите сначала их."
            )
        buyer_for_delete = await self.get_buyer_by_number(buyer_number, token)
        await self.session.delete(buyer_for_delete)
        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Покупатель удален"}
        )

    async def get_by_number(
        self,
        telephone_number:str,
        token:str,      
    ):
        current_user = self.admin_service.get_current_user(token)
        if current_user != settings.admin_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения действия"
            )
        stmt = select(tables.Buyers).filter(tables.Buyers.telephone_number == telephone_number)
        res = await self.session.execute(stmt)
        buyer_by_number = res.scalars().first()
        if buyer_by_number is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"Покупатель с номером: {telephone_number} не найден."
            )
        return buyer_by_number
        

    async def get_list(
            self,
            token: str
            #credentials: HTTPAuthorizationCredentials=Depends()
    ) -> List[tables.Buyers]:

        current_user = self.admin_service.get_current_user(token)
        if current_user != settings.admin_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения действия"
            )
        stmt = select(tables.Buyers)
        result = await self.session.execute(stmt)
        buyers = result.scalars().all()
        if buyers is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "Список покупателей пуст"
            )
        return buyers

    async def get_buyer_by_number(
            self,
            number: str,
            token:str
            #credentials: HTTPAuthorizationCredentials=Depends()
    ):
        current_user = self.admin_service.get_current_user(token)
        if current_user != settings.admin_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения действия"
            )
        stmt = select(tables.Buyers).filter(tables.Buyers.telephone_number == number)
        result = await self.session.execute(stmt)
        buyer_by_number = result.scalars().first()
        if buyer_by_number is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"Покупатель c номером {number} не найден"
            )
        return buyer_by_number
