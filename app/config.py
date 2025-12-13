from tkinter import E
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    #db_related
    DB_USER: str="postgres"
    DB_PASSWORD:str
    DB_HOST:str ="localhost"
    DB_PORT:int=5432
    DB_NAME:str
    
    #JWT
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int=60
    
    ENV:Optional[str]="production"
    
    
    class Config:
        env_file=".env"
        env_file_encoding="utf-8"
        

settings=Settings()