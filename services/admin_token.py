import jwt
from settings import settings
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from database import get_session
from models.token import Token
from fastapi import HTTPException, status
from  datetime import timedelta, datetime, timezone
from fastapi.security import HTTPAuthorizationCredentials

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
            admin_email:str,
            admin_password: str
    ) -> Token:
        if admin_email != settings.admin_name or admin_password != settings.admin_password:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль админа"
            )
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        access_token = self.create_access_token(
            data={
                "sub": admin_email,
                "exp": expire
            }
        )
        return Token(access_token=access_token)


    def get_current_user(self, credentials:HTTPAuthorizationCredentials = Depends(http_bearer)):
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Требуется токен для выполнения действия"
            )

        token_data = self.decode_token(credentials.credentials)

        res: str = token_data.get("sub")
        return res




