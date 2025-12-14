from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL:str
    
    #JWT
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int=60
    
    ENV:Optional[str]="production"
    
    
    class Config:
        env_file=".env"
        env_file_encoding="utf-8"
        

settings=Settings()