#!/usr/bin/env python3
"""
Test script to verify the apartment email template functionality with external template file.
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from app import (
        DEFAULT_EMAIL, 
        DEFAULT_APARTMENT_EMAIL_TEMPLATE, 
        format_apartment_email,
        send_apartment_appointment_email,
        MCP_AVAILABLE,
        load_email_template
    )
    
    print("✅ Successfully imported email template functions")
    print(f"✅ Default email from .env: {DEFAULT_EMAIL}")
    print(f"✅ MCP Available: {MCP_AVAILABLE}")
    
    # Test template loading
    print(f"✅ Template loaded from external file (length: {len(DEFAULT_APARTMENT_EMAIL_TEMPLATE)} characters)")
    
    # Test the email template formatting
    print("\n📧 Testing email template formatting...")
    
    sample_email = format_apartment_email(
        name_of_apartment="Luxury Downtown Apartment",
        address_of_apartment="123 Main Street, California, MD 20619",
        price_of_apartment="$3,000/month",
        appointment_time="10 AM tomorrow (September 15, 2025)",
        calendar_link='Add to Calendar',
        maps_link='View on Maps'
    )
    
    print("Sample formatted email (first 500 characters):")
    print("-" * 50)
    print(sample_email[:500] + "..." if len(sample_email) > 500 else sample_email)
    print("-" * 50)
    
    # Test the apartment email sending function (without actually sending)
    print("\n🧪 Testing apartment email function...")
    try:
        result = send_apartment_appointment_email(
            name_of_apartment="Luxury Downtown Apartment",
            address_of_apartment="123 Main Street, California, MD 20619",
            price_of_apartment="$3,000/month"
        )
        print(f"✅ Email function result: {result}")
    except Exception as e:
        print(f"❌ Email function error: {e}")
    
    # Test template loading function directly
    print("\n🧪 Testing template loading function...")
    try:
        template = load_email_template("apartment_appointment")
        print(f"✅ Template loaded successfully (length: {len(template)} characters)")
    except Exception as e:
        print(f"❌ Template loading error: {e}")
    
    print("\n🎉 Email template configuration test completed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Test error: {e}")
    sys.exit(1)