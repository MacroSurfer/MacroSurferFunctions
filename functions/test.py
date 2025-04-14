# Example usage
from datetime import datetime, timedelta
from macrosurfer.data_ingestion.fmp.economics.economic_calendar_ingestor import EconomicCalendarIngestor
from macrosurfer.database import Database
from macrosurfer.data_ingestion.fmp.directory.company_symbol_list_ingestor import CompanySymbolListIngestor

db = Database()
ingestor = EconomicCalendarIngestor(db)
ingestor.ingest(datetime.now(), datetime.now() + timedelta(days=30))

# ingestor = CompanySymbolListIngestor(db)
# ingestor.ingest(datetime.now(), datetime.now() + timedelta(days=30))
