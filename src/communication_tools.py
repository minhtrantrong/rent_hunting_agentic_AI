"""
Communication tools for Agent #3 - Email and SMS integration
"""

from typing import List, Dict, Optional
from agno.tools import Toolkit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import os
import re


class CommunicationTools(Toolkit):
    def __init__(
        self,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 587,
        email_address: str = None,
        email_password: str = None,
        twilio_account_sid: str = None,
        twilio_auth_token: str = None,
        twilio_phone_number: str = None
    ):
        super().__init__(name="communication_tools")
        
        # Email configuration
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_address = email_address or os.getenv("EMAIL_ADDRESS")
        self.email_password = email_password or os.getenv("EMAIL_PASSWORD")
        
        # Twilio configuration
        self.twilio_account_sid = twilio_account_sid or os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = twilio_auth_token or os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = twilio_phone_number or os.getenv("TWILIO_PHONE_NUMBER")
        
        # Initialize Twilio client
        if self.twilio_account_sid and self.twilio_auth_token:
            self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
        
        # Register tools
        self.register(self.send_email)
        self.register(self.send_sms)
        self.register(self.contact_property_agent)
        self.register(self.send_viewing_confirmation)
        self.register(self.send_viewing_reminder)
        self.register(self.handle_agent_response)

    def send_email(
        self,
        to_email: str,
        subject: str,
        message: str,
        is_html: bool = False
    ) -> Dict:
        """
        Send email to recipient
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            message: Email content
            is_html: Whether message contains HTML
            
        Returns:
            Result of email sending attempt
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'html' if is_html else 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            return {
                'status': 'sent',
                'recipient': to_email,
                'subject': subject,
                'message': 'Email sent successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'recipient': to_email,
                'error': str(e),
                'message': 'Failed to send email'
            }

    def send_sms(
        self,
        to_phone: str,
        message: str
    ) -> Dict:
        """
        Send SMS message
        
        Args:
            to_phone: Recipient phone number (E.164 format)
            message: SMS content
            
        Returns:
            Result of SMS sending attempt
        """
        if not self.twilio_client:
            return {
                'status': 'error',
                'message': 'Twilio not configured'
            }
        
        try:
            # Ensure phone number is in correct format
            if not to_phone.startswith('+'):
                to_phone = '+1' + re.sub(r'\D', '', to_phone)
            
            message_obj = self.twilio_client.messages.create(
                body=message,
                from_=self.twilio_phone_number,
                to=to_phone
            )
            
            return {
                'status': 'sent',
                'recipient': to_phone,
                'message_sid': message_obj.sid,
                'message': 'SMS sent successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'recipient': to_phone,
                'error': str(e),
                'message': 'Failed to send SMS'
            }

    def contact_property_agent(
        self,
        property_data: Dict,
        user_data: Dict,
        viewing_time: Dict,
        contact_method: str = "email"
    ) -> Dict:
        """
        Contact property agent to schedule viewing
        
        Args:
            property_data: Property information
            user_data: User contact information
            viewing_time: Proposed viewing time
            contact_method: "email" or "sms"
            
        Returns:
            Result of contacting agent
        """
        agent_contact = property_data.get('agent_contact', {})
        agent_name = property_data.get('agent_name', 'Property Manager')
        property_address = property_data.get('address', 'Property')
        
        # Generate professional message
        if contact_method == "email":
            subject = f"Property Viewing Request - {property_address}"
            
            message = f"""
Dear {agent_name},

I hope this email finds you well. I am writing on behalf of my client who is interested in scheduling a viewing for the property located at:

{property_address}

Property Details:
- Listing ID: {property_data.get('id', 'N/A')}
- Price: {property_data.get('price', 'N/A')}
- Bedrooms: {property_data.get('bedrooms', 'N/A')}
- Bathrooms: {property_data.get('bathrooms', 'N/A')}

Proposed Viewing Time:
- Date: {viewing_time.get('start', '').split('T')[0]}
- Time: {viewing_time.get('start', '').split('T')[1].split('.')[0]} - {viewing_time.get('end', '').split('T')[1].split('.')[0]}

Client Information:
- Name: {user_data.get('name', 'Client')}
- Phone: {user_data.get('phone', 'N/A')}
- Email: {user_data.get('email', 'N/A')}

Would this time work for a property viewing? If not, please let me know your available times and I will coordinate with my client.

Thank you for your time and I look forward to your response.

Best regards,
RentGenius AI Assistant
On behalf of {user_data.get('name', 'Client')}

This message was generated by RentGenius AI - your automated apartment hunting assistant.
            """.strip()
            
            return self.send_email(
                to_email=agent_contact.get('email'),
                subject=subject,
                message=message
            )
            
        else:  # SMS
            message = f"""
Hi {agent_name}, this is RentGenius AI assistant for {user_data.get('name')}. 

Interested in viewing {property_address} on {viewing_time.get('start', '').split('T')[0]} at {viewing_time.get('start', '').split('T')[1].split('.')[0]}.

Client: {user_data.get('phone')}
Can you confirm availability?

Thank you!
            """.strip()
            
            return self.send_sms(
                to_phone=agent_contact.get('phone'),
                message=message
            )

    def send_viewing_confirmation(
        self,
        user_data: Dict,
        property_data: Dict,
        viewing_details: Dict
    ) -> Dict:
        """
        Send confirmation to user about scheduled viewing
        
        Args:
            user_data: User contact information
            property_data: Property details
            viewing_details: Confirmed viewing time and details
            
        Returns:
            Result of sending confirmation
        """
        subject = f"✅ Property Viewing Confirmed - {property_data.get('address')}"
        
        message = f"""
<html>
<body>
<h2>Your Property Viewing is Confirmed! 🏠</h2>

