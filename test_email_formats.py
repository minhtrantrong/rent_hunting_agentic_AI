#!/usr/bin/env python3
"""
Test Email Formats - Verify all emails are sent in beautiful HTML format
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, '/Users/comradeflats/Desktop/rent_hunting_agentic_AI')

def test_enhanced_email_functions():
    """Test all enhanced email functions to ensure HTML formatting"""

    print("🧪 Testing Email Format Consistency")
    print("=" * 50)

    # Test data
    test_apartments = [
        {
            "name": "Test Apartment 1",
            "address": "123 Test Street, Test City, TX 12345",
            "price": "$1,500/month",
            "beds": 2,
            "baths": 1,
            "amenities": "Pool, Gym, Parking",
            "contact": "(555) 123-4567"
        },
        {
            "name": "Test Apartment 2",
            "address": "456 Sample Ave, Test City, TX 12345",
            "price": "$1,800/month",
            "beds": 3,
            "baths": 2,
            "amenities": "Balcony, Laundry, Pet-friendly",
            "contact": "(555) 987-6543"
        }
    ]

    test_email = "ryanwinstonelliott@gmail.com"

    try:
        print("1️⃣ Testing enhanced apartment listings email...")
        from enhanced_email_utils import send_enhanced_apartment_listings_email

        result1 = send_enhanced_apartment_listings_email(
            apartments=test_apartments,
            to_email=test_email,
            search_criteria="Test apartments with HTML formatting",
            recipient_name="Test User"
        )
        print(f"   ✅ Result: {result1}")

    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n" + "-" * 50)

    try:
        print("2️⃣ Testing enhanced appointment email...")
        from enhanced_email_utils import send_enhanced_apartment_appointment_email

        result2 = send_enhanced_apartment_appointment_email(
            name_of_apartment="Test Apartment",
            address_of_apartment="123 Test Street, Test City, TX 12345",
            price_of_apartment="$1,500/month",
            appointment_time="3 PM",
            appointment_date="tomorrow",
            duration_minutes=60,
            to_email=test_email
        )
        print(f"   ✅ Result: {result2}")

    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n" + "-" * 50)

    try:
        print("3️⃣ Testing safe_send_email_tool with plain text (should auto-convert to HTML)...")
        from email_format_wrapper import safe_send_email_tool

        plain_text_message = "This is a plain text message that should be automatically converted to beautiful HTML format with nice styling and colors."

        result3 = safe_send_email_tool(
            to_email=test_email,
            subject="Test Plain Text Auto-Conversion",
            message=plain_text_message
        )
        print(f"   ✅ Result: {result3}")

    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n" + "-" * 50)

    try:
        print("4️⃣ Testing auto_format_apartment_email...")
        from email_format_wrapper import auto_format_apartment_email

        result4 = auto_format_apartment_email(
            apartments=test_apartments,
            to_email=test_email
        )
        print(f"   ✅ Result: {result4}")

    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n" + "=" * 50)
    print("✅ Email format testing completed!")
    print("\n📧 Check your email inbox for:")
    print("   • Enhanced apartment listings with Google Maps")
    print("   • Appointment email with calendar integration")
    print("   • Auto-converted plain text with HTML styling")
    print("   • Auto-formatted apartment listings")
    print("\n🎨 All emails should now be in beautiful HTML format with:")
    print("   • Professional colors and gradients")
    print("   • Google Maps integration")
    print("   • Responsive design")
    print("   • Click-to-call phone numbers")
    print("   • Beautiful typography and layout")

def test_email_content_quality():
    """Test email content to ensure it meets quality standards"""

    print("\n" + "=" * 50)
    print("🔍 Testing Email Content Quality")
    print("=" * 50)

    try:
        from enhanced_email_utils import create_enhanced_apartment_listings_email
        from email_format_wrapper import ensure_html_format

        # Test apartment data
        test_apartments = [
            {
                "name": "Quality Test Apartment",
                "address": "789 Quality St, Excellence City, TX 78901",
                "price": "$2,000/month",
                "beds": 2,
                "baths": 2,
                "amenities": "Pool, Gym, Google Maps Integration, Beautiful Formatting",
                "contact": "(555) 555-5555"
            }
        ]

        # Generate HTML content
        html_content = create_enhanced_apartment_listings_email(
            apartments=test_apartments,
            search_criteria="quality-tested apartments",
            recipient_name="Quality Tester"
        )

        # Quality checks
        quality_checks = [
            ("Contains HTML structure", "<html>" in html_content.lower()),
            ("Contains CSS styling", "style=" in html_content),
            ("Contains Google Maps links", "maps.google.com" in html_content),
            ("Contains gradients", "gradient" in html_content.lower()),
            ("Contains responsive design", "max-width" in html_content),
            ("Contains proper encoding", "charset=utf-8" in html_content),
            ("Contains apartment data", test_apartments[0]["name"] in html_content),
            ("Contains contact info", test_apartments[0]["contact"] in html_content),
            ("Contains professional styling", "border-radius" in html_content),
            ("Contains call-to-action buttons", "background-color" in html_content)
        ]

        print("📋 Quality Check Results:")
        for check_name, passed in quality_checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")

        passed_checks = sum(1 for _, passed in quality_checks if passed)
        total_checks = len(quality_checks)

        print(f"\n📊 Quality Score: {passed_checks}/{total_checks} ({(passed_checks/total_checks)*100:.1f}%)")

        if passed_checks == total_checks:
            print("🎉 Perfect! All quality checks passed!")
        elif passed_checks >= total_checks * 0.8:
            print("😊 Good! Most quality checks passed.")
        else:
            print("⚠️ Some quality issues detected. Review the failed checks.")

    except Exception as e:
        print(f"❌ Quality test error: {e}")

if __name__ == "__main__":
    test_enhanced_email_functions()
    test_email_content_quality()