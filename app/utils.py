from passlib.context import CryptContext

pwd_context= CryptContext(schemes=["argon2"],deprecated="auto")


def hash(password:str):
    return pwd_context.hash(password)


def verify(raw_pwd,hashed_pwd):
    return pwd_context.verify(raw_pwd,hashed_pwd)
    