#!/usr/bin/env python3
"""
Calendar Utilities - Generate "Add to Calendar" Links
Provides functions to generate calendar links for various calendar services.
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from urllib.parse import quote_plus, urlencode
import re

def format_datetime_for_calendar(dt_str: str, timezone: str = "America/New_York") -> str:
    """
    Convert ISO datetime string to format suitable for calendar links.
    
    Args:
        dt_str: ISO datetime string (e.g., "2025-09-20T14:00:00")
        timezone: Timezone for the event
        
    Returns:
        Formatted datetime string for calendar URLs (YYYYMMDDTHHMMSSZ)
    """
    try:
        # Parse the datetime string
        dt = datetime.fromisoformat(dt_str)
        # Format for calendar links (UTC format)
        return dt.strftime("%Y%m%dT%H%M%SZ")
    except ValueError:
        # If parsing fails, try to create a reasonable default
        return datetime.now().strftime("%Y%m%dT%H%M%SZ")

def generate_google_calendar_link(
    title: str,
    start_datetime: str,
    end_datetime: str,
    description: str = "",
    location: str = "",
    timezone: str = "America/New_York",
    attendees: List[str] = None
) -> str:
    """
    Generate a Google Calendar 'Add to Calendar' link optimized for Gmail users.
    
    Args:
        title: Event title
        start_datetime: Start time in ISO format
        end_datetime: End time in ISO format  
        description: Event description
        location: Event location
        timezone: Event timezone
        attendees: List of attendee email addresses
        
    Returns:
        Google Calendar add event URL optimized for Gmail integration
    """
    base_url = "https://calendar.google.com/calendar/render"
    
    # Format dates
    start_formatted = format_datetime_for_calendar(start_datetime, timezone)
    end_formatted = format_datetime_for_calendar(end_datetime, timezone)
    
    # Enhanced description for Gmail users
    enhanced_description = description
    if description:
        enhanced_description += "\n\n(Added via email invitation)"
    
    # Create parameters optimized for Gmail
    params = {
        "action": "TEMPLATE",
        "text": title,
        "dates": f"{start_formatted}/{end_formatted}",
        "details": enhanced_description,
        "location": location,
        "sf": "true",
        "output": "xml",
        "ctz": timezone  # Include timezone for better Gmail integration
    }
    
    # Add attendees if provided (Gmail handles this well)
    if attendees:
        params["add"] = ",".join(attendees)
    
    # Remove empty parameters
    params = {k: v for k, v in params.items() if v}
    
    return f"{base_url}?{urlencode(params, quote_via=quote_plus)}"

def generate_outlook_calendar_link(
    title: str,
    start_datetime: str,
    end_datetime: str,
    description: str = "",
    location: str = "",
    timezone: str = "America/New_York"
) -> str:
    """
    Generate an Outlook Calendar 'Add to Calendar' link.
    
    Args:
        title: Event title
        start_datetime: Start time in ISO format
        end_datetime: End time in ISO format
        description: Event description
        location: Event location
        timezone: Event timezone
        
    Returns:
        Outlook Calendar add event URL
    """
    base_url = "https://outlook.live.com/calendar/0/deeplink/compose"
    
    # Format dates for Outlook (ISO format)
    start_formatted = start_datetime
    end_formatted = end_datetime
    
    # Create parameters
    params = {
        "subject": title,
        "startdt": start_formatted,
        "enddt": end_formatted,
        "body": description,
        "location": location
    }
    
    # Remove empty parameters
    params = {k: v for k, v in params.items() if v}
    
    return f"{base_url}?{urlencode(params, quote_via=quote_plus)}"

def generate_yahoo_calendar_link(
    title: str,
    start_datetime: str,
    end_datetime: str,
    description: str = "",
    location: str = "",
    timezone: str = "America/New_York"
) -> str:
    """
    Generate a Yahoo Calendar 'Add to Calendar' link.
    
    Args:
        title: Event title
        start_datetime: Start time in ISO format
        end_datetime: End time in ISO format
        description: Event description
        location: Event location
        timezone: Event timezone
        
    Returns:
        Yahoo Calendar add event URL
    """
    base_url = "https://calendar.yahoo.com/"
    
    # Format dates
    start_formatted = format_datetime_for_calendar(start_datetime, timezone)
    end_formatted = format_datetime_for_calendar(end_datetime, timezone)
    
    # Create parameters
    params = {
        "v": "60",
        "view": "d",
        "type": "20",
        "title": title,
        "st": start_formatted,
        "et": end_formatted,
        "desc": description,
        "in_loc": location
    }
    
    # Remove empty parameters
    params = {k: v for k, v in params.items() if v}
    
    return f"{base_url}?{urlencode(params, quote_via=quote_plus)}"

def generate_ics_content(
    title: str,
    start_datetime: str,
    end_datetime: str,
    description: str = "",
    location: str = "",
    timezone: str = "America/New_York"
) -> str:
    """
    Generate ICS (iCalendar) file content for calendar events.
    
    Args:
        title: Event title
        start_datetime: Start time in ISO format
        end_datetime: End time in ISO format
        description: Event description
        location: Event location
        timezone: Event timezone
        
    Returns:
        ICS file content as string
    """
    # Format dates
    start_formatted = format_datetime_for_calendar(start_datetime, timezone)
    end_formatted = format_datetime_for_calendar(end_datetime, timezone)
    
    # Generate unique ID
    import uuid
    uid = str(uuid.uuid4())
    
    # Create timestamp
    now = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Organization//Your App//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{uid}
DTSTART:{start_formatted}
DTEND:{end_formatted}
DTSTAMP:{now}
SUMMARY:{title}
DESCRIPTION:{description}
LOCATION:{location}
STATUS:CONFIRMED
SEQUENCE:0
END:VEVENT
END:VCALENDAR"""
    
    return ics_content

