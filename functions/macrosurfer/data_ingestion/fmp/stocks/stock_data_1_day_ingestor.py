from macrosurfer.data_ingestion.fmp.fmp_data_ingestor import FMPDataIngestor
from macrosurfer.database import Database
from macrosurfer.models.fmp import STOCK_PRICE_1_DAY_TABLE
from datetime import datetime, timezone, timedelta
from typing import List, override, Any
from sqlalchemy.dialects.postgresql import insert as pg_insert

class StockData1DayIngestor(FMPDataIngestor):
    def __init__(self, db: Database, symbol: str, batch_size: int = 100):
        super().__init__(db, STOCK_PRICE_1_DAY_TABLE, batch_size)
        self._symbol = symbol

    @override
    def ingest(self, start_date: datetime, end_date: datetime):
        url = self._get_url_with_api_key(start_date, end_date)
        data = self._get_data(url)
        self._execute_batch(data)

    @override
    def _get_stmt(self, event: Any) -> Any:
        event_date = datetime.strptime(event['date'], '%Y-%m-%d')
        return pg_insert(self._table).values(
            symbol=self._symbol,
            date=event_date,
            open=event['open'],
            high=event['high'],
            low=event['low'],
            close=event['close'],
            volume=event['volume'],
            change=event['change'],
            change_percentage=event['changePercent'],
            vwap=event['vwap']
        ).on_conflict_do_update(
            index_elements=['symbol', 'date'],
            set_=dict(
                open=event['open'],
                high=event['high'],
                low=event['low'],
                close=event['close'],
                volume=event['volume'],
                change=event['change'],
                change_percentage=event['changePercent'],
                vwap=event['vwap']
            )
        )

    @override
    def _get_url(self, start_date: datetime, end_date: datetime) -> str:
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        return f"https://financialmodelingprep.com/stable/historical-price-eod/full?symbol={self._symbol}&from={start_date_str}&to={end_date_str}"
