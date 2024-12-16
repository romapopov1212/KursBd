from pydantic import BaseModel

class PurchasedProduct(BaseModel):
    count: int
