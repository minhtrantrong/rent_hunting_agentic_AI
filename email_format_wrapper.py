#!/usr/bin/env python3
"""
Email Format Wrapper - Ensures all emails are sent in beautiful HTML format
Prevents plain text emails from being sent accidentally
"""

from typing import List, Dict, Any, Optional
import os

def ensure_html_format(content: str) -> str:
    """
    Ensure content is in HTML format. If it's plain text, wrap it in basic HTML.

    Args:
        content: Email content (HTML or plain text)

    Returns:
        HTML-formatted content
    """
    # Check if content already contains HTML tags
    if '<html>' in content.lower() or '<body>' in content.lower() or '<div>' in content.lower():
        return content

    # If it's plain text, wrap in basic HTML with nice formatting
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rent Hunting AI</title>
    </head>
    <body style="margin: 0; padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); overflow: hidden;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center;">
                <h1 style="margin: 0; font-size: 24px; font-weight: 600;">🏠 Rent Hunting AI</h1>
            </div>
            <div style="padding: 30px;">
                <div style="color: #2d3748; font-size: 16px; line-height: 1.6;">
                    {content.replace(chr(10), '<br>').replace(chr(13), '')}
                </div>
            </div>
            <div style="background-color: #f8fafc; padding: 20px; text-align: center; border-top: 1px solid #e2e8f0;">
                <p style="margin: 0; color: #64748b; font-size: 14px;">
                    Best regards,<br>
                    <strong style="color: #2d3748;">🤖 Rent Hunting AI Assistant</strong>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def safe_send_email_tool(to_email: str = "", subject: str = "", message: str = "", **kwargs) -> str:
    """
    Wrapper for send_email_tool that ensures HTML formatting

    Args:
        to_email: Recipient email
        subject: Email subject
        message: Email content
        **kwargs: Additional parameters

    Returns:
        Email sending result
    """
    try:
        from app import send_email_tool, MCP_AVAILABLE

        if not MCP_AVAILABLE:
            return "❌ Email functionality not available - MCP server not initialized"

        # Ensure message is HTML formatted
        html_message = ensure_html_format(message)

        # Force HTML to True
        kwargs['is_html'] = True

        return send_email_tool(
            to_email=to_email,
            subject=subject,
            message=html_message,
            **kwargs
        )

    except Exception as e:
        return f"❌ Error sending email: {str(e)}"

def auto_format_apartment_email(apartments: List[Dict[str, Any]] = None, to_email: str = "") -> str:
    """
    Automatically format and send apartment listings in beautiful HTML

    Args:
        apartments: List of apartment data
        to_email: Recipient email

    Returns:
        Email sending result
    """
    try:
        from enhanced_email_utils import send_enhanced_apartment_listings_email

        # Handle None apartments list
        if apartments is None:
            apartments = []

        return send_enhanced_apartment_listings_email(
            apartments=apartments,
            to_email=to_email,
            search_criteria="your search criteria",
            recipient_name="there"
        )

    except Exception as e:
        # Fallback to manual HTML creation if enhanced utils fail
        html_content = create_basic_apartment_html(apartments)
        return safe_send_email_tool(
            to_email=to_email,
            subject="🏠 Your Apartment Search Results",
            message=html_content
        )

def create_basic_apartment_html(apartments: List[Dict[str, Any]]) -> str:
    """
    Create basic HTML for apartment listings as fallback

    Args:
        apartments: List of apartment data

    Returns:
        HTML content
    """
    html = """
    <div style="margin-bottom: 30px;">
        <h2 style="color: #2d3748; margin-bottom: 20px;">🏠 Your Apartment Search Results</h2>
        <p style="color: #4a5568; margin-bottom: 30px;">Found <strong>{count}</strong> apartments matching your criteria:</p>
    </div>
    """.format(count=len(apartments))

    for i, apt in enumerate(apartments, 1):
        address_encoded = apt.get('address', '').replace(' ', '+')
        maps_url = f"https://maps.google.com/maps?q={address_encoded}"

        html += f"""
        <div style="background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px; padding: 20px; border-left: 4px solid #667eea;">
            <h3 style="margin: 0 0 10px 0; color: #2d3748;">{apt.get('name', f'Apartment {i}')}</h3>
            <p style="margin: 5px 0; color: #4a5568;"><strong>📍 Address:</strong> {apt.get('address', 'N/A')}</p>
            <p style="margin: 5px 0; color: #059669; font-weight: bold; font-size: 18px;"><strong>💰 Price:</strong> {apt.get('price', 'Contact for price')}</p>
            <p style="margin: 5px 0; color: #4a5568;"><strong>🛏️ Beds/Baths:</strong> {apt.get('beds', 'N/A')} bed / {apt.get('baths', 'N/A')} bath</p>
            <p style="margin: 5px 0; color: #4a5568;"><strong>📞 Contact:</strong> {apt.get('contact', apt.get('phone', 'N/A'))}</p>
            <p style="margin: 10px 0;"><strong>✨ Amenities:</strong> {apt.get('amenities', 'Contact for details')}</p>
            <div style="margin-top: 15px;">
                <a href="{maps_url}" target="_blank" style="display: inline-block; background-color: #4285f4; color: white; text-decoration: none; padding: 8px 16px; border-radius: 20px; margin-right: 10px;">🗺️ View on Maps</a>
                <a href="tel:{apt.get('contact', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')}" style="display: inline-block; background-color: #667eea; color: white; text-decoration: none; padding: 8px 16px; border-radius: 20px;">📞 Call</a>
            </div>
        </div>
        """

    return html