def generate_all_calendar_links(
    title: str,
    start_datetime: str,
    end_datetime: str,
    description: str = "",
    location: str = "",
    timezone: str = "America/New_York",
    attendees: List[str] = None
) -> Dict[str, str]:
    """
    Generate calendar links for all major calendar services, optimized for Gmail users.
    
    Args:
        title: Event title
        start_datetime: Start time in ISO format
        end_datetime: End time in ISO format
        description: Event description
        location: Event location
        timezone: Event timezone
        attendees: List of attendee email addresses
        
    Returns:
        Dictionary with calendar service names as keys and URLs as values
    """
    return {
        "google": generate_google_calendar_link(title, start_datetime, end_datetime, description, location, timezone, attendees),
        "outlook": generate_outlook_calendar_link(title, start_datetime, end_datetime, description, location, timezone),
        "yahoo": generate_yahoo_calendar_link(title, start_datetime, end_datetime, description, location, timezone),
        "ics_content": generate_ics_content(title, start_datetime, end_datetime, description, location, timezone)
    }

def create_gmail_optimized_email(
    subject: str,
    main_message: str,
    event_title: str,
    start_datetime: str,
    end_datetime: str,
    description: str = "",
    location: str = "",
    timezone: str = "America/New_York",
    attendees: List[str] = None,
    sender_name: str = "",
    use_simple_button: bool = False
) -> str:
    """
    Create a complete Gmail-optimized HTML email with calendar integration.
    
    Args:
        subject: Email subject (for reference, not included in body)
        main_message: Main email content
        event_title: Calendar event title
        start_datetime: Start time in ISO format
        end_datetime: End time in ISO format
        description: Event description
        location: Event location
        timezone: Event timezone
        attendees: List of attendee email addresses
        sender_name: Name of the sender
        use_simple_button: Use single Google Calendar button instead of all options
        
    Returns:
        Complete HTML email optimized for Gmail
    """
    # Generate calendar links
    calendar_links = generate_all_calendar_links(
        title=event_title,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        description=description,
        location=location,
        timezone=timezone,
        attendees=attendees
    )
    
    # Choose calendar button format
    if use_simple_button:
        calendar_html = format_gmail_calendar_button(calendar_links, event_title)
    else:
        calendar_html = format_calendar_links_html(calendar_links, event_title)
    
    # Format event details for display
    from datetime import datetime
    try:
        start_dt = datetime.fromisoformat(start_datetime)
        end_dt = datetime.fromisoformat(end_datetime)
        date_str = start_dt.strftime("%A, %B %d, %Y")
        time_str = f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}"
    except:
        date_str = "Date TBD"
        time_str = "Time TBD"
    
    # Create complete Gmail-optimized email
    html_email = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{subject}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #ffffff;">
        <table cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width: 600px; margin: 0 auto;">
            <tr>
                <td style="padding: 20px;">
                    <!-- Main Message -->
                    <div style="margin-bottom: 30px; color: #202124; font-size: 14px; line-height: 1.6;">
                        {main_message}
                    </div>
                    
                    <!-- Event Details -->
                    <table cellpadding="0" cellspacing="0" border="0" style="width: 100%; margin-bottom: 20px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e8eaed;">
                        <tr>
                            <td style="padding: 20px;">
                                <h2 style="margin: 0 0 15px 0; color: #1a73e8; font-size: 20px; font-weight: 500;">
                                    📅 {event_title}
                                </h2>
                                <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
                                    <tr>
                                        <td style="padding: 5px 0; color: #5f6368; font-size: 14px;">
                                            <strong>📅 Date:</strong> {date_str}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 5px 0; color: #5f6368; font-size: 14px;">
                                            <strong>🕐 Time:</strong> {time_str} ({timezone})
                                        </td>
                                    </tr>
                                    {f'<tr><td style="padding: 5px 0; color: #5f6368; font-size: 14px;"><strong>📍 Location:</strong> {location}</td></tr>' if location else ''}
                                    {f'<tr><td style="padding: 5px 0; color: #5f6368; font-size: 14px;"><strong>📝 Description:</strong> {description}</td></tr>' if description else ''}
                                </table>
                            </td>
                        </tr>
                    </table>
                    
                    <!-- Calendar Links -->
                    {calendar_html}
                    
                    {f'<p style="margin-top: 30px; color: #5f6368; font-size: 14px;">Best regards,<br><strong>{sender_name}</strong></p>' if sender_name else ''}
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    return html_email

