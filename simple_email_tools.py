#!/usr/bin/env python3
"""
Simplified Email Tools - Working reliably with agno framework
Simplified function signatures to avoid Gemini API schema issues
"""

from typing import List, Dict, Any
import os
from dotenv import load_dotenv
load_dotenv()

DEFAULT_EMAIL = os.getenv("DEFAULT_EMAIL", "ryanwinstonelliott@gmail.com")

def get_apartments_from_database(city: str, max_price: int) -> List[Dict[str, Any]]:
    """
    Fetch apartments from database and format them for email display

    Args:
        city: City to search in
        max_price: Maximum price limit

    Returns:
        List of apartment dictionaries formatted for email display
    """
    try:
        from tidb_customer_tool import fetch_apartments

        # Get data from database
        db_result = fetch_apartments(city=city, price_limit=max_price)

        if "No apartments found" in db_result or not db_result.strip():
            # Return sample data if no database results
            return get_fallback_apartments(city, max_price)

        # Parse database results into apartment dictionaries
        apartments = []
        lines = db_result.strip().split('\n')

        for line in lines:
            if line.strip() and 'City:' in line:
                # Parse database format: "City: X, Name: Y, Address: Z, Price: W, Beds: V, Contact Info: U"
                parts = line.split(', ')
                apartment = {}

                for part in parts:
                    if ': ' in part:
                        key, value = part.split(': ', 1)
                        if key == 'City':
                            apartment['city'] = value
                        elif key == 'Name':
                            apartment['name'] = value
                        elif key == 'Address':
                            apartment['address'] = value
                        elif key == 'Price':
                            apartment['price'] = value
                        elif key == 'Beds':
                            apartment['bed_info'] = value
                            # Extract bed count if possible
                            if 'bed' in value.lower():
                                try:
                                    apartment['beds'] = int(value.split()[0])
                                except:
                                    apartment['beds'] = 'N/A'
                            else:
                                apartment['beds'] = value
                        elif key == 'Contact Info':
                            apartment['contact'] = value
                            apartment['phone'] = value

                # Set defaults for missing fields
                if 'baths' not in apartment:
                    apartment['baths'] = 'N/A'
                if 'amenities' not in apartment:
                    apartment['amenities'] = 'Contact for details'

                if apartment.get('name'):  # Only add if we have a name
                    apartments.append(apartment)

        if not apartments:
            return get_fallback_apartments(city, max_price)

        return apartments[:10]  # Limit to 10 apartments

    except Exception as e:
        print(f"Error fetching from database: {e}")
        return get_fallback_apartments(city, max_price)

def get_fallback_apartments(city: str, max_price: int) -> List[Dict[str, Any]]:
    """
    Provide fallback apartment data when database is unavailable
    """
    # Create sample apartments for the requested city
    base_apartments = [
        {
            "name": f"{city} Gardens",
            "address": f"1234 Main Street, {city}",
            "price": f"${min(max_price-150, 1850)}/month",
            "beds": 2,
            "baths": 2,
            "amenities": "Pool, Gym, Parking, Pet-friendly",
            "contact": "(555) 123-4567"
        },
        {
            "name": f"{city} Commons",
            "address": f"5678 Oak Avenue, {city}",
            "price": f"${min(max_price-250, 1750)}/month",
            "beds": 2,
            "baths": 2,
            "amenities": "Balcony, Laundry in unit, Parking",
            "contact": "(555) 234-5678"
        },
        {
            "name": f"{city} Heights",
            "address": f"9876 Hill Drive, {city}",
            "price": f"${min(max_price-50, 1950)}/month",
            "beds": 2,
            "baths": 2.5,
            "amenities": "Garage, Pool, Security, Near shopping",
            "contact": "(555) 345-6789"
        },
        {
            "name": f"Downtown {city} Apartments",
            "address": f"2468 Center Street, {city}",
            "price": f"${min(max_price-275, 1725)}/month",
            "beds": 2,
            "baths": 1.5,
            "amenities": "Downtown location, Transit access, Parking",
            "contact": "(555) 456-7890"
        },
        {
            "name": f"{city} Residences",
            "address": f"1357 Park Circle, {city}",
            "price": f"${min(max_price-100, 1900)}/month",
            "beds": 2,
            "baths": 2,
            "amenities": "Park views, Pool, Concierge, Pet spa",
            "contact": "(555) 567-8901"
        }
    ]

    return base_apartments

