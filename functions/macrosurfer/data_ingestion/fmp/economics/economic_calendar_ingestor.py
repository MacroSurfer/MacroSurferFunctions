from typing import Any, override
from macrosurfer.data_ingestion.fmp.fmp_data_ingestor import FMPDataIngestor
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert as pg_insert
from macrosurfer.database import Database
from macrosurfer.models.fmp import ECONOMIC_CALENDAR_TABLE

class EconomicCalendarIngestor(FMPDataIngestor):

    def __init__(self, db: Database, batch_size: int = 100):
        super().__init__(db, ECONOMIC_CALENDAR_TABLE, batch_size)

    @override
    def ingest(self, start_date: datetime, end_date: datetime):
        url = self._get_url_with_api_key(start_date, end_date)
        data = self._get_data(url)
        self._execute_batch(data)

    @override
    def _get_stmt(self, event: Any) -> Any:
        event_date = datetime.strptime(event['date'], '%Y-%m-%d %H:%M:%S')
        return pg_insert(self._table).values(
            event=event['event'],
            event_date=event_date,
            country=event['country'],
            currency=event['currency'],
            previous=event['previous'],
            estimate=event['estimate'],
            actual=event['actual'],
            change=event['change'],
            impact=event['impact'],
            change_percentage=event['changePercentage'],
            unit=event['unit']
        ).on_conflict_do_update(
            index_elements=['event', 'event_date'],
            set_=dict(
                country=event['country'],
                currency=event['currency'],
                previous=event['previous'],
                estimate=event['estimate'],
                actual=event['actual'],
                change=event['change'],
                impact=event['impact'],
                change_percentage=event['changePercentage'],
                unit=event['unit']
            )
        )

    @override
    def _get_url(self, start_date: datetime, end_date: datetime) -> str:
        from_date = self.strf_date(start_date)
        to_date = self.strf_date(end_date)
        return f"{self.FMP_ENDPOINT}/economic-calendar?from={from_date}&to={to_date}"
