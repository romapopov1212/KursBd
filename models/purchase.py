from pydantic import BaseModel
from typing import List
# class Purchase(BaseModel):
#     id_product: int
#     buyer_number:str
#     date: str
#     full_price: float

class PurchaseProduct(BaseModel):
    product_id: int
    count: int
class Purchase(BaseModel):
    buyer_number: str
    products: List[PurchaseProduct]