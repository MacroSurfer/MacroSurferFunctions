from typing import Any, override
from macrosurfer.data_ingestion.fmp.fmp_data_ingestor import FMPDataIngestor
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert as pg_insert
from macrosurfer.database import Database
from macrosurfer.models.fmp import COMPANY_SYMBOLS

class CompanySymbolListIngestor(FMPDataIngestor):

    def __init__(self, db: Database, batch_size: int = 100):
        super().__init__(db, COMPANY_SYMBOLS, batch_size)

    @override
    def ingest(self, start_date: datetime, end_date: datetime):
        url = self._get_url(start_date, end_date)
        data = self._get_data(url)
        self._execute_batch(data)

    @override
    def _get_stmt(self, event: Any) -> Any:
        return pg_insert(self._table).values(
            symbol=event['symbol'],
            company_name=event['companyName']
        ).on_conflict_do_update(
            index_elements=['symbol'],
            set_=dict(
                company_name=event['companyName']
            )
        )

    @override
    def _get_url(self, start_date: datetime, end_date: datetime) -> str:
        return f"{self.FMP_ENDPOINT}/stock-list?&apikey={self._api_key}"
