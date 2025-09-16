#!/usr/bin/env python3
"""
Enhanced Email Utilities - Rent Hunting AI
Beautiful HTML email formatting with Google Maps integration
"""

import os
import urllib.parse
from typing import List, Dict, Any, Optional

def create_apartment_card_html(apartment: Dict[str, Any]) -> str:
    """
    Create a beautiful apartment card with Google Maps integration

    Args:
        apartment: Dictionary containing apartment details

    Returns:
        HTML string for apartment card
    """
    # Encode address for Google Maps URL
    address_encoded = urllib.parse.quote_plus(apartment.get('address', ''))

    # Create Google Maps link
    maps_url = f"https://maps.google.com/maps?q={address_encoded}"

    # Create directions link
    directions_url = f"https://maps.google.com/maps/dir/?api=1&destination={address_encoded}"

    # Format price with color coding
    price = apartment.get('price', 'Contact for price')
    price_color = '#27ae60' if price.replace('$', '').replace(',', '').replace('/month', '').isdigit() else '#e74c3c'

    # Format beds/baths
    beds = apartment.get('beds', apartment.get('bed_info', 'N/A'))
    baths = apartment.get('baths', 'N/A')

    # Format contact info
    contact = apartment.get('contact', apartment.get('phone', 'Contact for info'))

    # Format amenities
    amenities = apartment.get('amenities', 'Contact for details')
    if isinstance(amenities, list):
        amenities = ', '.join(amenities)

    card_html = f"""
    <div style="background: white; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.1); margin-bottom: 25px; overflow: hidden; border: 1px solid #e2e8f0; transition: transform 0.2s;">
        <!-- Apartment Header -->
        <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 20px; border-bottom: 1px solid #e2e8f0;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <h3 style="margin: 0; color: #2d3748; font-size: 20px; font-weight: 700;">{apartment.get('name', 'Apartment')}</h3>
                    <p style="margin: 5px 0 0 0; color: #4a5568; font-size: 14px;">📍 {apartment.get('address', 'Address not available')}</p>
                </div>
                <div style="text-align: right;">
                    <div style="background-color: {price_color}; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 700; font-size: 18px;">
                        {price}
                    </div>
                </div>
            </div>
        </div>

        <!-- Apartment Details -->
        <div style="padding: 25px;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px;">
                <div style="text-align: center; background-color: #ebf8ff; padding: 15px; border-radius: 8px;">
                    <div style="font-size: 24px; margin-bottom: 5px;">🛏️</div>
                    <div style="font-weight: 600; color: #2b6cb0;">{beds} Bed{'' if str(beds) == '1' else 's'}</div>
                </div>
                <div style="text-align: center; background-color: #f0fff4; padding: 15px; border-radius: 8px;">
                    <div style="font-size: 24px; margin-bottom: 5px;">🚿</div>
                    <div style="font-weight: 600; color: #38a169;">{baths} Bath{'' if str(baths) == '1' else 's'}</div>
                </div>
                <div style="text-align: center; background-color: #fef5e7; padding: 15px; border-radius: 8px;">
                    <div style="font-size: 24px; margin-bottom: 5px;">📞</div>
                    <div style="font-weight: 600; color: #d69e2e; font-size: 12px;">{contact}</div>
                </div>
            </div>

            <!-- Amenities -->
            <div style="background-color: #f7fafc; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h4 style="margin: 0 0 10px 0; color: #4a5568; font-size: 14px; font-weight: 600;">✨ Amenities</h4>
                <p style="margin: 0; color: #2d3748; font-size: 14px; line-height: 1.4;">{amenities}</p>
            </div>

            <!-- Action Buttons -->
            <div style="display: flex; gap: 10px; flex-wrap: wrap; justify-content: center;">
                <a href="{maps_url}" target="_blank"
                   style="flex: 1; min-width: 120px; display: inline-block; background: linear-gradient(135deg, #4285f4 0%, #34a853 100%); color: white; text-decoration: none; padding: 12px 20px; border-radius: 25px; font-weight: 600; text-align: center; box-shadow: 0 4px 12px rgba(66,133,244,0.3); transition: transform 0.2s;">
                    🗺️ View on Maps
                </a>
                <a href="{directions_url}" target="_blank"
                   style="flex: 1; min-width: 120px; display: inline-block; background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%); color: white; text-decoration: none; padding: 12px 20px; border-radius: 25px; font-weight: 600; text-align: center; box-shadow: 0 4px 12px rgba(255,107,107,0.3); transition: transform 0.2s;">
                    🧭 Get Directions
                </a>
                <a href="tel:{contact.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')}"
                   style="flex: 1; min-width: 120px; display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; padding: 12px 20px; border-radius: 25px; font-weight: 600; text-align: center; box-shadow: 0 4px 12px rgba(102,126,234,0.3); transition: transform 0.2s;">
                    📞 Call Now
                </a>
            </div>
        </div>
    </div>
    """

    return card_html

