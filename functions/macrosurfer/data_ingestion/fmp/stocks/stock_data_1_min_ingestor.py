from macrosurfer.data_ingestion.fmp.fmp_data_ingestor import FMPDataIngestor
from macrosurfer.database import Database
from macrosurfer.models.fmp import STOCK_PRICE_1_MIN_TABLE
from datetime import datetime, timezone, timedelta
from typing import List, override, Any
from sqlalchemy.dialects.postgresql import insert as pg_insert

class StockData1MinIngestor(FMPDataIngestor):
    def __init__(self, db: Database, symbol: str, backfill: bool = False, batch_size: int = 100):
        super().__init__(db, STOCK_PRICE_1_MIN_TABLE, batch_size)
        self._symbol = symbol
        self._backfill = backfill
        self._start_time = (datetime.now(timezone.utc) - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')

    @override
    def ingest(self, start_date: datetime, end_date: datetime):
        url = self._get_url_with_api_key(start_date, end_date)
        data = self._get_data(url)
        self._execute_batch(data)

    @override
    def _get_stmt(self, event: Any) -> Any:
        if (not self._backfill) and event['date'] < self._start_time:
            return None
        event_date = datetime.strptime(event['date'], '%Y-%m-%d %H:%M:%S')
        return pg_insert(self._table).values(
            symbol=self._symbol,
            date=event_date,
            open=event['open'],
            high=event['high'],
            low=event['low'],
            close=event['close'],
            volume=event['volume']
        ).on_conflict_do_update(
            index_elements=['symbol', 'date'],
            set_=dict(
                open=event['open'],
                high=event['high'],
                low=event['low'],
                close=event['close'],
                volume=event['volume']
            )
        )

    @override
    def _get_url(self, start_date: datetime, end_date: datetime) -> str:
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        return f"https://financialmodelingprep.com/stable/historical-chart/1min?symbol={self._symbol}&from={start_date_str}&to={end_date_str}"

