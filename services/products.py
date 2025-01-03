from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from services.admin_token import http_bearer

from models.products import Product
from database import get_session
from db import tables
from services.admin_token import AdminService


class ProductsService:

    def __init__(
            self,
            session: Session=Depends(get_session),
            admin_service: AdminService = Depends(),

    ):
        self.session = session
        self.admin_service = admin_service

    def exept_admin(
            self,
            credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
        current_user = self.admin_service.get_current_user(credentials)
        if current_user != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения действия"
            )
    
    
    async def add_product(
            self,
            product_data: Product,
            credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
        current_user = self.admin_service.get_current_user(credentials)
        if current_user != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения действия"
            )
        prod_try_name = await self.get_product_by_name_helper(product_data.name)
        if prod_try_name:
            prod_try_name.count += product_data.count
            prod_try_name.price = product_data.price
            await self.session.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": f"Товар '{product_data.name}' обновлен"}
            )
        prod = tables.Products(
            name = product_data.name,
            price = product_data.price,
            count=product_data.count
        )
        self.session.add(prod)
        await self.session.commit()
        return JSONResponse(
            status_code= status.HTTP_200_OK,
            content={"message": f"Товар '{product_data.name}' добален"}
        )


    async def update_product(
            self,
            product_id,
            new_data: Product,
            credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
        current_user = self.admin_service.get_current_user(credentials)
        if current_user != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения действия"
            )
        prod = await self.get_product_by_id(product_id)
        for field, value in vars(new_data).items():
            setattr(prod, field, value)
        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message" : f"Товар '{prod.name}' изменен"}
        )


    async def get_list(self) -> List[tables.Products]:
        stmt = select(tables.Products)
        result = await self.session.execute(stmt)
        prod = result.scalars().all()

        if prod is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Список продуктов пуст"
            )
        return prod


    async def get_product_by_name_helper(
            self,
            name: str
    ):
        stmt = select(tables.Products).filter(tables.Products.name == name)
        result = await self.session.execute(stmt)
        product_by_name = result.scalars().first()
        return product_by_name


    async def get_by_name(
            self,
            name: str
    ):
        res = await self.get_product_by_name_helper(name)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар с именем {name} не найден"
            )
        return res


    async def get_product_by_id(
            self,
            product_id: int
    ) -> tables.Products:
        prod = select(tables.Products).filter(tables.Products.id==product_id)
        result = await self.session.execute(prod)
        product_by_id = result.scalars().first()
        if product_by_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"Продукт с id: {product_id} не найден"
            )
        return product_by_id


    async def delete_by_id(
            self,
            product_id,
            credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
        current_user = self.admin_service.get_current_user(credentials)
        if current_user != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения действия"
            )
        search_in_purchase = await self.session.execute(
            select(tables.PurchasedProducts).where(tables.PurchasedProducts.id_product == product_id)
        )

        if search_in_purchase.scalars().first():
            prod = await self.get_product_by_id(product_id)
            prod.count = 0
            await self.session.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message" : f"Товар содержится в заказе, поэтому его нельзя удалить полностью, его кол-во = 0"}
            )
        prod = await self.get_product_by_id(product_id)
        await self.session.delete(prod)
        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Товар удален"}
        )


    async def delete_by_name(
            self,
            product_name: str,
            credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
        current_user = self.admin_service.get_current_user(credentials)
        if current_user != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения действия"
            )
        prod = await self.get_product_by_name_helper(product_name)
        if prod is None:
            raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail= f"Продукт '{product_name}' не найден"
                    )
        await self.session.delete(prod)
        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Товар удален"}
        )





