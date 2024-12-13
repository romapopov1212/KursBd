from pydantic import BaseModel

class Buyers(BaseModel):
    telephone_number: str
    firstname: str
    surname: str
    lastname: str