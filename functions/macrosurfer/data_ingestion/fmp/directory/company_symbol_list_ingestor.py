from typing import override
from macrosurfer.data_ingestion.fmp.fmp_data_ingestor import FMPDataIngestor
from datetime import datetime
import requests
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError
from macrosurfer.database import Database
from macrosurfer.models.fmp.directory import COMPANY_SYMBOLS

class CompanySymbolListIngestor(FMPDataIngestor):

    def __init__(self, db: Database, batch_size: int = 100):
        super().__init__(db, COMPANY_SYMBOLS, batch_size)

    @override
    def ingest(self, start_date: datetime, end_date: datetime):
        url = self._get_url(start_date, end_date)
        data = self._get_data(url)
        session = self._db.get_session()

        try:
            for i in range(0, len(data), self._batch_size):
                batch = data[i:i + self._batch_size]
                stmts = []
                
                for event in batch:
                    stmt = pg_insert(self._table).values(
                        symbol=event['symbol'],
                        company_name=event['companyName']
                    ).on_conflict_do_update(
                        index_elements=['symbol'],
                        set_=dict(
                            company_name=event['companyName']
                        )
                    )
                    stmts.append(stmt)

                # Execute batch
                for stmt in stmts:
                    session.execute(stmt)
                session.commit()
                print(f"Processed batch {i//self._batch_size + 1} of {(len(data) + self._batch_size - 1)//self._batch_size}")

        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except SQLAlchemyError as db_err:
            print(f"Database error occurred: {db_err}")
            session.rollback()
        except Exception as err:
            print(f"An error occurred: {err}")
        finally:
            session.close()

    @override
    def _get_url(self, start_date: datetime, end_date: datetime) -> str:
        return f"{self.FMP_ENDPOINT}/stock-list?&apikey={self._api_key}"
