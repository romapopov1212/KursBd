from pydantic import BaseModel, field_validator, ValidationError


class Product(BaseModel):
    name: str
    price: float
    count: int

    @field_validator("name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Ошибка")
        return v

    @field_validator("price")
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Ошибка")
        return v

    @field_validator("count")
    def validate_count(cls, v):
        if v < 0:
            raise ValueError("Ошибка")
        return v