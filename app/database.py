from time import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL=settings.DATABASE_URL

#'postgresql://<username>:<password>@<ip-address/hostname>/<databse name>'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


# def db_connector():
    
#     while True:
#         try:
#             connection =psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='niroop19',cursor_factory=RealDictCursor)
#             print("database successfully connected.")
#             return connection
        
#         except Exception as err:
#             print("conenction to database failed.",err)
#             time.sleep(3)

# conn=db_connector()
# cursor=conn.cursor()
    