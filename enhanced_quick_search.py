#!/usr/bin/env python3
"""
Enhanced Quick Apartment Search and Email
Beautiful HTML emails with Google Maps integration
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, '/Users/comradeflats/Desktop/rent_hunting_agentic_AI')

def get_apartments():
    """Sample apartments for Texas City, Texas under $2000"""
    return [
        {
            "name": "Bayview Gardens",
            "address": "1234 Bay Street, Texas City, TX 77590",
            "price": "$1,850/month",
            "beds": 2,
            "baths": 2,
            "amenities": "Pool, Gym, Parking, Pet-friendly",
            "contact": "(409) 948-1234"
        },
        {
            "name": "Gulf Coast Commons",
            "address": "5678 Gulf Shore Blvd, Texas City, TX 77591",
            "price": "$1,750/month",
            "beds": 2,
            "baths": 2,
            "amenities": "Balcony, Laundry in unit, Parking",
            "contact": "(409) 948-5678"
        },
        {
            "name": "Texas City Heights",
            "address": "9876 Heights Drive, Texas City, TX 77590",
            "price": "$1,950/month",
            "beds": 2,
            "baths": 2.5,
            "amenities": "Garage, Pool, Security, Near shopping",
            "contact": "(409) 948-9876"
        },
        {
            "name": "Coastal Living Apartments",
            "address": "2468 Coastal Way, Texas City, TX 77591",
            "price": "$1,650/month",
            "beds": 2,
            "baths": 1.5,
            "amenities": "Beach access, Parking, Gym",
            "contact": "(409) 948-2468"
        },
        {
            "name": "Marina Point Residences",
            "address": "1357 Marina Circle, Texas City, TX 77590",
            "price": "$1,900/month",
            "beds": 2,
            "baths": 2,
            "amenities": "Marina views, Pool, Concierge, Pet spa",
            "contact": "(409) 948-1357"
        }
    ]

def send_enhanced_apartment_email():
    """Send enhanced apartment listings via email with Google Maps integration"""
    try:
        print("🔍 Gathering apartment data...")
        apartments = get_apartments()

        print("📧 Creating enhanced email content with Google Maps integration...")
        from enhanced_email_utils import send_enhanced_apartment_listings_email

        result = send_enhanced_apartment_listings_email(
            apartments=apartments,
            to_email="ryanwinstonelliott@gmail.com",
            search_criteria="2-bedroom apartments under $2,000/month in Texas City, TX",
            recipient_name="Ryan"
        )

        print(f"✅ Enhanced email sent! Result: {result}")

        print("\n📋 Summary sent to your email:")
        for i, apt in enumerate(apartments, 1):
            print(f"{i:2d}. {apt['name']} - {apt['price']}")
            print(f"    📍 {apt['address']}")
            print(f"    📞 {apt['contact']}")
            print()

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def send_enhanced_appointment_email():
    """Send enhanced appointment email with Google Maps and calendar integration"""
    try:
        print("📅 Creating enhanced appointment email...")
        from enhanced_email_utils import send_enhanced_apartment_appointment_email

        result = send_enhanced_apartment_appointment_email(
            name_of_apartment="Bayview Gardens",
            address_of_apartment="1234 Bay Street, Texas City, TX 77590",
            price_of_apartment="$1,850/month",
            appointment_time="2 PM",
            appointment_date="tomorrow",
            duration_minutes=60,
            to_email="ryanwinstonelliott@gmail.com"
        )

        print(f"✅ Enhanced appointment email sent! Result: {result}")
        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🏠 Enhanced Texas City Apartment Search")
    print("=" * 50)
    print("Demonstrating enhanced email functionality with Google Maps integration...")
    print()

    # Test enhanced apartment listings email
    print("1️⃣ Testing enhanced apartment listings email...")
    success1 = send_enhanced_apartment_email()

    print("\n" + "="*50)

    # Test enhanced appointment email
    print("2️⃣ Testing enhanced appointment email...")
    success2 = send_enhanced_appointment_email()

    print("\n" + "="*50)

    if success1 and success2:
        print("✅ All tests completed successfully!")
        print("📧 Check your email inbox for:")
        print("   • Beautiful apartment listings with Google Maps links")
        print("   • Professional appointment email with calendar integration")
        print("   • Colorful formatting optimized for Gmail")
    else:
        print("❌ Some tests failed. Check the errors above.")

    print("\n🎨 Enhanced features include:")
    print("   • Google Maps integration for each property")
    print("   • Directions links for easy navigation")
    print("   • Click-to-call phone numbers")
    print("   • Beautiful visual card layout")
    print("   • Gmail-optimized calendar integration")
    print("   • Professional color schemes and typography")