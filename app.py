import sys
import os
from typing import List, Optional
from datetime import datetime, timedelta

import yaml

# For agent
from agno.agent import Agent
from agno.team.team import Team
from agno.tools import tool
from agno.db.sqlite import SqliteDb

# For environment variables
from dotenv import load_dotenv
load_dotenv() # Load environment variables

# Import calendar utilities
from calendar_utils import generate_all_calendar_links, format_calendar_links_html

# Default email configuration from environment
DEFAULT_EMAIL = os.getenv("DEFAULT_EMAIL")

# Load email template from external file
def load_email_template(template_name: str) -> str:
    """
    Load an email template from the email_templates directory.
    
    Args:
        template_name (str): Name of the template file (without .html extension)
    
    Returns:
        str: Template content
    """
    template_path = os.path.join("email_templates", f"{template_name}.html")
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"⚠️ Template file not found: {template_path}")
        # Fallback to a simple template
        return """
        <html>
        <body>
        <h2>Apartment Viewing Appointment</h2>
        <p><strong>Apartment:</strong> {name_of_apartment}</p>
        <p><strong>When:</strong> {appointment_time}</p>
        <p><strong>Where:</strong> {address_of_apartment}</p>
        <p><strong>Price:</strong> {price_of_apartment}</p>
        <p>{calendar_link} | {maps_link}</p>
        <p>Best regards,<br>Rent Hunting AI Assistant</p>
        </body>
        </html>
        """
    except Exception as e:
        print(f"❌ Error loading template: {e}")
        return "Error loading email template"

# Default email template for apartment appointments
DEFAULT_APARTMENT_EMAIL_TEMPLATE = load_email_template("apartment_appointment")

# For model configuration
from models import load_model_instance

# For custom tools
from city_data_extractor import extract_city_data
from tidb_customer_tool import fetch_apartments

# Get current date and time for instructions
from datetime import datetime
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Load city data
with open("data/country_and_city_urls.yaml", "r", encoding="utf-8") as file:
    country_and_city_urls = yaml.safe_load(file)

# Store agent sessions in a SQLite database
# Delete the existing database file if it exists
if os.path.exists("tmp/agent.db"):
    os.remove("tmp/agent.db")

# Try to load model instance
try:
    model_instance = load_model_instance("gemini")
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    sys.exit(1)

# Try to import and setup MCP servers
MCP_AVAILABLE = False
try:
    from email_server import EmailMCPServer
    from mcp_tools import MCPRegistry, MCPClient
    
    # Setup MCP servers
    email_server = EmailMCPServer()
    registry = MCPRegistry()
    registry.register_server(email_server)
    mcp_client = MCPClient(registry)
    
    MCP_AVAILABLE = True
    print("✅ MCP servers initialized successfully")
    
except Exception as e:
    print(f"⚠️ MCP servers not available: {e}")
    print("Agent will run without email/calendar functionality")

# Helper function to format apartment appointment emails
def format_apartment_email(name_of_apartment: str, address_of_apartment: str, 
                          price_of_apartment: str, appointment_time: str = "10 AM tomorrow",
                          calendar_link: str = "Add to Calendar", maps_link: str = "View on Maps") -> str:
    """
    Format an apartment appointment email using the default template.
    
    Args:
        name_of_apartment (str): Name of the apartment/property
        address_of_apartment (str): Full address of the apartment
        price_of_apartment (str): Price information (e.g., "$3000/month")
        appointment_time (str): Appointment time (default: "10 AM tomorrow")
        calendar_link (str): Calendar link text or HTML
        maps_link (str): Maps link text or HTML
    
    Returns:
        str: Formatted email content
    """
    # Use string replacement to avoid format string issues
    template = DEFAULT_APARTMENT_EMAIL_TEMPLATE
    template = template.replace("{name_of_apartment}", name_of_apartment)
    template = template.replace("{appointment_time}", appointment_time)
    template = template.replace("{address_of_apartment}", address_of_apartment)
    template = template.replace("{price_of_apartment}", price_of_apartment)
    template = template.replace("{calendar_link}", calendar_link)
    template = template.replace("{maps_link}", maps_link)
    return template

