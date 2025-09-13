
from email_server import EmailMCPServer
from mcp_tools import MCPRegistry, MCPClient

# For environment variables
from dotenv import load_dotenv
load_dotenv() # Load environment variables

# Setup
email_server = EmailMCPServer()
registry = MCPRegistry()
registry.register_server(email_server)
client = MCPClient(registry)

print("🧪 Testing Enhanced Email Server with Calendar Links")
print("=" * 60)

# Test 1: Send regular email (without calendar links)
print("\n📧 Test 1: Regular Email")
result = client.call("email-server", "send_email",
					to_email="recipient@example.com",
					subject="Test Email from MCP",
					message="Hello! This is a test email sent using EmailMCPServer.")

print(f"Status: {result['status']}")
if result['status'] == 'success':
	print(f"Email sent to: {result['to_email']}")
else:
	print(f"Error: {result['error']}")

# Test 2: Send email with calendar event links (Plain Text)
print("\n📅 Test 2: Email with Calendar Links (Plain Text)")
result_calendar_text = client.call("email-server", "send_email",
								  to_email="recipient@example.com",
								  subject="Meeting Invitation - Project Review",
								  message="Hi team,\n\nYou're invited to our project review meeting. Please add this event to your calendar using the links below.",
								  is_html=False,
								  event_title="Project Review Meeting",
								  event_start="2025-09-25T14:00:00",
								  event_end="2025-09-25T15:30:00",
								  event_description="Quarterly project review and planning session",
								  event_location="Conference Room A, Building 1",
								  event_timezone="America/New_York")

print(f"Status: {result_calendar_text['status']}")
if result_calendar_text['status'] == 'success':
	print(f"Email with calendar links (text) sent to: {result_calendar_text['to_email']}")
else:
	print(f"Error: {result_calendar_text['error']}")

# Test 3: Send email with calendar event links (HTML)
print("\n🎨 Test 3: Email with Calendar Links (HTML)")
result_calendar_html = client.call("email-server", "send_email",
								  to_email="recipient@example.com",
								  subject="Training Workshop - Advanced Python",
								  message="""<h2>Welcome to our Advanced Python Workshop!</h2>
								  <p>Dear participant,</p>
								  <p>We're excited to have you join our <strong>Advanced Python Workshop</strong>.</p>
								  <p>Workshop details:</p>
								  <ul>
								    <li>Duration: 2 hours</li>
								    <li>Format: Interactive hands-on session</li>
								    <li>Prerequisites: Basic Python knowledge</li>
								  </ul>
								  <p>Please add this event to your calendar and arrive 10 minutes early.</p>
								  <p>Best regards,<br>The Training Team</p>""",
								  is_html=True,
								  event_title="Advanced Python Workshop",
								  event_start="2025-09-28T10:00:00",
								  event_end="2025-09-28T12:00:00",
								  event_description="Hands-on workshop covering advanced Python concepts including decorators, context managers, and metaclasses",
								  event_location="Training Center - Room 101",
								  event_timezone="America/New_York")

print(f"Status: {result_calendar_html['status']}")
if result_calendar_html['status'] == 'success':
	print(f"Email with calendar links (HTML) sent to: {result_calendar_html['to_email']}")
else:
	print(f"Error: {result_calendar_html['error']}")

# Test 4: Demonstrate calendar link generation without sending email
print("\n🔗 Test 4: Calendar Link Generation Demo")
try:
	from calendar_utils import generate_all_calendar_links, format_calendar_links_html, format_calendar_links_text
	
	# Generate links for a sample event
	calendar_links = generate_all_calendar_links(
		title="Team Standup Meeting",
		start_datetime="2025-09-24T09:00:00",
		end_datetime="2025-09-24T09:30:00",
		description="Daily team standup meeting to discuss progress and blockers",
		location="Zoom Meeting Room",
		timezone="America/New_York"
	)
	
	print("Generated Calendar Links:")
	print(f"  🟦 Google Calendar: {calendar_links['google'][:80]}...")
	print(f"  🟦 Outlook: {calendar_links['outlook'][:80]}...")
	print(f"  🟦 Yahoo: {calendar_links['yahoo'][:80]}...")
	print(f"  📄 ICS Content: {len(calendar_links['ics_content'])} characters")
	
	# Show formatted HTML
	html_formatted = format_calendar_links_html(calendar_links, "Team Standup Meeting")
	print(f"\n📝 HTML Calendar Links ({len(html_formatted)} characters):")
	print("    [HTML content generated successfully]")
	
	# Show formatted text
	text_formatted = format_calendar_links_text(calendar_links, "Team Standup Meeting")
	print(f"\n📄 Text Calendar Links:")
	print(text_formatted[:200] + "..." if len(text_formatted) > 200 else text_formatted)
	
except Exception as e:
	print(f"Calendar link generation error: {e}")

print("\n✅ Email Server with Calendar Links Testing Complete!")
print("\n💡 Key Features Demonstrated:")
print("   • Regular email sending (without calendar links)")
print("   • Plain text emails with calendar links")
print("   • HTML emails with formatted calendar links")
print("   • Support for Google, Outlook, and Yahoo Calendar")
print("   • ICS file generation for other calendar apps")
print("   • Automatic calendar link formatting")
