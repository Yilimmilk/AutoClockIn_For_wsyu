from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ConfigConst import *

SQLALCHEMY_DATABASE_URL = f'mysql+mysqldb://{USER}:{PSWD}@{HOST}:{PORT}/{DB_NAME}?charset=utf8'
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
