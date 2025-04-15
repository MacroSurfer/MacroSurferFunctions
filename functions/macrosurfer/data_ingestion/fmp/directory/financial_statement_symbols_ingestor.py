from macrosurfer.data_ingestion.fmp.fmp_data_ingestor import FMPDataIngestor
from macrosurfer.database import Database   
from macrosurfer.models.fmp import FINANCIAL_STATEMENT_SYMBOLS
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert as pg_insert

from typing import Any, override

class FinancialStatementSymbolsIngestor(FMPDataIngestor):
    def __init__(self, db: Database, batch_size: int = 100):
        super().__init__(db, FINANCIAL_STATEMENT_SYMBOLS, batch_size)

    @override
    def ingest(self, start_date: datetime, end_date: datetime):
        url = self._get_url(start_date, end_date)
        data = self._get_data(url)
        self._execute_batch(data)

    @override
    def _get_stmt(self, event: Any) -> Any:
        return pg_insert(self._table).values(
            symbol=event['symbol'],
            company_name=event['companyName'],
            trading_currency=event['tradingCurrency'],
            reporting_currency=event['reportingCurrency']
                    ).on_conflict_do_update(
                        index_elements=['symbol'],
                        set_=dict(
                company_name=event['companyName'],
                trading_currency=event['tradingCurrency'],
                reporting_currency=event['reportingCurrency']
            )
        )
    
    @override
    def _get_url(self, start_date: datetime, end_date: datetime) -> str:
        return f"{self.FMP_ENDPOINT}/financial-statement-symbol-list?apikey={self._api_key}"