def _parse_appointment_datetime(appointment_time: str, appointment_date: str, duration_minutes: int = 60) -> tuple:
    """
    Parse human-readable appointment time and date into ISO datetime strings.
    
    Args:
        appointment_time (str): Time like "10 AM", "2 PM", "14:30"
        appointment_date (str): Date like "tomorrow", "2025-09-15", "today"
        duration_minutes (int): Duration in minutes
    
    Returns:
        tuple: (start_datetime_iso, end_datetime_iso)
    """
    import re
    from datetime import datetime, timedelta
    
    try:
        # Parse the date
        base_date = datetime.now()
        if appointment_date.lower() in ["today"]:
            target_date = base_date.date()
        elif appointment_date.lower() in ["tomorrow"]:
            target_date = (base_date + timedelta(days=1)).date()
        else:
            # Try to parse as ISO date
            try:
                target_date = datetime.fromisoformat(appointment_date).date()
            except:
                # Default to tomorrow if parsing fails
                target_date = (base_date + timedelta(days=1)).date()
        
        # Parse the time
        time_str = appointment_time.strip().upper()
        
        # Handle formats like "10 AM", "2 PM", "10:30 AM"
        am_pm_match = re.match(r'(\d{1,2})(?::(\d{2}))?\s*(AM|PM)', time_str)
        if am_pm_match:
            hour = int(am_pm_match.group(1))
            minute = int(am_pm_match.group(2)) if am_pm_match.group(2) else 0
            is_pm = am_pm_match.group(3) == 'PM'
            
            if is_pm and hour != 12:
                hour += 12
            elif not is_pm and hour == 12:
                hour = 0
        else:
            # Handle 24-hour format like "14:30"
            time_match = re.match(r'(\d{1,2}):(\d{2})', time_str)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2))
            else:
                # Default to 10 AM if parsing fails
                hour, minute = 10, 0
        
        # Create start datetime
        start_dt = datetime.combine(target_date, datetime.min.time().replace(hour=hour, minute=minute))
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        
        # Convert to ISO format
        return start_dt.isoformat(), end_dt.isoformat()
        
    except Exception as e:
        # Fallback to reasonable defaults
        print(f"Warning: Could not parse appointment datetime: {e}")
        start_dt = datetime.now() + timedelta(days=1, hours=10-datetime.now().hour, minutes=-datetime.now().minute)
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        return start_dt.isoformat(), end_dt.isoformat()

def send_apartment_appointment_email(name_of_apartment: str, address_of_apartment: str,
                                   price_of_apartment: str, appointment_time: str = "10 AM tomorrow",
                                   appointment_date: str = "tomorrow", duration_minutes: int = 60,
                                   to_email: str = None) -> str:
    """
    Send an apartment appointment email using the default template with functional calendar links.
    
    Args:
        name_of_apartment (str): Name of the apartment/property
        address_of_apartment (str): Full address of the apartment
        price_of_apartment (str): Price information
        appointment_time (str): Appointment time (e.g., "10 AM tomorrow", "2 PM")
        appointment_date (str): Appointment date (e.g., "tomorrow", "2025-09-15")
        duration_minutes (int): Duration of appointment in minutes (default: 60)
        to_email (str): Recipient email (defaults to DEFAULT_EMAIL)
    
    Returns:
        str: Status of email sending
    """
    if to_email is None:
        to_email = DEFAULT_EMAIL
    
    # Create calendar and maps links
    maps_link = f'<a href="https://maps.google.com/maps?q={address_of_apartment.replace(" ", "+")}" target="_blank">View on Maps</a>'
    
    # Generate proper calendar functionality
    try:
        # Parse the appointment time to create proper datetime strings
        start_datetime, end_datetime = _parse_appointment_datetime(appointment_time, appointment_date, duration_minutes)
        
        # Generate calendar links for all services
        calendar_links = generate_all_calendar_links(
            title=f"Apartment Viewing: {name_of_apartment}",
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            description=f"Apartment viewing appointment for {name_of_apartment}\nPrice: {price_of_apartment}\nLocation: {address_of_apartment}",
            location=address_of_apartment,
            timezone="America/New_York"
        )
        
        # Create HTML calendar links
        calendar_link = format_calendar_links_html(calendar_links, f"Apartment Viewing: {name_of_apartment}")
    except Exception as e:
        # Fallback to simple text if calendar generation fails
        print(f"Warning: Could not generate calendar links: {e}")
        calendar_link = f'<a href="#" onclick="alert(\'Please manually add this appointment to your calendar: {appointment_time} at {address_of_apartment}\')">Add to Calendar</a>'
    
    email_content = format_apartment_email(
        name_of_apartment=name_of_apartment,
        address_of_apartment=address_of_apartment,
        price_of_apartment=price_of_apartment,
        appointment_time=appointment_time,
        calendar_link=calendar_link,
        maps_link=maps_link
    )
    
    subject = f"Apartment Viewing Appointment: {name_of_apartment}"
    
    if MCP_AVAILABLE:
        return send_email_tool(
            to_email=to_email,
            subject=subject,
            message=email_content,
            is_html=True
        )
    else:
        from app import send_email
        return send_email(subject=subject, body=email_content, to_address=to_email)

