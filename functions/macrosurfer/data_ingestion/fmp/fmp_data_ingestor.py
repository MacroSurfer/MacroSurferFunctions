from abc import ABC, abstractmethod
from datetime import datetime
from macrosurfer.database import Database
import os
import requests
from typing import Any, List
from sqlalchemy.exc import SQLAlchemyError

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
    
    @abstractmethod
    def _get_url(self, start_date: datetime, end_date: datetime) -> str:
        pass
    
    @staticmethod
    def strf_date(date: datetime) -> str:
        return date.strftime('%Y-%m-%d')
    
    @abstractmethod
    def _get_stmt(self, event: Any) -> Any:
        pass

    def _get_data(self, url: str) -> Any:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _get_url_with_api_key(self, start_date: datetime, end_date: datetime) -> str:
        url = self._get_url(start_date, end_date)
        if '?' in url:
            return f"{url}&apikey={self._api_key}"
        else:
            return f"{url}?apikey={self._api_key}"
    
    def _execute_batch(self, data: List[Any]):
        session = self._db.get_session()
        try:
            for i in range(0, len(data), self._batch_size):
                batch = data[i:i + self._batch_size]
                stmts = []
                for event in batch:
                    stmt = self._get_stmt(event)
                    stmts.append(stmt)

                for stmt in stmts:
                    session.execute(stmt)
                
                session.commit()
                print(f"Processed batch {i//self._batch_size + 1} of {(len(data) + self._batch_size - 1)//self._batch_size}")
        
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except SQLAlchemyError as db_err:
            print(f"Database error occurred: {db_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        finally:
            session.close()