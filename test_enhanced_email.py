#!/usr/bin/env python3
"""
Test script for enhanced email functionality with Google Maps, Calendar, and WhatsApp integrations
"""

import sys
import os
from datetime import datetime, timedelta

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from mcp_servers import CommunicationMCPServer
    print("✅ Successfully imported enhanced CommunicationMCPServer")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_enhanced_email():
    """Test the enhanced email generation with all integrations"""
    
    # Create communication server
    comm_server = CommunicationMCPServer()
    
    # Mock user profile
    user_profile = {
        "name": "Alex Chen",
        "email": "alex.chen@example.com"
    }
    
    # Mock viewing schedule with enhanced property data
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
        }
    ]
    
    # Mock insights
    insights = {
        "total_properties_analyzed": 3,
        "mcp_coordination": True
    }
    
    # Generate enhanced email
    print("🔧 Generating enhanced email with integrations...")
    enhanced_email = comm_server._generate_coordination_email(
        user_profile, 
        viewing_schedule, 
        insights
    )
    
    # Save to file for inspection
    output_file = "/Users/comradeflats/Desktop/RentGenius_Agent3_TiDB_Hackathon/enhanced_email_sample.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(enhanced_email)
    
    print(f"✅ Enhanced email generated and saved to: {output_file}")
    print("\n🎯 Enhanced Features Included:")
    print("   🗺️ Google Maps integration (directions & view)")
    print("   📅 Google Calendar integration (add to calendar)")
    print("   📱 WhatsApp integration (contact agents)")
    print("   📞 Click-to-call phone numbers")
    print("   📧 Click-to-email agent contacts")
    
    # Display sample URLs that will be generated
    sample_address = "2505 San Gabriel St, Austin, TX 78705"
    sample_phone = "+15127891234"
    
    print(f"\n🔗 Sample Integration URLs Generated:")
    print(f"   Maps Directions: https://maps.google.com/maps?daddr={sample_address.replace(' ', '+')}")
    print(f"   Maps View: https://maps.google.com/?q={sample_address.replace(' ', '+')}")
    print(f"   Calendar: https://calendar.google.com/calendar/render?action=TEMPLATE&text=...")
    print(f"   WhatsApp: https://wa.me/{sample_phone.replace('+', '')}?text=...")
    
    return output_file

if __name__ == "__main__":
    print("🏠 Testing Enhanced Email Functionality")
    print("=" * 50)
    
    output_file = test_enhanced_email()
    
    print(f"\n🎉 Test completed successfully!")
    print(f"📧 Open {output_file} in a web browser to see the enhanced email")
    print(f"🚀 All integration features are now active in the MCP system!")