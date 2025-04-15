from sqlalchemy import Table, Column, String, TIMESTAMP

from macrosurfer.models.metadata import METADATA

COMPANY_SYMBOLS = Table(
    'company_symbols', METADATA,
    Column('symbol', String, primary_key=True),
    Column('company_name', String)
)

FINANCIAL_STATEMENT_SYMBOLS = Table(
    'financial_statement_symbols', METADATA,
    Column('symbol', String, primary_key=True),
    Column('company_name', String, index=True),
    Column('trading_currency', String),
    Column('reporting_currency', String)
)

CIK_LIST = Table(
    'cik_list', METADATA,
    Column('cik', String, primary_key=True),
    Column('company_name', String, index=True)
)

SYMBOL_CHANGE_LIST = Table(
    'symbol_change_list', METADATA,
    Column('new_symbol', String, primary_key=True),
    Column('old_symbol', String, index=True),
    Column('company_name', String, index=True),
    Column('date', TIMESTAMP, index=True)
)

ETF_LIST = Table(
    'etf_list', METADATA,
    Column('symbol', String, primary_key=True),
    Column('name', String, index=True)
)

ACTIVE_TRADING_LIST = Table(
    'active_trading_list', METADATA,
    Column('symbol', String, primary_key=True),
    Column('name', String, index=True)
)

AVAILABLE_EXCHANGES = Table(
    'available_exchanges', METADATA,
    Column('exchange', String, primary_key=True)
)

AVAILABLE_SECTORS = Table(
    'available_sectors', METADATA,
    Column('sector', String, primary_key=True)
)

AVAILABLE_INDUSTRIES = Table(
    'available_industries', METADATA,
    Column('industry', String, primary_key=True)
)

AVAILABLE_COUNTRIES = Table(
    'available_countries', METADATA,
    Column('country', String, primary_key=True)
)