# Define custom tools that use MCP servers (only if available)
def send_email_tool(to_email: str = DEFAULT_EMAIL, subject: str = "", message: str = "", 
                   event_title: str = "", event_start: str = "", event_end: str = "",
                   event_description: str = "", event_location: str = "", 
                   event_timezone: str = "America/New_York", is_html: bool = False) -> str:
    """
    Send an email using the email MCP server with optional calendar event links.
    
    Args:
        to_email (str): Recipient's email address
        subject (str): Email subject
        message (str): Email message content
        event_title (str): Calendar event title (optional, if provided, adds calendar links)
        event_start (str): Event start time in ISO format (e.g., '2025-09-20T14:00:00')
        event_end (str): Event end time in ISO format (e.g., '2025-09-20T15:00:00')
        event_description (str): Event description (optional)
        event_location (str): Event location (optional)
        event_timezone (str): Event timezone (default: 'America/New_York')
        is_html (bool): Whether message is HTML formatted (default: False)
    
    Returns:
        str: Status of the email sending operation
    """
    if not MCP_AVAILABLE:
        return "❌ Email functionality not available - MCP server not initialized"
    
    try:
        # Prepare parameters
        email_params = {
            "to_email": to_email,
            "subject": subject,
            "message": message,
            "is_html": is_html
        }
        
        # Add calendar event parameters if provided
        if event_title and event_start and event_end:
            email_params.update({
                "event_title": event_title,
                "event_start": event_start,
                "event_end": event_end,
                "event_description": event_description,
                "event_location": event_location,
                "event_timezone": event_timezone
            })
        
        result = mcp_client.call("email-server", "send_email", **email_params)
        
        if result['status'] == 'success':
            calendar_note = " with calendar links" if event_title else ""
            return f"✅ Email{calendar_note} successfully sent to {result['to_email']}"
        else:
            return f"❌ Failed to send email: {result['error']}"
    except Exception as e:
        return f"❌ Error sending email: {str(e)}"

def create_calendar_event_tool(title: str, description: str, start_datetime: str, 
                              end_datetime: str, location: str = "", 
                              attendees_emails: str = "", timezone: str = "America/New_York") -> str:
    """
    Create a calendar event using the Google Calendar MCP server.
    
    Args:
        title (str): Event title
        description (str): Event description
        start_datetime (str): Start time in ISO format (e.g., "2025-09-20T14:00:00")
        end_datetime (str): End time in ISO format (e.g., "2025-09-20T15:00:00")
        location (str): Event location (optional)
        attendees_emails (str): Comma-separated list of attendee email addresses (optional)
        timezone (str): Timezone for the event (default: "America/New_York")
    
    Returns:
        str: Details of the created event
    """
    if not MCP_AVAILABLE:
        return "❌ Calendar functionality not available - MCP server not initialized"
    
    try:
        # Convert comma-separated string to list
        attendees = []
        if attendees_emails.strip():
            attendees = [email.strip() for email in attendees_emails.split(",")]
            
        result = mcp_client.call("google-calendar-server", "create_event",
                                title=title,
                                description=description,
                                start_datetime=start_datetime,
                                end_datetime=end_datetime,
                                location=location,
                                attendees=attendees,
                                timezone=timezone)
        
        return f"📅 Event created successfully!\nEvent ID: {result['event_id']}\nLink: {result['event_link']}"
    except Exception as e:
        return f"❌ Error creating calendar event: {str(e)}"

