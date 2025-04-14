from typing import override
from macrosurfer.data_ingestion.fmp.fmp_data_ingestor import FMPDataIngestor
from datetime import datetime
import requests
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError
from macrosurfer.database import Database
from macrosurfer.models.fmp.economics import ECONOMIC_CALENDAR_TABLE

class EconomicCalendarIngestor(FMPDataIngestor):

    def __init__(self, db: Database, batch_size: int = 100):
        super().__init__(db, ECONOMIC_CALENDAR_TABLE, batch_size)

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
                    event_date = datetime.strptime(event['date'], '%Y-%m-%d %H:%M:%S')
                    stmt = pg_insert(self._table).values(
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
        from_date = self.strf_date(start_date)
        to_date = self.strf_date(end_date)
        return f"{self.FMP_ENDPOINT}/economic-calendar?from={from_date}&to={to_date}&apikey={self._api_key}"