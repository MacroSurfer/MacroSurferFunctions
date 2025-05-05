# Example usage
from datetime import datetime, timedelta
from macrosurfer.data_ingestion.fmp.economics.economic_calendar_ingestor import EconomicCalendarIngestor
from macrosurfer.database import Database
from macrosurfer.data_ingestion.fmp.directory.company_symbol_list_ingestor import CompanySymbolListIngestor
from macrosurfer.data_ingestion.fmp.directory.financial_statement_symbols_ingestor import FinancialStatementSymbolsIngestor
from macrosurfer.data_ingestion.fmp.directory.cik_list_ingestor import CIKListIngestor
from macrosurfer.models.fmp import *
from dotenv import load_dotenv
from macrosurfer.data_ingestion.fmp.stocks.stock_data_1_day_ingestor import StockData1DayIngestor
from macrosurfer.data_ingestion.fmp.stocks.stock_data_1_min_ingestor import StockData1MinIngestor

load_dotenv()

db = Database()
start_date = datetime(2023, 5, 11, 0, 0, 0)
end_date = datetime(2024, 5, 10, 0, 0, 0)

# ingestor = FinancialStatementSymbolsIngestor(db)
# ingestor.ingest(start_date, end_date)

# ingestor = CompanySymbolListIngestor(db)
# ingestor.ingest(datetime.now(), datetime.now() + timedelta(days=30))

# ingestor = CIKListIngestor(db)
# ingestor.ingest(datetime.now(), datetime.now() + timedelta(days=30))

ingestor = StockData1DayIngestor(db, 'SPY')
ingestor.ingest(start_date, end_date)

while start_date < end_date:
    ingestor = StockData1MinIngestor(db, 'SPY', backfill=True)
    ingestor.ingest(start_date, start_date + timedelta(days=1))
    start_date += timedelta(days=1)