def create_enhanced_apartment_listings_email(apartments: List[Dict[str, Any]],
                                           search_criteria: str = "your search criteria",
                                           recipient_name: str = "there") -> str:
    """
    Create a beautifully formatted HTML email with apartment listings and Google Maps integration

    Args:
        apartments: List of apartment dictionaries
        search_criteria: Description of search criteria
        recipient_name: Name of the recipient

    Returns:
        Complete HTML email string
    """
    total_count = len(apartments)

    # Create apartment cards HTML
    apartments_html = ""
    for apartment in apartments:
        apartments_html += create_apartment_card_html(apartment)

    # Load template
    template_path = os.path.join("email_templates", "apartment_listings.html")
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template = file.read()
    except FileNotFoundError:
        # Fallback template if file not found
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Apartment Search Results</title>
        </head>
        <body style="font-family: Arial, sans-serif; margin: 20px; background-color: #f5f7fa;">
            <div style="max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px;">
                <h1 style="color: #2d3748;">🏠 Your Apartment Search Results</h1>
                <p>Hi {recipient_name}! Found <strong>{total_count} apartments</strong> matching {search_criteria}</p>
                {apartments_html}
                <p>Best regards,<br><strong>🤖 Rent Hunting AI Assistant</strong></p>
            </div>
        </body>
        </html>
        """

    # Replace template variables
    html_email = template.replace("{search_summary}", f"Hi {recipient_name}! Found great options matching {search_criteria}")
    html_email = html_email.replace("{total_count}", str(total_count))
    html_email = html_email.replace("{apartments_html}", apartments_html)

    return html_email

def create_enhanced_apartment_appointment_email(name_of_apartment: str,
                                              address_of_apartment: str,
                                              price_of_apartment: str,
                                              appointment_time: str = "10 AM tomorrow",
                                              calendar_link: str = "") -> str:
    """
    Create enhanced apartment appointment email with Google Maps integration

    Args:
        name_of_apartment: Name of the apartment
        address_of_apartment: Full address
        price_of_apartment: Price information
        appointment_time: Appointment time
        calendar_link: Calendar link HTML

    Returns:
        Enhanced HTML email string
    """
    # Encode address for Google Maps
    address_encoded = urllib.parse.quote_plus(address_of_apartment)

    # Load and process template
    template_path = os.path.join("email_templates", "apartment_appointment.html")
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template = file.read()
    except FileNotFoundError:
        # Fallback template
        template = """
        <html>
        <body style="font-family: Arial, sans-serif; margin: 20px;">
            <h1>🏠 Apartment Viewing Appointment</h1>
            <p><strong>Apartment:</strong> {name_of_apartment}</p>
            <p><strong>When:</strong> {appointment_time}</p>
            <p><strong>Where:</strong> {address_of_apartment}</p>
            <p><strong>Price:</strong> {price_of_apartment}</p>
            <div>{calendar_link}</div>
            <p><a href="https://maps.google.com/maps?q={address_of_apartment_encoded}" target="_blank">🗺️ View on Google Maps</a></p>
            <p>Best regards,<br><strong>🤖 Rent Hunting AI Assistant</strong></p>
        </body>
        </html>
        """

    # Replace template variables
    html_email = template.replace("{name_of_apartment}", name_of_apartment)
    html_email = html_email.replace("{address_of_apartment}", address_of_apartment)
    html_email = html_email.replace("{address_of_apartment_encoded}", address_encoded)
    html_email = html_email.replace("{price_of_apartment}", price_of_apartment)
    html_email = html_email.replace("{appointment_time}", appointment_time)
    html_email = html_email.replace("{calendar_link}", calendar_link)

    return html_email

def send_enhanced_apartment_listings_email(apartments: List[Dict[str, Any]] = None,
                                         to_email: str = "",
                                         search_criteria: str = "your search criteria",
                                         recipient_name: str = "there") -> str:
    """
    Send enhanced apartment listings email using MCP email server

    Args:
        apartments: List of apartment dictionaries
        to_email: Recipient email address
        search_criteria: Description of search criteria
        recipient_name: Name of recipient

    Returns:
        Status of email sending
    """
    try:
        # Import here to avoid circular imports
        from app import send_email_tool, MCP_AVAILABLE

        if not MCP_AVAILABLE:
            return "❌ Email functionality not available - MCP server not initialized"

        # Handle None apartments list
        if apartments is None:
            apartments = []

        # Create enhanced email content
        email_html = create_enhanced_apartment_listings_email(
            apartments=apartments,
            search_criteria=search_criteria,
            recipient_name=recipient_name
        )

        # Create subject
        subject = f"🏠 Your Apartment Search Results - {len(apartments)} Options Found"

        # Send email
        result = send_email_tool(
            to_email=to_email,
            subject=subject,
            message=email_html,
            is_html=True
        )

        return result

    except Exception as e:
        return f"❌ Error sending enhanced email: {str(e)}"

def send_enhanced_apartment_appointment_email(name_of_apartment: str = "",
                                            address_of_apartment: str = "",
                                            price_of_apartment: str = "",
                                            appointment_time: str = "10 AM tomorrow",
                                            appointment_date: str = "tomorrow",
                                            duration_minutes: int = 60,
                                            to_email: str = "") -> str:
    """
    Send enhanced apartment appointment email with Google Maps and calendar integration

    Args:
        name_of_apartment: Name of the apartment
        address_of_apartment: Full address
        price_of_apartment: Price information
        appointment_time: Appointment time
        appointment_date: Appointment date
        duration_minutes: Duration in minutes
        to_email: Recipient email

    Returns:
        Status of email sending
    """
    try:
        from app import (send_gmail_calendar_email_tool, _parse_appointment_datetime,
                        DEFAULT_EMAIL, MCP_AVAILABLE)

        if not MCP_AVAILABLE:
            return "❌ Email functionality not available - MCP server not initialized"

        if not to_email:
            to_email = DEFAULT_EMAIL

        # Parse appointment datetime
        start_datetime, end_datetime = _parse_appointment_datetime(
            appointment_time, appointment_date, duration_minutes
        )

        # Create main message
        message = f"""
        <div style="font-size: 16px; color: #2d3748; margin-bottom: 20px;">
            <p>Your apartment viewing appointment has been scheduled! Here are the details:</p>
        </div>
        """

        # Send Gmail-optimized email with calendar integration
        result = send_gmail_calendar_email_tool(
            to_email=to_email,
            subject=f"Apartment Viewing: {name_of_apartment}",
            message=message,
            event_title=f"Apartment Viewing: {name_of_apartment}",
            event_start=start_datetime,
            event_end=end_datetime,
            event_description=f"Apartment viewing appointment for {name_of_apartment}\nPrice: {price_of_apartment}\nAddress: {address_of_apartment}",
            event_location=address_of_apartment,
            sender_name="Rent Hunting AI Assistant"
        )

        return result

    except Exception as e:
        return f"❌ Error sending enhanced appointment email: {str(e)}"