def send_email_with_calendar_event_tool(to_email: str = DEFAULT_EMAIL, subject: str = "", message: str = "",
                                       event_title: str = "", event_start: str = "", event_end: str = "",
                                       event_description: str = "", event_location: str = "",
                                       event_timezone: str = "America/New_York") -> str:
    """
    Send an email with calendar event "Add to Calendar" links.
    
    Args:
        to_email (str): Recipient's email address
        subject (str): Email subject
        message (str): Email message content
        event_title (str): Calendar event title
        event_start (str): Event start time in ISO format (e.g., '2025-09-20T14:00:00')
        event_end (str): Event end time in ISO format (e.g., '2025-09-20T15:00:00')
        event_description (str): Event description (optional)
        event_location (str): Event location (optional)
        event_timezone (str): Event timezone (default: 'America/New_York')
    
    Returns:
        str: Status of the email sending operation
    """
    return send_email_tool(
        to_email=to_email,
        subject=subject,
        message=message,
        event_title=event_title,
        event_start=event_start,
        event_end=event_end,
        event_description=event_description,
        event_location=event_location,
        event_timezone=event_timezone,
        is_html=True  # Use HTML for better calendar link formatting
    )

def send_gmail_calendar_email_tool(to_email: str = DEFAULT_EMAIL, subject: str = "", message: str = "",
                                  event_title: str = "", event_start: str = "", event_end: str = "",
                                  event_description: str = "", event_location: str = "",
                                  event_timezone: str = "America/New_York", sender_name: str = "") -> str:
    """
    Send a Gmail-optimized email with calendar event integration.
    This tool creates professional-looking emails that render perfectly in Gmail
    with prominent Google Calendar integration.
    
    Args:
        to_email (str): Recipient's email address
        subject (str): Email subject
        message (str): Email message content
        event_title (str): Calendar event title
        event_start (str): Event start time in ISO format (e.g., '2025-09-20T14:00:00')
        event_end (str): Event end time in ISO format (e.g., '2025-09-20T15:00:00')
        event_description (str): Event description (optional)
        event_location (str): Event location (optional)
        event_timezone (str): Event timezone (default: 'America/New_York')
        sender_name (str): Name of the sender (optional)
    
    Returns:
        str: Status of the email sending operation
    """
    if not MCP_AVAILABLE:
        return "❌ Email functionality not available - MCP server not initialized"
    
    try:
        result = mcp_client.call("email-server", "send_gmail_calendar_email",
                                to_email=to_email,
                                subject=subject,
                                message=message,
                                event_title=event_title,
                                event_start=event_start,
                                event_end=event_end,
                                event_description=event_description,
                                event_location=event_location,
                                event_timezone=event_timezone,
                                sender_name=sender_name,
                                use_simple_button=True)
        
        if result['status'] == 'success':
            return f"✅ Gmail-optimized email with Google Calendar integration sent to {result['to_email']}"
        else:
            return f"❌ Failed to send Gmail email: {result['error']}"
    except Exception as e:
        return f"❌ Error sending Gmail email: {str(e)}"

# Prepare tools based on MCP availability
email_tools = []
if MCP_AVAILABLE:
    email_tools = [send_email_tool, create_calendar_event_tool, send_email_with_calendar_event_tool, send_gmail_calendar_email_tool, send_apartment_appointment_email]
else:
    # Fallback simple email function
    def send_email(subject: str = "", body: str = "", to_address: str = DEFAULT_EMAIL) -> str:
        """
        Send an email.

        Args:
            subject (str): The subject of the email.
            body (str): The body of the email.
            to_address (str): The address to send the email to (defaults to value from .env).
        """
        return f"Sent email to {to_address} with subject {subject} and body {body}"
    
    email_tools = [send_email, send_apartment_appointment_email]

# Create the web agent
web_agent = Agent(
    name="Web Search Agent",
    model=model_instance,
    tools=[extract_city_data], 
    instructions=[
        "Search your knowledge before answering the question.",
        "When providing data, format it in a tabular format.",
        "Include sources in your response.",
        "Generate a brief and concise summary of the search results.",
        "Only include the report in your response. No other text.",
        f"Source: {country_and_city_urls}",
    ],
    markdown=True,
)

# Create the apartment agent
apartment_agent = Agent(
    name="Apartment Data Agent",
    role="Analyze and provide list of apartments that match user criteria",
    model=model_instance,
    tools=[fetch_apartments],
    instructions=[
        "Query apartment database for relevant property information",
        "Present data in clear, structured tables with key metrics",
        "Include location details, pricing, and property features",
    ],
    markdown=True,
)

