# Example usage
from datetime import datetime, timedelta
from macrosurfer.data_ingestion.fmp.economics.economic_calendar_ingestor import EconomicCalendarIngestor
from macrosurfer.database import Database
from macrosurfer.data_ingestion.fmp.directory.company_symbol_list_ingestor import CompanySymbolListIngestor
from macrosurfer.data_ingestion.fmp.directory.financial_statement_symbols_ingestor import FinancialStatementSymbolsIngestor
from macrosurfer.models.fmp import *
from dotenv import load_dotenv

load_dotenv()

db = Database()
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now() + timedelta(days=30)

ingestor = FinancialStatementSymbolsIngestor(db)
ingestor.ingest(start_date, end_date)

# ingestor = CompanySymbolListIngestor(db)
# ingestor.ingest(datetime.now(), datetime.now() + timedelta(days=30))
