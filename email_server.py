#!/usr/bin/env python3
"""
Email Server Example - MCP Tools Framework
Demonstrates how to create an email server using the MCP Tools framework.
"""

import sys
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, Any, List, Optional

# Add mcp_tools to path (for development)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_tools import MCPServer, MCPTool, MCPRegistry, MCPClient, setup_mcp_logging
from calendar_utils import (generate_all_calendar_links, format_calendar_links_html, 
                           format_calendar_links_text, create_gmail_optimized_email, 
                           format_gmail_calendar_button)

class EmailMCPServer(MCPServer):
    """MCP Server for email operations using SMTP"""
    
    def __init__(self, smtp_config: Optional[Dict[str, str]] = None):
        super().__init__("email-server", "1.0.0")
        
        # SMTP configuration
        self.smtp_config = smtp_config or {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": "587",
            "use_tls": "true",
            "username": "",  # Set via environment or parameters
            "password": ""   # Set via environment or parameters
        }
        
        # Try to get credentials from environment
        if not self.smtp_config["username"]:
            self.smtp_config["username"] = os.getenv("EMAIL_USERNAME", "")
        if not self.smtp_config["password"]:
            self.smtp_config["password"] = os.getenv("EMAIL_PASSWORD", "")
    
    def _define_capabilities(self):
        return [
            "email_send",
            "email_compose", 
            "template_processing",
            "attachment_support"
        ]
    
    def _initialize_tools(self):
        """Initialize email tools"""
        
        # Send simple email tool
        self.register_tool(MCPTool(
            name="send_email",
            description="Send a simple email message with optional calendar event links",
            input_schema={
                "type": "object",
                "properties": {
                    "to_email": {
                        "type": "string",
                        "description": "Recipient email address"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line"
                    },
                    "message": {
                        "type": "string",
                        "description": "Email message content"
                    },
                    "from_email": {
                        "type": "string",
                        "description": "Sender email (optional, uses configured default)"
                    },
                    "is_html": {
                        "type": "boolean",
                        "description": "Whether message is HTML formatted",
                        "default": False
                    },
                    "event_title": {
                        "type": "string",
                        "description": "Calendar event title (optional, if provided, adds calendar links)"
                    },
                    "event_start": {
                        "type": "string",
                        "description": "Event start time in ISO format (e.g., '2025-09-20T14:00:00')"
                    },
                    "event_end": {
                        "type": "string",
                        "description": "Event end time in ISO format (e.g., '2025-09-20T15:00:00')"
                    },
                    "event_description": {
                        "type": "string",
                        "description": "Event description (optional)"
                    },
                    "event_location": {
                        "type": "string",
                        "description": "Event location (optional)"
                    },
                    "event_timezone": {
                        "type": "string",
                        "description": "Event timezone (optional, defaults to 'America/New_York')"
                    }
                },
                "required": ["to_email", "subject", "message"]
            },
            handler=self._handle_send_email
        ))
        
        # Send bulk email tool
        self.register_tool(MCPTool(
            name="send_bulk_email",
            description="Send email to multiple recipients",
            input_schema={
                "type": "object",
                "properties": {
                    "recipients": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of recipient email addresses"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line"
                    },
                    "message": {
                        "type": "string",
                        "description": "Email message content"
                    },
                    "from_email": {
                        "type": "string",
                        "description": "Sender email (optional)"
                    },
                    "is_html": {
                        "type": "boolean",
                        "description": "Whether message is HTML formatted",
                        "default": False
                    }
                },
                "required": ["recipients", "subject", "message"]
            },
            handler=self._handle_send_bulk_email
        ))
        
        # Create email from template tool
        self.register_tool(MCPTool(
            name="send_template_email",
            description="Send email using a template with variable substitution",
            input_schema={
                "type": "object",
                "properties": {
                    "to_email": {
                        "type": "string",
                        "description": "Recipient email address"
                    },
                    "template_name": {
                        "type": "string",
                        "description": "Template name/type"
                    },
                    "template_variables": {
                        "type": "object",
                        "description": "Variables to substitute in template"
                    },
                    "from_email": {
                        "type": "string",
                        "description": "Sender email (optional)"
                    }
                },
                "required": ["to_email", "template_name", "template_variables"]
            },
            handler=self._handle_send_template_email
        ))
        
        # Test email configuration tool
        self.register_tool(MCPTool(
            name="test_email_config",
            description="Test email server configuration",
            input_schema={
                "type": "object",
                "properties": {
                    "test_recipient": {
                        "type": "string",
                        "description": "Email address to send test email to"
                    }
                },
                "required": ["test_recipient"]
            },
            handler=self._handle_test_email_config
        ))
        
        # Gmail-optimized email with calendar event tool
        self.register_tool(MCPTool(
            name="send_gmail_calendar_email",
            description="Send a Gmail-optimized email with calendar event integration",
            input_schema={
                "type": "object",
                "properties": {
                    "to_email": {
                        "type": "string",
                        "description": "Recipient email address"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line"
                    },
                    "message": {
                        "type": "string",
                        "description": "Main email message content"
                    },
                    "event_title": {
                        "type": "string",
                        "description": "Calendar event title"
                    },
                    "event_start": {
                        "type": "string",
                        "description": "Event start time in ISO format (e.g., '2025-09-20T14:00:00')"
                    },
                    "event_end": {
                        "type": "string",
                        "description": "Event end time in ISO format (e.g., '2025-09-20T15:00:00')"
                    },
                    "event_description": {
                        "type": "string",
                        "description": "Event description (optional)"
                    },
                    "event_location": {
                        "type": "string",
                        "description": "Event location (optional)"
                    },
                    "event_timezone": {
                        "type": "string",
                        "description": "Event timezone (optional, defaults to 'America/New_York')"
                    },
                    "sender_name": {
                        "type": "string",
                        "description": "Name of the sender (optional)"
                    },
                    "from_email": {
                        "type": "string",
                        "description": "Sender email (optional, uses configured default)"
                    },
                    "use_simple_button": {
                        "type": "boolean",
                        "description": "Use single Google Calendar button instead of all calendar options",
                        "default": True
                    }
                },
                "required": ["to_email", "subject", "message", "event_title", "event_start", "event_end"]
            },
            handler=self._handle_send_gmail_calendar_email
        ))
    
    def _handle_send_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle single email sending with optional calendar links"""
        try:
            # Extract parameters
            to_email = params["to_email"]
            subject = params["subject"]
            message = params["message"]
            from_email = params.get("from_email", self.smtp_config["username"])
            is_html = params.get("is_html", False)
            
            # Extract calendar event parameters
            event_title = params.get("event_title")
            event_start = params.get("event_start")
            event_end = params.get("event_end")
            event_description = params.get("event_description", "")
            event_location = params.get("event_location", "")
            event_timezone = params.get("event_timezone", "America/New_York")
            
            # Validate configuration
            if not self.smtp_config["username"] or not self.smtp_config["password"]:
                return {
                    "status": "error",
                    "error": "Email credentials not configured. Set EMAIL_USERNAME and EMAIL_PASSWORD environment variables."
                }
            
            # Generate calendar links if event details are provided
            calendar_content = ""
            if event_title and event_start and event_end:
                try:
                    calendar_links = generate_all_calendar_links(
                        title=event_title,
                        start_datetime=event_start,
                        end_datetime=event_end,
                        description=event_description,
                        location=event_location,
                        timezone=event_timezone
                    )
                    
                    if is_html:
                        calendar_content = format_calendar_links_html(calendar_links, event_title)
                    else:
                        calendar_content = format_calendar_links_text(calendar_links, event_title)
                        
                except Exception as e:
                    # If calendar link generation fails, continue without links
                    print(f"Warning: Could not generate calendar links: {e}")
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Combine message and calendar content
            full_message = message
            if calendar_content:
                if is_html:
                    # For HTML emails, add calendar content after the main message
                    full_message = f"""<html><body>
                    <div>{message}</div>
                    {calendar_content}
                    </body></html>"""
                else:
                    # For plain text emails, append calendar content
                    full_message = message + "\n\n" + calendar_content
            
            # Add message body
            if is_html:
                msg.attach(MIMEText(full_message, 'html'))
            else:
                msg.attach(MIMEText(full_message, 'plain'))
            
            # Send email
            result = self._send_message(msg, [to_email])
            
            return {
                "status": "success" if result["success"] else "error",
                "message": result["message"],
                "to_email": to_email,
                "subject": subject,
                "from_email": from_email
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "to_email": params.get("to_email", "unknown")
            }
    
    def _handle_send_bulk_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle bulk email sending"""
        try:
            recipients = params["recipients"]
            subject = params["subject"]
            message = params["message"]
            from_email = params.get("from_email", self.smtp_config["username"])
            is_html = params.get("is_html", False)
            
            if not self.smtp_config["username"] or not self.smtp_config["password"]:
                return {
                    "status": "error",
                    "error": "Email credentials not configured."
                }
            
            results = []
            successful_sends = 0
            
            for recipient in recipients:
                try:
                    # Create individual message for each recipient
                    msg = MIMEMultipart()
                    msg['From'] = from_email
                    msg['To'] = recipient
                    msg['Subject'] = subject
                    
                    if is_html:
                        msg.attach(MIMEText(message, 'html'))
                    else:
                        msg.attach(MIMEText(message, 'plain'))
                    
                    # Send to this recipient
                    result = self._send_message(msg, [recipient])
                    
                    results.append({
                        "recipient": recipient,
                        "status": "success" if result["success"] else "error",
                        "message": result["message"]
                    })
                    
                    if result["success"]:
                        successful_sends += 1
                        
                except Exception as e:
                    results.append({
                        "recipient": recipient,
                        "status": "error",
                        "message": str(e)
                    })
            
            return {
                "status": "completed",
                "total_recipients": len(recipients),
                "successful_sends": successful_sends,
                "failed_sends": len(recipients) - successful_sends,
                "results": results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _handle_send_template_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle template-based email sending"""
        try:
            to_email = params["to_email"]
            template_name = params["template_name"]
            template_variables = params["template_variables"]
            from_email = params.get("from_email", self.smtp_config["username"])
            
            # Get template
            template = self._get_email_template(template_name)
            if not template:
                return {
                    "status": "error",
                    "error": f"Template not found: {template_name}"
                }
            
            # Substitute variables
            try:
                subject = template["subject"].format(**template_variables)
                message = template["message"].format(**template_variables)
            except KeyError as e:
                return {
                    "status": "error",
                    "error": f"Missing template variable: {e}"
                }
            
            # Send email using the composed content
            email_params = {
                "to_email": to_email,
                "subject": subject,
                "message": message,
                "from_email": from_email,
                "is_html": template.get("is_html", False)
            }
            
            return self._handle_send_email(email_params)
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _handle_test_email_config(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Test email configuration"""
        try:
            test_recipient = params["test_recipient"]
            
            if not self.smtp_config["username"] or not self.smtp_config["password"]:
                return {
                    "status": "error",
                    "error": "Email credentials not configured"
                }
            
            # Send test email
            test_params = {
                "to_email": test_recipient,
                "subject": "MCP Tools Email Server Test",
                "message": f"""This is a test email from MCP Tools Email Server.

Configuration:
- SMTP Server: {self.smtp_config['smtp_server']}
- SMTP Port: {self.smtp_config['smtp_port']}
- From: {self.smtp_config['username']}
- TLS: {self.smtp_config['use_tls']}

If you received this email, your configuration is working correctly!

Sent at: {os.popen('date /t & time /t').read().strip()}""",
                "is_html": False
            }
            
            result = self._handle_send_email(test_params)
            
            return {
                "status": result["status"],
                "message": f"Test email sent to {test_recipient}",
                "config_test": "passed" if result["status"] == "success" else "failed",
                "details": result
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _handle_send_gmail_calendar_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Gmail-optimized email with calendar event"""
        try:
            # Extract parameters
            to_email = params["to_email"]
            subject = params["subject"]
            message = params["message"]
            event_title = params["event_title"]
            event_start = params["event_start"]
            event_end = params["event_end"]
            event_description = params.get("event_description", "")
            event_location = params.get("event_location", "")
            event_timezone = params.get("event_timezone", "America/New_York")
            sender_name = params.get("sender_name", "")
            from_email = params.get("from_email", self.smtp_config["username"])
            use_simple_button = params.get("use_simple_button", True)
            
            # Validate configuration
            if not self.smtp_config["username"] or not self.smtp_config["password"]:
                return {
                    "status": "error",
                    "error": "Email credentials not configured. Set EMAIL_USERNAME and EMAIL_PASSWORD environment variables."
                }
            
            # Create Gmail-optimized email content
            try:
                html_content = create_gmail_optimized_email(
                    subject=subject,
                    main_message=message,
                    event_title=event_title,
                    start_datetime=event_start,
                    end_datetime=event_end,
                    description=event_description,
                    location=event_location,
                    timezone=event_timezone,
                    sender_name=sender_name,
                    use_simple_button=use_simple_button
                )
            except Exception as e:
                return {
                    "status": "error",
                    "error": f"Failed to create Gmail-optimized email: {str(e)}"
                }
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add HTML content
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            result = self._send_message(msg, [to_email])
            
            return {
                "status": "success" if result["success"] else "error",
                "message": result["message"],
                "to_email": to_email,
                "subject": subject,
                "from_email": from_email,
                "event_title": event_title,
                "gmail_optimized": True
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "to_email": params.get("to_email", "unknown")
            }
    
    def _send_message(self, msg: MIMEMultipart, recipients: List[str]) -> Dict[str, Any]:
        """Send email message via SMTP"""
        try:
            # Create SMTP connection
            server = smtplib.SMTP(self.smtp_config["smtp_server"], int(self.smtp_config["smtp_port"]))
            
            if self.smtp_config["use_tls"].lower() == "true":
                # Enable TLS
                context = ssl.create_default_context()
                server.starttls(context=context)
            
            # Login
            server.login(self.smtp_config["username"], self.smtp_config["password"])
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.smtp_config["username"], recipients, text)
            server.quit()
            
            return {
                "success": True,
                "message": f"Email sent successfully to {', '.join(recipients)}"
            }
            
        except smtplib.SMTPAuthenticationError:
            return {
                "success": False,
                "message": "SMTP authentication failed. Check username/password."
            }
        except smtplib.SMTPConnectError:
            return {
                "success": False,
                "message": f"Could not connect to SMTP server {self.smtp_config['smtp_server']}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Email sending failed: {str(e)}"
            }
    
    def _get_email_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get email template by name"""
        templates = {
            "welcome": {
                "subject": "Welcome {name}!",
                "message": """Hello {name},

Welcome to our service! We're excited to have you on board.

Your account details:
- Email: {email}
- Registration Date: {date}

Best regards,
The Team""",
                "is_html": False
            },
            "notification": {
                "subject": "Notification: {title}",
                "message": """<html>
<body>
<h2>{title}</h2>
<p>{message}</p>
<p><strong>Details:</strong></p>
<ul>
{details}
</ul>
<p>Thank you!</p>
</body>
</html>""",
                "is_html": True
            },
            "reminder": {
                "subject": "Reminder: {event_name}",
                "message": """Hi {name},

This is a reminder about: {event_name}

Event Details:
- Date: {event_date}
- Time: {event_time}
- Location: {location}

Don't forget to attend!

Best regards""",
                "is_html": False
            }
        }
        
        return templates.get(template_name)

def demo_email_usage():
    """Demonstrate email server usage"""
    print("📧 MCP Tools - Email Server Demo")
    print("=" * 40)
    
    # Setup logging
    setup_mcp_logging("INFO")
    
    # Check for environment variables
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    
    if not username or not password:
        print("⚠️  Email credentials not found in environment variables.")
        print("   Set EMAIL_USERNAME and EMAIL_PASSWORD to test actual email sending.")
        print("   This demo will show the framework structure without sending real emails.\n")
    
    # Create email server with configuration
    print("🏗️ Setting up Email MCP Server...")
    email_server = EmailMCPServer({
        "smtp_server": "smtp.gmail.com",
        "smtp_port": "587", 
        "use_tls": "true",
        "username": username or "demo@example.com",
        "password": password or "demo_password"
    })
    
    # Create registry and client
    registry = MCPRegistry()
    registry.register_server(email_server)
    client = MCPClient(registry)
    
    # Show available tools
    print(f"\n🔧 Available Email Tools:")
    tools = client.list_available_tools()
    for tool in tools["email-server"]:
        print(f"   • {tool}")
    
    # Demo email operations (mock if no credentials)
    print(f"\n📨 Email Operations Demo:")
    
    try:
        # Test 1: Simple email
        print("\n1. Simple Email:")
        if username and password:
            result = client.call("email-server", "send_email",
                               to_email="test@example.com",
                               subject="Test from MCP Tools",
                               message="Hello! This is a test email from MCP Tools framework.")
            print(f"   Status: {result['status']}")
            if result['status'] == 'error':
                print(f"   Error: {result['error']}")
        else:
            print("   [MOCK] Would send: 'Test from MCP Tools' to test@example.com")
        
        # Test 2: Template email
        print("\n2. Template Email:")
        template_result = client.call("email-server", "send_template_email",
                                    to_email="user@example.com",
                                    template_name="welcome",
                                    template_variables={
                                        "name": "John Doe",
                                        "email": "user@example.com",
                                        "date": "2024-09-13"
                                    })
        if username and password:
            print(f"   Status: {template_result['status']}")
        else:
            print("   [MOCK] Would send welcome email to user@example.com")
        
        # Test 3: Bulk email
        print("\n3. Bulk Email:")
        bulk_result = client.call("email-server", "send_bulk_email",
                                recipients=["user1@example.com", "user2@example.com"],
                                subject="Newsletter Update",
                                message="This is our monthly newsletter!")
        if username and password:
            print(f"   Status: {bulk_result['status']}")
            print(f"   Recipients: {bulk_result['total_recipients']}")
        else:
            print("   [MOCK] Would send newsletter to 2 recipients")
        
        # Test 4: Configuration test
        print("\n4. Configuration Test:")
        if username and password:
            config_test = client.call("email-server", "test_email_config",
                                    test_recipient=username)  # Send to self
            print(f"   Config Status: {config_test['config_test']}")
        else:
            print("   [MOCK] Would test email configuration")
        
    except Exception as e:
        print(f"   Demo Error: {e}")
    
    print(f"\n✅ Email Server Demo Completed!")
    print(f"\n🎓 Key Features Demonstrated:")
    print(f"   • Simple email sending with SMTP")
    print(f"   • Template-based emails with variable substitution")
    print(f"   • Bulk email sending to multiple recipients")
    print(f"   • Configuration testing and validation")
    print(f"   • HTML and plain text email support")
    print(f"   • Comprehensive error handling")

def main():
    """Main demo function"""
    demo_email_usage()
    
    print(f"\n📋 Setup Instructions:")
    print(f"   1. Set environment variables:")
    print(f"      set EMAIL_USERNAME=your-email@gmail.com")
    print(f"      set EMAIL_PASSWORD=your-app-password")
    print(f"   2. For Gmail, use an App Password instead of your regular password")
    print(f"   3. Run this demo again to test actual email sending")
    print(f"\n💡 Integration Example:")
    print(f"   from examples.email_server_example import EmailMCPServer")
    print(f"   server = EmailMCPServer(your_smtp_config)")
    print(f"   # Use in any MCP Tools application!")

if __name__ == "__main__":
    main()