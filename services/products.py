from copy import deepcopy
from wsgiref.util import request_uri

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
        prod = tables.Products(
            name = product_data.name,
            price = product_data.price
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
        prod = await self.get_product(product_id)
        if prod is None:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар не найден"
            )
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
                detail="Список продуктов пуст",
            )
        return prod

    async def get_product(
            self,
            anything,
    ) -> tables.Products:
        prod = select(tables.Products).filter(tables.Products.id==anything)
        result = await self.session.execute(prod)
        product_by_id = result.scalars().first()
        return product_by_id

