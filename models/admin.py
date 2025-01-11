from pydantic import BaseModel

class AdminLogin(BaseModel):
    admin_name: str
    admin_password: str