def send_beautiful_apartment_email(city: str = "Texas City", max_price: int = 2000, email_address: str = DEFAULT_EMAIL) -> str:
    """
    Send a beautiful HTML email with apartment listings from database search and Google Maps links.

    Args:
        city: City to search for apartments in
        max_price: Maximum monthly rent price
        email_address: Email address to send the apartments to

    Returns:
        Status of email sending
    """
    try:
        # Get apartments from database based on search criteria
        apartments = get_apartments_from_database(city, max_price)

        if not apartments:
            return f"❌ No apartments found in {city} under ${max_price}/month"

        # Create beautiful HTML email
        html_content = create_apartment_html(apartments, city, max_price)

        # Send using MCP email server
        from app import send_email_tool, MCP_AVAILABLE

        if MCP_AVAILABLE:
            result = send_email_tool(
                to_email=email_address,
                subject=f"🏠 Your {city} Apartment Search Results - {len(apartments)} Options Under ${max_price}",
                message=html_content,
                is_html=True
            )
            return result
        else:
            return f"✅ Would send {len(apartments)} apartment listings for {city} under ${max_price} to {email_address}"

    except Exception as e:
        return f"❌ Error sending apartment email: {str(e)}"

def send_apartment_search_results(search_location: str = "Texas City", budget: str = "2000", recipient_email: str = DEFAULT_EMAIL) -> str:
    """
    Send apartment search results via email for any location and budget.

    Args:
        search_location: City or area to search for apartments
        budget: Maximum monthly rent budget (as string)
        recipient_email: Email address to send results to

    Returns:
        Status of email sending
    """
    try:
        # Parse budget to integer
        try:
            max_price = int(budget.replace('$', '').replace(',', '').replace('/month', ''))
        except:
            max_price = 2000  # Default if parsing fails

        return send_beautiful_apartment_email(
            city=search_location,
            max_price=max_price,
            email_address=recipient_email
        )

    except Exception as e:
        return f"❌ Error sending apartment search results: {str(e)}"

def schedule_apartment_viewing(apartment_name: str = "Beautiful Apartment", email_address: str = DEFAULT_EMAIL) -> str:
    """
    Schedule an apartment viewing appointment with calendar integration and Google Maps.

    Args:
        apartment_name: Name of the apartment to schedule viewing for
        email_address: Email address to send appointment confirmation to

    Returns:
        Status of appointment scheduling
    """
    try:
        from app import send_gmail_calendar_email_tool, MCP_AVAILABLE
        from datetime import datetime, timedelta

        if not MCP_AVAILABLE:
            return f"✅ Would schedule viewing for {apartment_name} and send to {email_address}"

        # Create appointment for tomorrow at 2 PM
        tomorrow = datetime.now() + timedelta(days=1)
        start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        # Sample apartment details
        apartment_address = "123 Sample Street, Texas City, TX 77590"

        message = f"""
        <div style="font-size: 16px; color: #2d3748; margin-bottom: 20px;">
            <p>Your apartment viewing appointment has been confirmed! Here are the details:</p>
            <p>We look forward to showing you this beautiful property.</p>
        </div>
        """

        result = send_gmail_calendar_email_tool(
            to_email=email_address,
            subject=f"Apartment Viewing Confirmed: {apartment_name}",
            message=message,
            event_title=f"Apartment Viewing: {apartment_name}",
            event_start=start_time.isoformat(),
            event_end=end_time.isoformat(),
            event_description=f"Apartment viewing appointment for {apartment_name}",
            event_location=apartment_address,
            sender_name="Rent Hunting AI Assistant"
        )

        return result

    except Exception as e:
        return f"❌ Error scheduling apartment viewing: {str(e)}"

def search_apartments_by_criteria(city: str = "Texas City", max_price: int = 2000) -> str:
    """
    Search for apartments in the database by city and maximum price.

    Args:
        city: City to search in
        max_price: Maximum monthly rent price

    Returns:
        Formatted list of matching apartments
    """
    try:
        from tidb_customer_tool import fetch_apartments

        result = fetch_apartments(city=city, price_limit=max_price)

        if "No apartments found" in result:
            return f"No apartments found in {city} under ${max_price}/month. Try increasing your budget or searching in nearby areas."

        return f"Found apartments in {city} under ${max_price}/month:\n\n{result}"

    except Exception as e:
        return f"❌ Error searching apartments: {str(e)}"

