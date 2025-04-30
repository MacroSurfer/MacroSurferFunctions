# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`
import json
import os
from datetime import datetime
from decimal import Decimal

# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import https_fn, options
from dotenv import load_dotenv
# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app
from sqlalchemy.sql import text
from sqlalchemy import create_engine, select, and_
from macrosurfer.models.fmp.economics import ECONOMIC_CALENDAR_TABLE, EVENT_DETAILS
from macrosurfer.database import Database
from langchain.chat_models import ChatOpenAI
from macrosurfer.agent.query_agent import QueryAgent

initialize_app()
load_dotenv()

# Replace the direct database connection with Database class
db = Database()
engine = db.get_engine()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=0, model="gpt-4o")
query_agent = QueryAgent(db, llm)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
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

@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
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
    
    with db.get_engine().connect() as connection:
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
    
@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
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
    
    with db.get_engine().connect() as connection:
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


@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def getEventDetails(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the messages collection."""
    # Grab the text parameter.
    event = req.args.get("event")
    country = req.args.get("country")

    if not event or not country:
        return https_fn.Response("Event and country name are required", status=400)
    
    with db.get_engine().connect() as connection:
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

@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def chat(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the messages collection."""
    # Grab the text parameter.
    question = req.args.get("question")

    if not question:
        return https_fn.Response("Please ask a question", status=400)
    
    result = query_agent.query(question)
    return https_fn.Response(result, status=200)
