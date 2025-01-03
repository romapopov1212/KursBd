from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    admin_name: str
    admin_password: str
    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()