email_agent = Agent(
    name="Email Agent",
    role="Send email notifications and manage calendar events",
    model=model_instance,
    tools=email_tools,
    instructions=[
        f"You are a helpful email and calendar assistant. Current date/time: {current_datetime}",
        f"Default email recipient (from .env): {DEFAULT_EMAIL}",
        "Compose and send email notifications based on user interactions",
        "Ensure all emails are sent to the correct recipients",
        "Include relevant information and context in each email",
        "If no email address is specified, use the default email address from environment variables",
        "You can send emails even when user doesn't explicitly provide an email address",
        "APARTMENT APPOINTMENTS: Use send_apartment_appointment_email for apartment viewing appointments - it uses a professional template with apartment details, timing, and helpful links."
    ] + (
        [
            "You can send emails to any recipient with a subject and message.",
            "You can create calendar events with title, description, date/time, location, and attendees.",
            "You can send emails WITH calendar event links that allow recipients to easily add events to their calendars.",
            "IMPORTANT: Since users primarily use Gmail, ALWAYS prefer send_gmail_calendar_email_tool for meeting invitations as it creates professional Gmail-optimized emails with prominent Google Calendar integration.",
            "The Gmail-optimized emails render perfectly in Gmail with beautiful formatting, event details, and a prominent 'Add to Google Calendar' button.",
            "For Gmail users, the send_gmail_calendar_email_tool provides the best experience with table-based HTML that works perfectly in Gmail's interface.",
            "When sending meeting invitations or event notifications, prioritize send_gmail_calendar_email_tool over other email tools.",
            "Calendar links support Google Calendar (primary), Outlook, Yahoo Calendar, and ICS files for other calendar apps.",
            "When scheduling events, always ask for essential details like title, date, time, and duration.",
            "For email sending, ensure you have the recipient, subject, and message content.",
            "Use proper date/time formats for calendar events (ISO format: YYYY-MM-DDTHH:MM:SS).",
            "For attendees, use comma-separated email addresses if multiple attendees are needed.",
            "Be helpful in suggesting appropriate email subjects and event titles if not provided.",
            "Always confirm the details before sending emails or creating events.",
            "Include sender name when using Gmail-optimized emails for a professional touch.",
        ] if MCP_AVAILABLE else [
            "Email and calendar functionality is currently not available, but I can help answer questions and provide assistance."
        ]
    ),
    markdown=True,
)

# Create the rent hunting team
rent_hunting_team = Team(
    name="Rent Hunting AI Team",
    model=model_instance,
    members=[apartment_agent, web_agent, email_agent],
    instructions=[
        "You are a collaborative team of AI agents specializing in apartment hunting and rental research.",
        "Work systematically to help users find the perfect rental property based on their criteria.",
        "WORKFLOW:",
        "1. Apartment Agent: Query database for properties matching user criteria (location, budget, bedrooms, etc.)",
        "2. Web Agent: Supplement with additional market research and neighborhood information",
        "3. Email Agent: Offer to send property summaries and schedule viewing appointments",
        "",
        "COLLABORATION GUIDELINES:",
        "- Share findings between agents to build comprehensive property profiles",
        "- Cross-reference data to ensure accuracy and completeness",
        "- Prioritize properties that best match user requirements",
        "- Include practical details: pricing, availability, contact information, and location benefits",
        "",
        "OUTPUT REQUIREMENTS:",
        "- Present findings in clear, structured format with key property details",
        "- Include address, rent, bedrooms, bathrooms, amenities, and contact information",
        "- Provide neighborhood insights and market context when available",
        "- Offer actionable next steps (viewing appointments, contact methods)",
        "",
        "EMAIL SERVICES:",
        "- Proactively offer to email property summaries to user's preferred address",
        "- Use send_apartment_appointment_email for scheduling property viewings",
        "- Send follow-up information and market updates when requested",
        "",
        "Always maintain a helpful, professional tone focused on finding the best rental solutions."
    ],
    markdown=True,
    show_members_responses=True,
    db=SqliteDb(db_file="tmp/agent.db"),
    add_history_to_context=True,
)

if __name__ == "__main__":

    print("="*80)
    print("🤖 Welcome to the Rent Hunting AI Team!")
    print("You can ask questions about apartment hunting, rental properties, and market research.")
    print("Type 'exit' or 'quit' to end the session.")

    while True:
        user_input = input("\n📝 Enter your apartment search query (or 'exit' to quit): ").strip()
        if user_input.lower() in ['exit', 'quit'] or user_input == '':
            print("👋 Exiting the Rent Hunting AI Team. Goodbye!")
            break
        
        rent_hunting_team.print_response(
            user_input,
            stream=True,
            show_full_reasoning=True,
            stream_intermediate_steps=True,
        )

