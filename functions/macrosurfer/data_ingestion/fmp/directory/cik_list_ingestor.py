from macrosurfer.data_ingestion.fmp.fmp_data_ingestor import FMPDataIngestor
from macrosurfer.database import Database
from macrosurfer.models.fmp import CIK_LIST
from datetime import datetime
from typing import Any, override
from sqlalchemy.dialects.postgresql import insert as pg_insert
class CIKListIngestor(FMPDataIngestor):

    def __init__(self, db: Database):
        super().__init__(db, CIK_LIST)

    @override
    def ingest(self, start_date: datetime, end_date: datetime):
        url = self._get_url_with_api_key(start_date, end_date)
        data = self._get_data(url)
        self._execute_batch(data)

    @override
    def _get_stmt(self, event: Any) -> Any:
        return pg_insert(self._table).values(
            cik=event['cik'],
            company_name=event['companyName'],
            
        ).on_conflict_do_update(
            index_elements=['cik'],
            set_=dict(
                company_name=event['companyName'],
            )
        )

    @override
    def _get_url(self, start_date: datetime, end_date: datetime) -> str:
        return f"{self.FMP_ENDPOINT}/cik-list"

