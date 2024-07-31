# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`
import json
import os
from datetime import datetime
from decimal import Decimal

# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import firestore_fn, https_fn
from dotenv import load_dotenv
# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore
import google.cloud.firestore
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, MetaData, Table, select, and_
from macrosurfer.tables import ECONOMIC_CALENDAR_TABLE, EVENT_DETAILS

initialize_app()
load_dotenv()

DATABASE_URL = f'postgresql+psycopg2://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST_NAME")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)
# metadata = MetaData()

# # Define your table
# ECONOMIC_CALENDAR_TABLE = Table(
#     'economic_calendar', metadata,
#     autoload_with=engine
# )

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    return https_fn.Response("Hello world!")

def deserialize_row(row):
    return {
        "event": row.event,
        "event_date": row.event_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "country": row.country,
        "currency": row.currency,
        "previous": row.previous,
        "estimate": row.estimate,
        "actual": row.actual,
        "change": row.change,
        "impact": row.impact,
        "change_percentage": row.change_percentage,
        "unit": row.unit
    }

@https_fn.on_request()
def getEventsInDateRange(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the messages collection."""
    # Grab the text parameter.
    start_date = req.args.get("startDate")
    end_date = req.args.get("endDate")
    country = req.args.get("country", "US")

    print("start date: ", start_date)
    print("end date: ", end_date)
    print("country: ", country)

    if not start_date or not end_date:
        return https_fn.Response("startDate and endDate are required", status=400)
    
    with engine.connect() as connection:
        query = select(
            ECONOMIC_CALENDAR_TABLE

        ).where(
            and_(
                ECONOMIC_CALENDAR_TABLE.c.event_date >= text(f"'{start_date}'"),
                ECONOMIC_CALENDAR_TABLE.c.event_date <= text(f"'{end_date}'")
            )
        )
        
        if country:
            query = query.where(ECONOMIC_CALENDAR_TABLE.c.country == country)
        
        result = connection.execute(query)
        events = [deserialize_row(row) for row in result][:15]
        return https_fn.Response(json.dumps(events), status=200)
    
@https_fn.on_request()
def getHistoryForEvent(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the messages collection."""
    # Grab the text parameter.
    event = req.args.get("event")
    country = req.args.get("country", "US")
    end_date = req.args.get("endDate")
    start_date = req.args.get("startDate")

    print("start date: ", start_date)
    print("end date: ", end_date)
    print("event: ", event)

    if not event or not country:
        return https_fn.Response("Event and country name are required", status=400)
    
    with engine.connect() as connection:
        query = select(
            ECONOMIC_CALENDAR_TABLE

        ).where(
            and_(
                ECONOMIC_CALENDAR_TABLE.c.country == country,
                ECONOMIC_CALENDAR_TABLE.c.event.like(f"%{event}%")
            )
        )
        
        if start_date and end_date:
            query = query.where(
                and_(
                    ECONOMIC_CALENDAR_TABLE.c.event_date >= text(f"'{start_date}'"),
                    ECONOMIC_CALENDAR_TABLE.c.event_date <= text(f"'{end_date}'")
                )
            )

        result = connection.execute(query)
        events = [deserialize_row(row) for row in result][:15]
        return https_fn.Response(json.dumps(events), status=200)


@https_fn.on_request()
def getEventDetails(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the messages collection."""
    # Grab the text parameter.
    event = req.args.get("event")
    country = req.args.get("country")

    if not event or not country:
        return https_fn.Response("Event and country name are required", status=400)
    
    with engine.connect() as connection:
        query = select(
            EVENT_DETAILS

        ).where(
            and_(
                EVENT_DETAILS.c.country == country,
                EVENT_DETAILS.c.event == event
            )
        )
        result = connection.execute(query)
        events = [dict(row._mapping) for row in result]
        if len(events) == 0:
            return https_fn.Response("No details found", status=404)
        return https_fn.Response(json.dumps(events[0]), status=200)
