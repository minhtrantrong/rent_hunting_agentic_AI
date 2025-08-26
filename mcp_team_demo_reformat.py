import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
from urllib.parse import quote_plus
from dotenv import load_dotenv

# agno imports
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools import tool
import mysql.connector

# TiDB / SQLAlchemy / LlamaIndex
from sqlalchemy import URL, create_engine, text
from llama_index.vector_stores.tidbvector import TiDBVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from agno.storage.sqlite import SqliteStorage

# Google + Email
from google.oauth2 import service_account
from googleapiclient.discovery import build
import smtplib
from email.mime.text import MIMEText
import requests

load_dotenv()
if os.path.exists("tmp/agent.db"):
    os.remove("tmp/agent.db")
# Create the storage
storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")


# The database connection function now reads from the loaded environment variables
def get_tidb_connection():
    return mysql.connector.connect(
        host=os.getenv("TIDB_HOST"),
        user=os.getenv("TIDB_USER"),
        password=os.getenv("TIDB_PASSWORD"),
        database=os.getenv("TIDB_DATABASE")
    )

# -------------------------
# TOOLS
# -------------------------

@tool
def get_properties() -> List[Dict[str, Any]]:
    """Simulates Agent #1: property intelligence with investment metrics."""
    return [
        {
            "property_id": "mcp_prop_001",
            "name": "The Independent",
            "address": "2505 San Gabriel St, Austin, TX 78705",
            "price_analysis": {"monthly_rent": 3800, "affordability_score": 8.2, "market_position": "competitive"},
            "investment_metrics": {"roi_projection": 7.8, "rental_demand": "high"},
            "risk_assessment": {"overall_risk": "low"},
            "property_features": {"bedrooms": 2, "bathrooms": 2, "sqft": 950},
        },
        {
            "property_id": "mcp_prop_002",
            "name": "East Austin Loft",
            "address": "2400 E 6th St, Austin, TX 78702",
            "price_analysis": {"monthly_rent": 3200, "affordability_score": 8.8, "market_position": "value"},
            "investment_metrics": {"roi_projection": 8.4, "rental_demand": "very_high"},
            "risk_assessment": {"overall_risk": "low"},
            "property_features": {"bedrooms": 2, "bathrooms": 1, "sqft": 850},
        },
        {
            "property_id": "mcp_prop_003",
            "name": "South Lamar Modern",
            "address": "1900 S Lamar Blvd, Austin, TX 78704",
            "price_analysis": {"monthly_rent": 4100, "affordability_score": 7.5, "market_position": "premium"},
            "investment_metrics": {"roi_projection": 6.9, "rental_demand": "high"},
            "risk_assessment": {"overall_risk": "moderate"},
            "property_features": {"bedrooms": 2, "bathrooms": 2, "sqft": 1100},
        },
    ]


@tool
def get_regional_data() -> Dict[str, Any]:
    """Simulates Agent #2: regional intelligence for Austin, TX."""
    return {
        "region_name": "Austin, TX - Central District",
        "safety_score": 8.4,
        "walkability": 82,
        "lifestyle_fit": {"young_professional": 8.9, "family_friendly": 7.2, "student_oriented": 8.1},
        "market_trends": {"rental_growth": 0.065, "occupancy_rate": 0.94},
    }


@tool
def score_property(property: Dict[str, Any], regional_data: Dict[str, Any], user_profile: Dict[str, Any]) -> float:
    """Scores a property based on multi-agent metrics."""
    rent = property["price_analysis"]["monthly_rent"]
    budget = user_profile["budget_max"]

    score = 0.0
    if rent <= budget:
        score += 30 * (1.5 - (rent / budget))

    score += (property["price_analysis"]["affordability_score"] / 10.0) * 20
    score += min(property["investment_metrics"]["roi_projection"] / 10.0, 1.0) * 15
    score += {"low": 10, "moderate": 5, "high": 0}[property["risk_assessment"]["overall_risk"]]

    lifestyle = user_profile["lifestyle"]
    score += (regional_data["lifestyle_fit"].get(lifestyle, 7.0) / 10.0) * 15
    score += (regional_data["safety_score"] / 10.0) * 5
    score += (regional_data["walkability"] / 100.0) * 5

    return round(min(score, 100.0), 1)





