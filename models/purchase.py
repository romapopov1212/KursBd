from pydantic import BaseModel
from typing import List


class PurchaseProduct(BaseModel):
    product_id: int
    count: int


class Purchase(BaseModel):
    buyer_number: str
    products: List[PurchaseProduct]