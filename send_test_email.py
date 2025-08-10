#!/usr/bin/env python3
"""
Send a test email with the enhanced integrations
"""

import sys
import os
from datetime import datetime, timedelta

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set email credentials
os.environ['EMAIL_ADDRESS'] = 'ryanwinstonelliott@gmail.com'
os.environ['EMAIL_PASSWORD'] = 'lydh msld dwro ojvc'

try:
    from mcp_servers import CommunicationMCPServer
    from mcp_framework import MCPRegistry, MCPClient
    print("✅ Successfully imported MCP components")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def send_enhanced_email():
    """Send the enhanced email with all integrations"""
    
    recipient_email = 'ryanwinstonelliott@gmail.com'  # Send to yourself for testing
    
    print(f"🚀 Sending enhanced email with integrations...")
    print(f"📧 From: ryanwinstonelliott@gmail.com")
    print(f"📨 To: {recipient_email}")
    
    # Create MCP registry and communication server
    registry = MCPRegistry()
    comm_server = CommunicationMCPServer()
    registry.register_server(comm_server)
    client = MCPClient(registry)
    
    # Mock user profile
    user_profile = {
        "name": "Ryan Elliott",
        "email": recipient_email
    }
    
    # Enhanced viewing schedule with all integration data
    viewing_schedule = [
        {
            "property": {
                "name": "The Independent",
                "address": "2505 San Gabriel St, Austin, TX 78705",
                "price": "$3,800/month",
                "agent_name": "Sarah Martinez",
                "agent_contact": {
                    "phone": "+15127891234",
                    "email": "sarah.martinez@theindependent.com"
                }
            },
            "time_slot": {
                "start": (datetime.now() + timedelta(days=1)).replace(hour=14, minute=0).isoformat(),
                "end": (datetime.now() + timedelta(days=1)).replace(hour=16, minute=0).isoformat()
            },
            "coordination_score": 84.0
        },
        {
            "property": {
                "name": "East Austin Loft",
                "address": "2400 E 6th St, Austin, TX 78702",
                "price": "$3,200/month",
                "agent_name": "Michael Chen",
                "agent_contact": {
                    "phone": "+15125551987",
                    "email": "michael.chen@eastaustinloft.com"
                }
            },
            "time_slot": {
                "start": (datetime.now() + timedelta(days=2)).replace(hour=10, minute=0).isoformat(),
                "end": (datetime.now() + timedelta(days=2)).replace(hour=12, minute=0).isoformat()
            },
            "coordination_score": 77.6
        },
        {
            "property": {
                "name": "South Lamar Modern",
                "address": "1900 S Lamar Blvd, Austin, TX 78704",
                "price": "$4,100/month",
                "agent_name": "Jessica Williams",
                "agent_contact": {
                    "phone": "+15124567890",
                    "email": "j.williams@southlamarmodern.com"
                }
            },
            "time_slot": {
                "start": (datetime.now() + timedelta(days=3)).replace(hour=15, minute=30).isoformat(),
                "end": (datetime.now() + timedelta(days=3)).replace(hour=17, minute=30).isoformat()
            },
            "coordination_score": 71.2
        }
    ]
    
    # Multi-agent insights
    insights = {
        "total_properties_analyzed": 5,
        "regional_data_integrated": True,
        "mcp_coordination": True,
        "coordination_timestamp": datetime.now().isoformat()
    }
    
    print(f"🏠 Properties: {len(viewing_schedule)} viewings scheduled")
    
    try:
        # Send via MCP Communication Server
        result = client.call(
            "communication-server",
            "send_coordination_email",
            user_profile=user_profile,
            viewing_schedule=viewing_schedule,
            multi_agent_insights=insights,
            template_style="professional"
        )
        
        print(f"\n✅ Email sent successfully!")
        print(f"📊 Status: {result.get('status', 'sent')}")
        
        print(f"\n🎯 Enhanced Features Included in Email:")
        print(f"   🗺️ Google Maps integration (directions & view)")
        print(f"   📅 Google Calendar integration (add to calendar)")
        print(f"   📱 WhatsApp integration (contact agents)")
        print(f"   📞 Click-to-call phone numbers")
        print(f"   📧 Click-to-email agent contacts")
        
        print(f"\n📲 Check your email inbox at: {recipient_email}")
        print(f"🔍 Look for subject: '🏠 Your 3 Apartment Viewings Are Ready!'")
        
    except Exception as e:
        print(f"\n❌ Failed to send email: {e}")
        print(f"💡 Error details: {str(e)}")

if __name__ == "__main__":
    print("🏠 RentGenius Enhanced Email Test")
    print("🚀 Send Real Email with Google Maps, Calendar & WhatsApp Integration")
    print("=" * 70)
    
    send_enhanced_email()
    
    print(f"\n🎉 Test completed!")
    print(f"📧 Check your Gmail inbox and test all the integration buttons!")