from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.future import select
from models.purchase import Purchase, PurchaseProduct
from models.products import Product
from database import get_session
from db import tables
from sqlalchemy.exc import IntegrityError
from datetime import datetime
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

    async def get_product_by_name(
            self,
            name: str
    ):
        stmt = select(tables.Products).filter(tables.Products.name == name)
        result = await self.session.execute(stmt)
        product_by_name = result.scalars().first()
        if product_by_name is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"Продукт '{name}' не найден"
            )

        return product_by_name


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
        prod = await self.get_product_by_name(product_name)

        await self.session.delete(prod)
        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Товар удален"}
        )

    async def make_purchase(
            self,
            buyer_number: str,
            products_to_buy: List[PurchaseProduct]
    ):
        buyer = await self.session.get(tables.Buyers, buyer_number)
        if not buyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Покупатель с номером телефона {buyer_number} не найден."
            )

        purchase = tables.Purchase(
            buyer_number=buyer_number,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            full_price=0
        )
        self.session.add(purchase)
        await self.session.flush()

        total_price = 0
        purchased_items = []

        for item in products_to_buy:
            product_id = item.product_id
            count_to_buy = item.count

            product = await self.get_product_by_id(product_id)
            if product.count < count_to_buy:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Недостаточно товара '{product.name}' на складе. Доступно: {product.count}, запрошено: {count_to_buy}."
                )

            product.count -= count_to_buy

            purchased_product = tables.PurchasedProducts(
                id_purchase=purchase.id_purchase,
                id_product=product_id,
                count=count_to_buy
            )
            self.session.add(purchased_product)

            total_price += product.price * count_to_buy

            purchased_items.append({
                "product_name": product.name,
                "count": count_to_buy,
                "price_per_item": float(product.price),
                "total_price": float(product.price * count_to_buy)
            })

        purchase.full_price = total_price

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при выполнении покупки. Попробуйте снова."
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Покупка успешно завершена",
                "purchase_id": purchase.id_purchase,
                "total_price": float(total_price),
                "purchased_items": purchased_items
            }
        )





