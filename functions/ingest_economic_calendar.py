from dotenv import load_dotenv
from macrosurfer.data_ingestion.ingest_economic_calendar import ingest_incoming_month_economic_calendar
from datetime import datetime, timedelta
from macrosurfer.database import Database

load_dotenv()

if __name__ == "__main__":
    db = Database()

    end_date = datetime(2015, 1, 1, 0, 0, 0)
    start_date = datetime(2005, 1, 1, 0, 0, 0)
    while start_date < end_date:
        cur_end_date = min(start_date + timedelta(days=3), end_date)
        print(f"Ingesting economic calendar from {start_date} to {cur_end_date}")
        ingest_incoming_month_economic_calendar(db, start_date, cur_end_date)
        start_date = cur_end_date
