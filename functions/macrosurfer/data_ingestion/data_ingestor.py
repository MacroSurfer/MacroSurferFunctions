from abc import ABC, abstractmethod
from datetime import datetime
from macrosurfer.database import Database

class DataIngestor(ABC):
    FMP_ENDPOINT = "https://financialmodelingprep.com/api/v3"

    def __init__(self, db: Database, table: str, batch_size: int = 100):
        self.__db = db
        self.__table = table
        self.__batch_size = batch_size
    
    @abstractmethod
    def ingest(self, start_date: datetime, end_date: datetime):
        pass
    