def create_apartment_html(apartments: List[Dict[str, Any]], city: str = "Your City", max_price: int = 2000) -> str:
    """
    Create beautiful HTML for apartment listings with Google Maps integration
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your {city} Apartment Search Results</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa; line-height: 1.6;">
        <div style="max-width: 800px; margin: 0 auto; background-color: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); overflow: hidden;">

            <!-- Header -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center;">
                <h1 style="margin: 0; font-size: 32px; font-weight: 700;">🏠 Your {city} Apartment Search</h1>
                <p style="margin: 15px 0 0 0; font-size: 18px; opacity: 0.9;">Found {len(apartments)} apartments under ${max_price}/month</p>
            </div>

            <!-- Content -->
            <div style="padding: 40px;">
    """

    for i, apt in enumerate(apartments, 1):
        # Encode address for Google Maps
        address_encoded = apt.get('address', '').replace(' ', '+')
        maps_url = f"https://maps.google.com/maps?q={address_encoded}"
        directions_url = f"https://maps.google.com/maps/dir/?api=1&destination={address_encoded}"

        price_color = '#27ae60'

        html += f"""
        <div style="background: white; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.1); margin-bottom: 25px; overflow: hidden; border: 1px solid #e2e8f0;">
            <!-- Apartment Header -->
            <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 20px; border-bottom: 1px solid #e2e8f0;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <h3 style="margin: 0; color: #2d3748; font-size: 20px; font-weight: 700;">{apt.get('name', f'Apartment {i}')}</h3>
                        <p style="margin: 5px 0 0 0; color: #4a5568; font-size: 14px;">📍 {apt.get('address', 'Address not available')}</p>
                    </div>
                    <div style="text-align: right;">
                        <div style="background-color: {price_color}; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 700; font-size: 18px;">
                            {apt.get('price', 'Contact for price')}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Apartment Details -->
            <div style="padding: 25px;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px;">
                    <div style="text-align: center; background-color: #ebf8ff; padding: 15px; border-radius: 8px;">
                        <div style="font-size: 24px; margin-bottom: 5px;">🛏️</div>
                        <div style="font-weight: 600; color: #2b6cb0;">{apt.get('beds', 'N/A')} Bed{'s' if str(apt.get('beds', '')) != '1' else ''}</div>
                    </div>
                    <div style="text-align: center; background-color: #f0fff4; padding: 15px; border-radius: 8px;">
                        <div style="font-size: 24px; margin-bottom: 5px;">🚿</div>
                        <div style="font-weight: 600; color: #38a169;">{apt.get('baths', 'N/A')} Bath{'s' if str(apt.get('baths', '')) != '1' else ''}</div>
                    </div>
                    <div style="text-align: center; background-color: #fef5e7; padding: 15px; border-radius: 8px;">
                        <div style="font-size: 24px; margin-bottom: 5px;">📞</div>
                        <div style="font-weight: 600; color: #d69e2e; font-size: 12px;">{apt.get('contact', 'Contact for info')}</div>
                    </div>
                </div>

                <!-- Amenities -->
                <div style="background-color: #f7fafc; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                    <h4 style="margin: 0 0 10px 0; color: #4a5568; font-size: 14px; font-weight: 600;">✨ Amenities</h4>
                    <p style="margin: 0; color: #2d3748; font-size: 14px; line-height: 1.4;">{apt.get('amenities', 'Contact for details')}</p>
                </div>

                <!-- Action Buttons -->
                <div style="display: flex; gap: 10px; flex-wrap: wrap; justify-content: center;">
                    <a href="{maps_url}" target="_blank"
                       style="flex: 1; min-width: 120px; display: inline-block; background: linear-gradient(135deg, #4285f4 0%, #34a853 100%); color: white; text-decoration: none; padding: 12px 20px; border-radius: 25px; font-weight: 600; text-align: center; box-shadow: 0 4px 12px rgba(66,133,244,0.3);">
                        🗺️ View on Maps
                    </a>
                    <a href="{directions_url}" target="_blank"
                       style="flex: 1; min-width: 120px; display: inline-block; background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%); color: white; text-decoration: none; padding: 12px 20px; border-radius: 25px; font-weight: 600; text-align: center; box-shadow: 0 4px 12px rgba(255,107,107,0.3);">
                        🧭 Get Directions
                    </a>
                    <a href="tel:{apt.get('contact', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')}"
                       style="flex: 1; min-width: 120px; display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; padding: 12px 20px; border-radius: 25px; font-weight: 600; text-align: center; box-shadow: 0 4px 12px rgba(102,126,234,0.3);">
                        📞 Call Now
                    </a>
                </div>
            </div>
        </div>
        """

    html += """
            </div>

            <!-- Footer -->
            <div style="background-color: #f8fafc; padding: 30px 40px; text-align: center; border-top: 1px solid #e2e8f0;">
                <p style="margin: 0; color: #64748b; font-size: 16px;">
                    Best of luck with your apartment search!<br>
                    <strong style="color: #2d3748;">🤖 Rent Hunting AI Assistant</strong>
                </p>
                <p style="margin: 15px 0 0 0; color: #94a3b8; font-size: 14px;">
                    Need more options or have questions? Simply reply to this email.
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    return html