import jwt
from settings import settings
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from database import get_session
from models.token import Token
from fastapi import HTTPException, status
from  datetime import timedelta, datetime

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
            #expires_delta: timedelta | None = None
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
            admin_email:str,
            admin_password: str
    ) -> Token:
        if admin_email != settings.admin_name or admin_password != settings.admin_password:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Invalid admin login or password"
            )
        access_token_expires = timedelta(minutes=40)
        expiration_time = (datetime.utcnow() + access_token_expires).timestamp()

        access_token = self.create_access_token(
            data={
                "sub": admin_email,
                "exp": expiration_time
            }
        )
        return Token(access_token=access_token)


