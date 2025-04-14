from abc import ABC, abstractmethod
from datetime import datetime
from macrosurfer.database import Database
import os
import requests
from typing import Any

class FMPDataIngestor(ABC):
    FMP_ENDPOINT = "https://financialmodelingprep.com/stable"

    def __init__(self, db: Database, table: str, batch_size: int = 100):
        self._db = db
        self._table = table
        self._batch_size = batch_size
        self._api_key = os.getenv("FINANCIAL_MODELINGPREP_API_KEY")
    
    @abstractmethod
    def ingest(self, start_date: datetime, end_date: datetime):
        pass

    def _get_data(self, url: str) -> Any:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    @abstractmethod
    def _get_url(self, start_date: datetime, end_date: datetime) -> str:
        pass
    
    @staticmethod
    def strf_date(date: datetime) -> str:
        return date.strftime('%Y-%m-%d')