@tool
def create_calendar_events(selected_properties: List[Dict[str, Any]], user_email: str) -> Dict[str, Any]:
    """Schedules viewing events for selected properties using Google Calendar API."""
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_CALENDAR_CREDENTIALS"),
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    service = build("calendar", "v3", credentials=creds)

    events = []
    for i, prop in enumerate(selected_properties, 1):
        event_start = (datetime.utcnow() + timedelta(days=i, hours=10))
        event_end = event_start + timedelta(hours=1)

        event = {
            "summary": f"Viewing: {prop['name']}",
            "location": prop["address"],
            "description": f"Property viewing scheduled by RentGenius for {user_email}",
            "start": {"dateTime": event_start.isoformat() + "Z"},
            "end": {"dateTime": event_end.isoformat() + "Z"},
            "attendees": [{"email": user_email}],
        }

        created = service.events().insert(calendarId="primary", body=event).execute()
        events.append({"event_id": created["id"], "property": prop["name"], "time": created["start"]["dateTime"]})

    return {"events_created": events, "status": "success"}



@tool
def send_coordination_email(user_profile: Dict[str, Any], schedule: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Sends a coordination email with the property viewing schedule via Gmail SMTP."""
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = user_profile["email"]

    body = "📅 Property Viewing Schedule:\n\n"
    for evt in schedule:
        body += f"- {evt['property']} at {evt['time']}\n"

    msg = MIMEText(body)
    msg["Subject"] = "Your RentGenius Viewing Schedule"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        return {"status": "sent", "to": receiver, "viewings": schedule}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@tool
def optimize_route(properties: List[Dict[str, Any]], start_location: str) -> Dict[str, Any]:
    """Optimizes the route for property viewings using Google Maps Directions API."""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    waypoints = "|".join([p["address"] for p in properties])

    url = (
        f"https://maps.googleapis.com/maps/api/directions/json"
        f"?origin={start_location}"
        f"&destination={properties[-1]['address']}"
        f"&waypoints=optimize:true|{waypoints}"
        f"&key={api_key}"
    )

    resp = requests.get(url)
    data = resp.json()

    if data.get("status") != "OK":
        return {"status": "error", "error": data.get("status", "Unknown error")}

    order = data["routes"][0]["waypoint_order"]
    optimized_order = [properties[i]["name"] for i in order]

    return {"status": "success", "optimized_order": optimized_order}


# -------------------------
# AGENT
# -------------------------

gemini_model = Gemini(id="gemini-1.5-flash-latest")

agent = Agent(
    name="MCP Apartment Coordinator",
    model=gemini_model,
    storage=storage,
    tools=[get_properties, get_regional_data, score_property, create_calendar_events, send_coordination_email, optimize_route],
    description="Agent that demonstrates Model Context Protocol via tool-augmented reasoning.",
    instructions=[
        "Use get_properties and get_regional_data to collect data.",
        "Use score_property to evaluate properties for the user.",
        "Select the top 2 properties and coordinate next steps.",
        "Schedule viewings with create_calendar_events.",
        "Send user an email with send_coordination_email.",
        "Optimize the route with optimize_route.",
        "Always explain reasoning and show results in tables.",
    ],
    show_tool_calls=True,
    add_history_to_messages=True,
    num_history_runs=3,
    markdown=True,
)


if __name__ == "__main__":
    print("🏠 RentGenius Agent #3 - MCP Team Demo")
    print("🤖 Rewritten with Gemini Agent + Tools")
    print("🚀 TiDB Hackathon 2025\n")

    user_profile = {
        "name": "Alex Chen",
        "email": os.getenv("EMAIL_ADDRESS", "demo@rentgenius.com"),
        "lifestyle": "young_professional",
        "budget_max": 4200,
        "current_location": "Downtown Austin, TX",
    }

    while True:
        user_input = input("User: ")
        if user_input.strip() == "":
            print("Exiting...")
            break

        agent.print_response(
            message=f"{user_input}\n\nUser Profile: {user_profile}",
            markdown=True,
        )
