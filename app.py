import sys
import os
from typing import List, Optional

# Adjust the path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

# For agent
from agno.agent import Agent
from agno.db.sqlite import SqliteDb

# For environment variables
from dotenv import load_dotenv
load_dotenv() # Load environment variables

# For model configuration
from models import load_model_instance

# Get current date and time for instructions
from datetime import datetime
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

# Define custom tools that use MCP servers (only if available)
def send_email_tool(to_email: str, subject: str, message: str, 
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

def send_email_with_calendar_event_tool(to_email: str, subject: str, message: str,
                                       event_title: str, event_start: str, event_end: str,
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

def send_gmail_calendar_email_tool(to_email: str, subject: str, message: str,
                                  event_title: str, event_start: str, event_end: str,
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
tools = []
if MCP_AVAILABLE:
    tools = [send_email_tool, create_calendar_event_tool, send_email_with_calendar_event_tool, send_gmail_calendar_email_tool]

# Create instructions
instructions = [
    f"You are a helpful assistant. Current date/time: {current_datetime}",
]

if MCP_AVAILABLE:
    instructions.extend([
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
    ])
else:
    instructions.append("Email and calendar functionality is currently not available, but I can help answer questions and provide assistance.")

# Create agent with error handling
try:
    agent = Agent(
        name="EmailCalendarAgent" if MCP_AVAILABLE else "Assistant",
        model=model_instance,
        tools=tools,
        instructions=instructions,
        db=SqliteDb(db_file="tmp/agent.db"),
        add_history_to_context=True,
    )
    print("✅ Agent created successfully")
except Exception as e:
    print(f"❌ Error creating agent: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("\n🤖 Agent Ready!")
    if MCP_AVAILABLE:
        print("I can help you:")
        print("+ Send emails")
        print("+ Schedule calendar events")
        print("+ Manage your communications and appointments")
        print("+ Answer general questions")
    else:
        print("I can help answer questions and provide assistance.")
        print("(Email and calendar features are currently unavailable)")
    
    print("\nType 'exit' to quit\n")

    # Interactive loop
    while True:
        try:
            user_input = input("User: ").strip()

            if user_input.lower() in ["exit", "quit", ""]:
                print("Goodbye! 👋")
                break

            agent.print_response(user_input)
            print("\n" + "-"*30 + "\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")