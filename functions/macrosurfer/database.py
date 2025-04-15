import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from macrosurfer.models.metadata import METADATA
from sqlalchemy.orm import scoped_session
from macrosurfer.models.fmp import *

class Database:
    def __init__(self):
        self.DATABASE_URL = f'postgresql+psycopg2://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST_NAME")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
        print(self.DATABASE_URL)
        self.engine = create_engine(self.DATABASE_URL)
        self.__session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_engine(self) -> Engine:
        return self.engine
    
    def get_session(self) -> Session:
        SC = scoped_session(self.__session_factory)
        return SC()
    
    def get_metadata(self) -> MetaData:
        return METADATA