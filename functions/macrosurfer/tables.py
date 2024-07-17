from sqlalchemy import Table, Column, String, Boolean, Double, TIMESTAMP, MetaData

METADATA = MetaData()

ECONOMIC_CALENDAR_TABLE = Table(
    'economic_calendar', METADATA,
    Column('event', String, primary_key=True),
    Column('event_date', TIMESTAMP, primary_key=True),
    Column('country', String),
    Column('currency', String),
    Column('previous', Double),
    Column('estimate', Double),
    Column('actual', Double),
    Column('change', Double),
    Column('impact', String),
    Column('change_percentage', Double),
    Column('unit', String),
)

EVENT_DETAILS = Table(
    'event_details', METADATA,
    Column('event', String, primary_key=True),
    Column('country', String, primary_key=True),
    Column('period', String),
    Column('official_data', Boolean),
    Column('detail', String),
)