def format_calendar_links_html(calendar_links: Dict[str, str], event_title: str = "Event") -> str:
    """
    Format calendar links as HTML optimized for Gmail display.
    
    Args:
        calendar_links: Dictionary of calendar links from generate_all_calendar_links
        event_title: Title of the event for display
        
    Returns:
        HTML formatted string with calendar links optimized for Gmail
    """
    html = f"""
    <table cellpadding="0" cellspacing="0" border="0" style="width: 100%; margin: 20px 0; font-family: Arial, sans-serif;">
        <tr>
            <td style="padding: 20px; background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px;">
                <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
                    <tr>
                        <td>
                            <h3 style="margin: 0 0 15px 0; color: #1a73e8; font-size: 18px; font-weight: 500;">
                                📅 Add "{event_title}" to Your Calendar
                            </h3>
                            <p style="margin: 0 0 20px 0; color: #5f6368; font-size: 14px; line-height: 1.4;">
                                Click below to add this event to your calendar:
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-bottom: 15px;">
                            <!-- Primary Google Calendar Button (Gmail optimized) -->
                            <table cellpadding="0" cellspacing="0" border="0" style="display: inline-block; margin-right: 10px; margin-bottom: 10px;">
                                <tr>
                                    <td style="background-color: #1a73e8; border-radius: 6px; padding: 12px 24px;">
                                        <a href="{calendar_links.get('google', '#')}" 
                                           style="color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 500; display: block;">
                                            📅 Add to Google Calendar
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            <!-- Alternative calendar options -->
                            <table cellpadding="0" cellspacing="0" border="0" style="display: inline-block; margin-right: 10px; margin-bottom: 10px;">
                                <tr>
                                    <td style="background-color: #0078d4; border-radius: 6px; padding: 8px 16px;">
                                        <a href="{calendar_links.get('outlook', '#')}" 
                                           style="color: #ffffff; text-decoration: none; font-size: 12px; display: block;">
                                            Outlook
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            <table cellpadding="0" cellspacing="0" border="0" style="display: inline-block; margin-bottom: 10px;">
                                <tr>
                                    <td style="background-color: #6001d2; border-radius: 6px; padding: 8px 16px;">
                                        <a href="{calendar_links.get('yahoo', '#')}" 
                                           style="color: #ffffff; text-decoration: none; font-size: 12px; display: block;">
                                            Yahoo
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p style="margin: 0; font-size: 12px; color: #80868b; line-height: 1.3;">
                                Can't access the links? 
                                <a href="data:text/calendar;charset=utf8,{quote_plus(calendar_links.get('ics_content', ''))}" 
                                   download="event.ics" 
                                   style="color: #1a73e8; text-decoration: none;">
                                    Download calendar file
                                </a>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
    """
    return html

def format_gmail_calendar_button(calendar_links: Dict[str, str], event_title: str = "Event") -> str:
    """
    Format a single prominent Google Calendar button optimized for Gmail.
    
    Args:
        calendar_links: Dictionary of calendar links from generate_all_calendar_links
        event_title: Title of the event for display
        
    Returns:
        HTML formatted string with a single Google Calendar button
    """
    html = f"""
    <table cellpadding="0" cellspacing="0" border="0" style="margin: 15px 0;">
        <tr>
            <td style="background-color: #1a73e8; border-radius: 8px; padding: 0;">
                <a href="{calendar_links.get('google', '#')}" 
                   style="display: block; padding: 14px 28px; color: #ffffff; text-decoration: none; font-size: 16px; font-weight: 500; font-family: Arial, sans-serif;">
                    📅 Add to Google Calendar
                </a>
            </td>
        </tr>
    </table>
    """
    return html

def format_calendar_links_text(calendar_links: Dict[str, str], event_title: str = "Event") -> str:
    """
    Format calendar links as plain text for email inclusion.
    
    Args:
        calendar_links: Dictionary of calendar links from generate_all_calendar_links
        event_title: Title of the event for display
        
    Returns:
        Plain text formatted string with calendar links
    """
    text = f"""
📅 ADD "{event_title.upper()}" TO YOUR CALENDAR

Add this event to your calendar by clicking one of these links:

🔗 Google Calendar: {calendar_links.get('google', 'Not available')}

🔗 Outlook Calendar: {calendar_links.get('outlook', 'Not available')}

🔗 Yahoo Calendar: {calendar_links.get('yahoo', 'Not available')}

💾 For other calendar apps, you can create an ICS file with the event details.

"""
    return text