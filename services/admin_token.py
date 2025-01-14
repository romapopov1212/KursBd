import jwt
from settings import settings
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from database import get_session
from models.token import Token
from fastapi import HTTPException, status
from  datetime import timedelta, datetime, timezone
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import Response

from models.admin import AdminLogin

http_bearer = HTTPBearer(auto_error=False)

class AdminService:
    def __init__(
            self,
            session: Session=Depends(get_session)
    ):
        self.session = session

    @staticmethod
    def create_access_token(
            data: dict,
    ):
        to_encode = data.copy()
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return encoded_jwt

    @staticmethod
    def decode_token(token:str) -> dict:
        token_data = jwt.decode(token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return token_data

    async def login_admin(
            self,
            admin_data: AdminLogin,
            response: Response = None
    ) -> Token:
        if admin_data.admin_name != settings.admin_name or admin_data.admin_password != settings.admin_password:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль админа"
            )
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)

        access_token = self.create_access_token(
            data={
                "sub": admin_data.admin_name,
                "exp": expire
            }
        )
        response.set_cookie("token", access_token)
        return Token(access_token=access_token)


    def get_current_user(
            self, 
            token:str,
    ):
        if not token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет прав для выполнения действия"
            )

        token_data = self.decode_token(token)

        res: str = token_data.get("sub")
        return res
    
    def get_cooks_and_check_is_admin(self, request: Request):
        t = request.cookies.get("token")
        current_user = self.get_current_user(t)
        if current_user != settings.admin_name:
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail="Вы не вошли как администратор."
            )
        return t





