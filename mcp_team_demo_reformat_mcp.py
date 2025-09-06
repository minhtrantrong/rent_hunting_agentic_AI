import asyncio
import os
from datetime import datetime, timedelta
import sys
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

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

load_dotenv()
if os.path.exists("tmp/agent.db"):
    os.remove("tmp/agent.db")
# Create the storage
storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")
try:
    from mcp_framework import MCPRegistry, MCPClient, setup_mcp_logging
    from mcp_servers import CalendarMCPServer, CommunicationMCPServer, MapsMCPServer
    print("✅ MCP framework and servers loaded")
except ImportError as e:
    print(f"❌ MCP import error: {e}")
    sys.exit(1)

class MCPTeamDemo:
    """
    Complete MCP demonstration for team review
    Shows Agent #3 using Model Context Protocol with real API integration
    """
    
    def __init__(self):
        # Check basic environment
        if not os.getenv('EMAIL_ADDRESS'):
            print("⚠️ No EMAIL_ADDRESS found - using demo mode")
            os.environ['DEMO_MODE'] = 'true'
        
        # Setup MCP logging
        setup_mcp_logging("INFO")
        
        # Initialize MCP architecture
        self.mcp_registry = MCPRegistry()
        self._initialize_mcp_servers()
        self.mcp_client = MCPClient(self.mcp_registry)
        
        print("🏠 RentGenius Agent #3 - MCP Team Demo")
        print("=" * 60)
        print("🤖 Model Context Protocol Architecture")
        print("🚀 Multi-Agent Apartment Hunting Coordination")
        print("🏆 TiDB Hackathon 2025")
        print()
    
    def _initialize_mcp_servers(self):
        """Initialize all MCP servers"""
        try:
            # Calendar MCP Server
            calendar_server = CalendarMCPServer()
            self.mcp_registry.register_server(calendar_server)
            
            # Communication MCP Server  
            comm_server = CommunicationMCPServer()
            self.mcp_registry.register_server(comm_server)
            
            # Maps MCP Server
            maps_server = MapsMCPServer()
            self.mcp_registry.register_server(maps_server)
            
            print("✅ All MCP servers initialized")
            
        except Exception as e:
            print(f"❌ MCP server initialization failed: {e}")
            raise
    
    def demonstrate_mcp_architecture(self):
        """Demonstrate MCP architecture components"""
        print("🏗️ MCP ARCHITECTURE DEMONSTRATION")
        print("=" * 50)
        
        # Show MCP status
        mcp_status = self.mcp_registry.list_servers()
        available_tools = self.mcp_client.list_available_tools()
        
        print("📊 MCP Registry Status:")
        for server_name, server_info in mcp_status.items():
            print(f"   🔧 {server_name}: {server_info['version']} ({len(server_info['tools'])} tools)")
            
        print(f"\n🛠️ Available Tools:")
        for server_name, tool_names in available_tools.items():
            print(f"   {server_name}: {', '.join(tool_names)}")
        
        # Test MCP communication
        print(f"\n🔄 Testing MCP Communication:")
        self._test_mcp_communication()
        
        return True
    
    def _test_mcp_communication(self):
        """Test MCP server communication"""
        
        # Test Calendar MCP Server
        try:
            start_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            end_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
            
            result = self.mcp_client.call(
                "calendar-server",
                "get_availability",
                start_date=start_date,
                end_date=end_date,
                duration_minutes=90
            )
            
            slots = result.get("availability_slots", [])
            print(f"   📅 Calendar Server: Found {len(slots)} available slots")
            
        except Exception as e:
            print(f"   ❌ Calendar Server error: {e}")
        
        # Test Communication MCP Server
        try:
            result = self.mcp_client.call(
                "communication-server",
                "send_email",
                to_email="demo@rentgenius.com",
                subject="MCP Test",
                message="Testing MCP communication server"
            )
            
            status = result.get("status", "unknown")
            print(f"   📧 Communication Server: {status}")
            
        except Exception as e:
            print(f"   ❌ Communication Server error: {e}")
        
        # Test Maps MCP Server
        try:
            result = self.mcp_client.call(
                "maps-server",
                "calculate_travel_time",
                origin="Downtown Austin, TX",
                destination="University of Texas at Austin"
            )
            
            travel_time = result.get("travel_time_minutes", "unknown")
            print(f"   🗺️ Maps Server: {travel_time} minute travel time")
            
        except Exception as e:
            print(f"   ❌ Maps Server error: {e}")

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
demo = MCPTeamDemo()

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
        score += max(0, 30 * (1.5 - (rent / budget)))  # tránh âm

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
    try:
        return demo.mcp_client.call(
            "calendar-server",
            "create_calendar_events",
            selected_properties=selected_properties,
            user_email=user_email
        )
    except Exception as e:
        return {"status": "error", "error": str(e)}

@tool
def send_coordination_email(user_profile: Dict[str, Any], schedule: List[Dict[str, Any]]) -> Dict[str, Any]:
    try:
        message = "\n".join([f"- {evt.get('property')} at {evt.get('time')}" for evt in schedule])
        return demo.mcp_client.call(
            "communication-server",
            "send_email",
            to_email=user_profile["email"],
            subject="Your RentGenius Viewing Schedule",
            message=message
        )
    except Exception as e:
        return {"status": "error", "error": str(e)}

@tool
def optimize_route(properties: List[Dict[str, Any]], start_location: str) -> Dict[str, Any]:
    try:
        return demo.mcp_client.call(
            "maps-server",
            "calculate_travel_time",
            origin=start_location,
            destination=properties[-1]["address"]
        )
    except Exception as e:
        return {"status": "error", "error": str(e)}





# -------------------------
# AGENT
# -------------------------
async def init_agent():
    gemini_model = Gemini(id="gemini-1.5-flash-latest")
    agent = Agent(
        name="MCP Apartment Coordinator",
        model=gemini_model,
        storage=storage,
        tools=[
            get_properties,
            get_regional_data,
            score_property,
            create_calendar_events,
            send_coordination_email,
            optimize_route,
        ],
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
    return agent


if __name__ == "__main__":
    print("🏠 RentGenius Agent #3 - MCP Team Demo")
    print("🤖 Gemini + MCP Tools")
    print("🚀 TiDB Hackathon 2025\n")

    user_profile = {
        "name": "Alex Chen",
        "email": os.getenv("EMAIL_ADDRESS", "demo@rentgenius.com"),
        "lifestyle": "young_professional",
        "budget_max": 4200,
        "current_location": "Downtown Austin, TX",
    }

    async def main():
        agent = await init_agent()
        try:
            while True:
                user_input = input("User: ")
                if not user_input.strip():
                    print("Exiting...")
                    break
                try:
                    agent.print_response(
                        message=f"{user_input}\n\nUser Profile: {user_profile}",
                        markdown=True,
                    )
                except Exception as e:
                    print(f"❌ Agent error: {e}")
        finally:
            if demo and hasattr(demo, "mcp_client"):
                demo.mcp_client.disconnect()
    asyncio.run(main())
