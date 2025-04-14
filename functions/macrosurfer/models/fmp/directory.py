from sqlalchemy import Table, Column, String

from macrosurfer.models.metadata import METADATA

COMPANY_SYMBOLS = Table(
    'company_symbols', METADATA,
    Column('symbol', String, primary_key=True),
    Column('company_name', String)
)