<p>Hi {user_data.get('name', 'there')},</p>

<p>Great news! Your property viewing has been confirmed with the following details:</p>

<div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 15px 0;">
    <h3>📍 Property Details</h3>
    <strong>Address:</strong> {property_data.get('address')}<br>
    <strong>Price:</strong> {property_data.get('price')}<br>
    <strong>Bedrooms:</strong> {property_data.get('bedrooms')}<br>
    <strong>Bathrooms:</strong> {property_data.get('bathrooms')}<br>
</div>

<div style="background-color: #e8f4fd; padding: 15px; border-radius: 5px; margin: 15px 0;">
    <h3>🕐 Viewing Schedule</h3>
    <strong>Date:</strong> {viewing_details.get('date')}<br>
    <strong>Time:</strong> {viewing_details.get('time')}<br>
    <strong>Duration:</strong> {viewing_details.get('duration', '90 minutes')}<br>
</div>

<div style="background-color: #f0f9ff; padding: 15px; border-radius: 5px; margin: 15px 0;">
    <h3>👥 Agent Information</h3>
    <strong>Agent:</strong> {property_data.get('agent_name', 'Property Manager')}<br>
    <strong>Contact:</strong> {property_data.get('agent_contact', {}).get('phone', 'N/A')}<br>
    <strong>Email:</strong> {property_data.get('agent_contact', {}).get('email', 'N/A')}<br>
</div>

<h3>📝 Next Steps:</h3>
<ul>
    <li>📅 Calendar event has been added to your calendar</li>
    <li>⏰ You'll receive a reminder 30 minutes before the viewing</li>
    <li>🚗 Directions will be provided closer to the viewing time</li>
    <li>📋 Prepare any questions you'd like to ask during the viewing</li>
</ul>

<p><strong>Need to reschedule or have questions?</strong> Just reply to this email and I'll help you coordinate any changes.</p>

<p>Looking forward to helping you find your perfect home! 🏡</p>

<hr>
<p><em>This confirmation was generated by RentGenius AI - your personal apartment hunting assistant.</em></p>
</body>
</html>
        """
        
        return self.send_email(
            to_email=user_data.get('email'),
            subject=subject,
            message=message,
            is_html=True
        )

    def send_viewing_reminder(
        self,
        user_data: Dict,
        property_data: Dict,
        viewing_details: Dict,
        reminder_type: str = "30min"
    ) -> Dict:
        """
        Send viewing reminder to user
        
        Args:
            user_data: User contact information
            property_data: Property details
            viewing_details: Viewing details
            reminder_type: "30min", "1day", etc.
            
        Returns:
            Result of sending reminder
        """
        if reminder_type == "30min":
            subject = "🔔 Property Viewing in 30 Minutes!"
            message_content = f"""
Your property viewing is starting in 30 minutes!

📍 Address: {property_data.get('address')}
🕐 Time: {viewing_details.get('time')}
👤 Agent: {property_data.get('agent_name')}
📞 Agent Phone: {property_data.get('agent_contact', {}).get('phone', 'N/A')}

Don't forget to bring:
- Valid ID
- Questions about the property
- Checkbook (if you love it!)

Safe travels! 🚗
            """
        else:  # 1 day reminder
            subject = "📅 Property Viewing Tomorrow"
            message_content = f"""
Reminder: You have a property viewing scheduled for tomorrow!

📍 {property_data.get('address')}
🕐 {viewing_details.get('time')}
👤 Agent: {property_data.get('agent_name')}

I'll send you another reminder 30 minutes before the viewing.
            """
        
        # Send both email and SMS for important reminders
        email_result = self.send_email(
            to_email=user_data.get('email'),
            subject=subject,
            message=message_content
        )
        
        sms_result = self.send_sms(
            to_phone=user_data.get('phone'),
            message=f"🏠 Viewing reminder: {property_data.get('address')} at {viewing_details.get('time')}. Agent: {property_data.get('agent_name')} ({property_data.get('agent_contact', {}).get('phone', 'N/A')})"
        )
        
        return {
            'email_result': email_result,
            'sms_result': sms_result,
            'reminder_type': reminder_type
        }

    def handle_agent_response(
        self,
        agent_response: str,
        original_request: Dict
    ) -> Dict:
        """
        Process and respond to property agent's response
        
        Args:
            agent_response: Agent's response content
            original_request: Original viewing request details
            
        Returns:
            Next steps based on agent response
        """
        response_lower = agent_response.lower()
        
        if any(word in response_lower for word in ['yes', 'confirmed', 'available', 'works']):
            return {
                'status': 'confirmed',
                'action': 'send_confirmation',
                'message': 'Agent confirmed the viewing time',
                'next_steps': [
                    'Send confirmation to user',
                    'Add to calendar',
                    'Set up reminders'
                ]
            }
        elif any(word in response_lower for word in ['no', 'not available', 'busy', 'conflict']):
            return {
                'status': 'declined',
                'action': 'reschedule',
                'message': 'Agent declined the proposed time',
                'next_steps': [
                    'Ask agent for alternative times',
                    'Check user availability for alternatives',
                    'Propose new times'
                ]
            }
        elif any(word in response_lower for word in ['alternative', 'different', 'other']):
            return {
                'status': 'alternative_needed',
                'action': 'find_alternatives',
                'message': 'Agent suggested alternative times',
                'next_steps': [
                    'Extract suggested times',
                    'Check user calendar',
                    'Confirm best alternative'
                ]
            }
        else:
            return {
                'status': 'unclear',
                'action': 'request_clarification',
                'message': 'Agent response needs clarification',
                'next_steps': [
                    'Ask agent for clear yes/no',
                    'Request specific available times'
                ]
            }