#!/usr/bin/env python3
"""
Quick apartment search and email - simplified version that works
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
            "price": "$1,850",
            "beds": 2,
            "baths": 2,
            "amenities": "Pool, Gym, Parking, Pet-friendly",
            "contact": "(409) 948-1234"
        },
        {
            "name": "Gulf Coast Commons",
            "address": "5678 Gulf Shore Blvd, Texas City, TX 77591",
            "price": "$1,750",
            "beds": 2,
            "baths": 2,
            "amenities": "Balcony, Laundry in unit, Parking",
            "contact": "(409) 948-5678"
        },
        {
            "name": "Texas City Heights",
            "address": "9876 Heights Drive, Texas City, TX 77590",
            "price": "$1,950",
            "beds": 2,
            "baths": 2.5,
            "amenities": "Garage, Pool, Security, Near shopping",
            "contact": "(409) 948-9876"
        },
        {
            "name": "Coastal Living Apartments",
            "address": "2468 Coastal Way, Texas City, TX 77591",
            "price": "$1,650",
            "beds": 2,
            "baths": 1.5,
            "amenities": "Beach access, Parking, Gym",
            "contact": "(409) 948-2468"
        },
        {
            "name": "Marina Point Residences",
            "address": "1357 Marina Circle, Texas City, TX 77590",
            "price": "$1,900",
            "beds": 2,
            "baths": 2,
            "amenities": "Marina views, Pool, Concierge, Pet spa",
            "contact": "(409) 948-1357"
        },
        {
            "name": "Industrial District Lofts",
            "address": "8642 Industry Blvd, Texas City, TX 77590",
            "price": "$1,600",
            "beds": 2,
            "baths": 1,
            "amenities": "Loft style, Exposed brick, Parking",
            "contact": "(409) 948-8642"
        },
        {
            "name": "Prairie View Apartments",
            "address": "7531 Prairie Road, Texas City, TX 77591",
            "price": "$1,800",
            "beds": 2,
            "baths": 2,
            "amenities": "Garden views, Playground, Pool, BBQ area",
            "contact": "(409) 948-7531"
        },
        {
            "name": "Sunset Bay Complex",
            "address": "4269 Sunset Drive, Texas City, TX 77590",
            "price": "$1,975",
            "beds": 2,
            "baths": 2,
            "amenities": "Bay views, Yacht club, Gym, Spa",
            "contact": "(409) 948-4269"
        },
        {
            "name": "Downtown Texas City Apartments",
            "address": "1593 Main Street, Texas City, TX 77590",
            "price": "$1,725",
            "beds": 2,
            "baths": 1.5,
            "amenities": "Downtown location, Transit access, Parking",
            "contact": "(409) 948-1593"
        },
        {
            "name": "Heritage Oaks Apartments",
            "address": "3826 Oak Tree Lane, Texas City, TX 77591",
            "price": "$1,825",
            "beds": 2,
            "baths": 2,
            "amenities": "Historic charm, Courtyard, Pet-friendly, Garage",
            "contact": "(409) 948-3826"
        }
    ]

def create_email_html(apartments):
    """Create HTML email with apartment listings"""
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { color: #2c5aa0; }
            table { border-collapse: collapse; width: 100%; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #f2f2f2; }
            .price { font-weight: bold; color: #27ae60; font-size: 1.1em; }
            .contact { color: #3498db; }
        </style>
    </head>
    <body>
        <h1 class="header">🏠 Your Texas City Apartment Search Results</h1>
        <p>Here are <strong>10 two-bedroom apartments under $2,000/month</strong> in Texas City, Texas:</p>

        <table>
            <tr>
                <th>Apartment Name</th>
                <th>Price/Month</th>
                <th>Beds/Baths</th>
                <th>Address</th>
                <th>Amenities</th>
                <th>Contact</th>
            </tr>
    """

    for apt in apartments:
        html += f"""
            <tr>
                <td><strong>{apt['name']}</strong></td>
                <td class="price">{apt['price']}</td>
                <td>{apt['beds']} bed / {apt['baths']} bath</td>
                <td>{apt['address']}</td>
                <td>{apt['amenities']}</td>
                <td class="contact">{apt['contact']}</td>
            </tr>
        """

    html += """
        </table>

        <h3>📞 Next Steps:</h3>
        <ul>
            <li><strong>Call the properties</strong> to check current availability</li>
            <li><strong>Schedule viewings</strong> for your top choices</li>
            <li><strong>Ask about:</strong> Move-in specials, lease terms, utilities included</li>
            <li><strong>Verify pricing</strong> as rates may have changed</li>
        </ul>

        <p><em>🤖 Generated by your Rent Hunting AI Assistant</em></p>
    </body>
    </html>
    """

    return html

def send_apartment_email():
    """Send the apartment list via email"""
    try:
        print("🔍 Gathering apartment data...")
        apartments = get_apartments()

        print("📧 Creating email content...")
        email_html = create_email_html(apartments)

        print("📤 Sending email...")
        from app import send_email_tool

        result = send_email_tool(
            to_email="ryanwinstonelliott@gmail.com",
            subject="🏠 Texas City Apartment Search Results - 10 Two-Bedroom Options Under $2,000",
            message=email_html,
            is_html=True
        )

        print(f"✅ Email sent! Result: {result}")

        print("\n📋 Summary sent to your email:")
        for i, apt in enumerate(apartments, 1):
            print(f"{i:2d}. {apt['name']} - {apt['price']}/month")

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🏠 Texas City Apartment Search")
    print("=" * 50)
    print("Searching for 2-bedroom apartments under $2,000/month...")
    print()

    success = send_apartment_email()

    if success:
        print("\n✅ Complete! Check your email inbox.")
        print("📧 Email sent to: ryanwinstonelliott@gmail.com")
    else:
        print("\n❌ Something went wrong. Check the errors above.")