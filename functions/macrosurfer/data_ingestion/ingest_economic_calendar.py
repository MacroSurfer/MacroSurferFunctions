import os
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from pydantic import BaseModel
from macrosurfer.database import Database

from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from macrosurfer.tables import ECONOMIC_CALENDAR_TABLE, EVENT_DETAILS
import requests
from datetime import datetime, timedelta
from sqlalchemy import insert, update, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
load_dotenv()

db = Database()
engine = db.get_engine()
session = db.get_session()

def ingest_incoming_month_economic_calendar(start_date: datetime, end_date: datetime):
    # Format dates for the API
    from_date = start_date.strftime('%Y-%m-%d')
    to_date = end_date.strftime('%Y-%m-%d')
    try:
        # Fetch data from the API
        api_key = os.getenv("FINANCIAL_MODELINGPREP_API_KEY")
        url = f'https://financialmodelingprep.com/api/v3/economic_calendar?from={from_date}&to={to_date}&apikey={api_key}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Process data in chunks of 1000 records
        BATCH_SIZE = 100
        for i in range(0, len(data), BATCH_SIZE):
            batch = data[i:i + BATCH_SIZE]
            stmts = []
            
            for event in batch:
                event_date = datetime.strptime(event['date'], '%Y-%m-%d %H:%M:%S')
                stmt = pg_insert(ECONOMIC_CALENDAR_TABLE).values(
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
            print(f"Processed batch {i//BATCH_SIZE + 1} of {(len(data) + BATCH_SIZE - 1)//BATCH_SIZE}")

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except SQLAlchemyError as db_err:
        print(f"Database error occurred: {db_err}")
        session.rollback()
    except Exception as err:
        print(f"An error occurred: {err}")
    finally:
        session.close()

