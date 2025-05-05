from sqlalchemy import Table, Column, String, Boolean, Double, TIMESTAMP
from macrosurfer.models.metadata import METADATA

STOCK_PRICE_1_MIN_TABLE = Table(
    'stock_price_1_min', METADATA,
    Column('symbol', String, primary_key=True),
    Column('date', TIMESTAMP, primary_key=True),
    Column('open', Double),
    Column('high', Double),
    Column('low', Double),
    Column('close', Double),
    Column('volume', Double))

STOCK_PRICE_1_DAY_TABLE = Table(
    'stock_price_1_day', METADATA,
    Column('symbol', String, primary_key=True),
    Column('date', TIMESTAMP, primary_key=True),
    Column('open', Double),
    Column('high', Double),
    Column('low', Double),
    Column('close', Double),
    Column('volume', Double),
    Column('change', Double),
    Column('change_percentage', Double),
    Column('vwap', Double)
)
