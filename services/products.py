from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.future import select

from models.products import Product
from database import get_session
from db import tables


class ProductsService:

    def __init__(
            self,
            session: Session=Depends(get_session)
    ):
        self.session = session


    async def add_product(
            self,
            product_data: Product
    ):
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
            new_data: Product
    ):
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
            product_id
    ):
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
    ):
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





