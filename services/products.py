from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi import status

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

