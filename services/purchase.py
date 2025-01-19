from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import datetime
from services.products import ProductsService
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from fastapi.security import HTTPAuthorizationCredentials

from services.buyers import BuyersService
from settings import settings
from services.buyers import http_bearer, AdminService
from database import get_session
from models.purchase import PurchaseProduct
from db import tables

class PurchaseService:
    def __init__(
            self,
            session: Session = Depends(get_session),
            service: ProductsService = Depends(),
            admin_service: AdminService = Depends(),
            buyer_service: BuyersService = Depends()
    ):
        self.session = session
        self.service = service
        self.admin_service = admin_service
        self.buyer_service = buyer_service

    async def make_purchase(
            self,
            buyer_number: str,
            products_to_buy: List[PurchaseProduct],
    ):
        buyer = await self.session.get(tables.Buyers, buyer_number)
        if not buyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Покупатель с таким номером телефона не найден, сначала зарегистрируйтесь"
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

    async def get_list(
            self,
            token: str
            #credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    ) -> List[tables.Purchase]:

        current_user = self.admin_service.get_current_user(token)
        if current_user != settings.admin_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения действия"
            )
        stmt = select(tables.Purchase)
        result = await self.session.execute(stmt)
        pur = result.scalars().all()

        if pur is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Список покупок пуст."
            )
        return pur
    

    async def get_purchaseProduct_list(
            self, 
            token: str
            #credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    ) -> List[tables.PurchasedProducts]:
        current_user = self.admin_service.get_current_user(token)
        if current_user != settings.admin_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения действия"
            )
        stmt = select(tables.PurchasedProducts)
        result = await self.session.execute(stmt)
        purProd = result.scalars().all()

        if purProd is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Список купленных продуктов пуст"
            )
        return purProd


    async def delete_purchase_by_id(
            self,
            purchase_id: int,
            token:str
            #credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    ):

        current_user = self.admin_service.get_current_user(token)
        if current_user != settings.admin_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения действия"
            )

        purchase = await self.session.get(tables.Purchase, purchase_id)
        if purchase is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Нет покупки с id: {purchase_id}"
            )
        stmt = select(tables.PurchasedProducts).where(tables.PurchasedProducts.id_purchase == purchase_id)
        result = await self.session.execute(stmt)
        purchased_products = result.scalars().all()
        for item in purchased_products:
            await self.session.delete(item)

        await self.session.delete(purchase)
        await self.session.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message" : "Покупка удалена успешно."}
        )

    async def get_report(
        self,
        buyer_number: str,
        token: str
    ):
        # Проверка прав доступа
        current_user = self.admin_service.get_current_user(token)
        if current_user != settings.admin_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения действия"
            )

        # Получаем все покупки покупателя
        buyer = await self.session.get(tables.Buyers, buyer_number)
        if not buyer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Покупатель с таким номером телефона не найден."
            )

        stmt = select(tables.Purchase).where(tables.Purchase.buyer_number == buyer_number)
        result = await self.session.execute(stmt)
        purchases = result.scalars().all()

        if not purchases:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="У покупателя нет совершенных покупок."
            )

        # Собираем данные для отчета
        report = []
        for purchase in purchases:
            # Получаем информацию о продуктах, купленных в рамках этой покупки
            stmt = select(tables.PurchasedProducts).where(tables.PurchasedProducts.id_purchase == purchase.id_purchase)
            result = await self.session.execute(stmt)
            purchased_products = result.scalars().all()

            products_details = []
            for purchased_product in purchased_products:
                product = await self.service.get_product_by_id(purchased_product.id_product)
                products_details.append({
                    "product_name": product.name,
                    "count": purchased_product.count,
                    "price_per_item": float(product.price),
                    "total_price": float(product.price * purchased_product.count)
                })

            report.append({
                "purchase_id": purchase.id_purchase,
                "date": purchase.date,
                "full_price": float(purchase.full_price),
                "products": products_details
            })

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Отчет о покупках покупателя",
                "buyer_number": buyer_number,
                "purchases": report
            }
        )

            
