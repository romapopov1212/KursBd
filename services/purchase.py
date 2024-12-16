from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import datetime
from services.products import ProductsService
from sqlalchemy.exc import IntegrityError

from database import get_session
from models.purchase import PurchaseProduct, Purchase
from db import tables

class PurchaseService:
    def __init__(
            self,
            session: Session = Depends(get_session),
            service: ProductsService = Depends()
    ):
        self.session = session
        self.service = service


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

            product = await self.service.get_product_by_id(product_id)
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