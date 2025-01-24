from pydantic import BaseModel, field_validator

class Buyers(BaseModel):
    telephone_number: str
    firstname: str
    surname: str
    lastname: str

    @field_validator("telephone_number")
    def validate_telephone_number(cls, v):
        if not v.startswith('8') or not v[1:].isdigit() or len(v) != 11:
            raise ValueError("Номер телефона должен начинаться с '8' и содержать 11 цифр")
        return v
    
    @field_validator("firstname", "surname", "lastname")
    def validate_names(cls, v, field):
        if not v.isalpha():
            raise ValueError("Некорректное ФИО")
        return v