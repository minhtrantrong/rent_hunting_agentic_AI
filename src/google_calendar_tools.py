"""
Google Calendar integration tool for Agent #3 - Personal Assistant Agent
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from agno.tools import Toolkit
import google.auth
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json


class GoogleCalendarTools(Toolkit):
    def __init__(
        self,
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
        scopes: List[str] = None
    ):
        super().__init__(name="google_calendar_tools")
        
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.scopes = scopes or ['https://www.googleapis.com/auth/calendar']
        self.service = None
        
        # Register the tools
        self.register(self.get_availability)
        self.register(self.schedule_appointment)
        self.register(self.find_optimal_viewing_slots)
        self.register(self.create_viewing_event)
        self.register(self.send_calendar_invite)

    def _authenticate(self):
        """Authenticate and build Google Calendar service"""
        import os
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                from google_auth_oauthlib.flow import InstalledAppFlow
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.scopes)
                creds = flow.run_local_server(port=0)
            
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('calendar', 'v3', credentials=creds)

    def get_availability(
        self, 
        start_date: str, 
        end_date: str,
        duration_minutes: int = 60
    ) -> List[Dict]:
        """
        Get user's availability for apartment viewings
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format  
            duration_minutes: Required duration for viewing
            
        Returns:
            List of available time slots
        """
        if not self.service:
            self._authenticate()
            
        # Get busy times from primary calendar
        time_min = f"{start_date}T00:00:00Z"
        time_max = f"{end_date}T23:59:59Z"
        
        freebusy_query = {
            'timeMin': time_min,
            'timeMax': time_max,
            'items': [{'id': 'primary'}]
        }
        
        result = self.service.freebusy().query(body=freebusy_query).execute()
        busy_times = result['calendars']['primary']['busy']
        
        # Generate available slots (9 AM - 6 PM, excluding busy times)
        available_slots = []
        current_date = datetime.fromisoformat(start_date)
        end_date_obj = datetime.fromisoformat(end_date)
        
        while current_date <= end_date_obj:
            # Skip weekends for viewing appointments
            if current_date.weekday() < 5:  # Monday = 0
                day_start = current_date.replace(hour=9, minute=0)
                day_end = current_date.replace(hour=18, minute=0)
                
                # Find free slots during business hours
                current_time = day_start
                while current_time + timedelta(minutes=duration_minutes) <= day_end:
                    slot_end = current_time + timedelta(minutes=duration_minutes)
                    
                    # Check if slot conflicts with busy times
                    is_free = True
                    for busy in busy_times:
                        busy_start = datetime.fromisoformat(busy['start'].replace('Z', '+00:00'))
                        busy_end = datetime.fromisoformat(busy['end'].replace('Z', '+00:00'))
                        
                        if not (slot_end <= busy_start or current_time >= busy_end):
                            is_free = False
                            break
                    
                    if is_free:
                        available_slots.append({
                            'start': current_time.isoformat(),
                            'end': slot_end.isoformat(),
                            'duration_minutes': duration_minutes
                        })
                    
                    current_time += timedelta(minutes=30)  # Check every 30 mins
            
            current_date += timedelta(days=1)
        
        return available_slots

    def find_optimal_viewing_slots(
        self, 
        properties: List[Dict],
        preferred_times: List[str] = None
    ) -> List[Dict]:
        """
        Find optimal time slots for viewing multiple properties
        
        Args:
            properties: List of property data with addresses
            preferred_times: User's preferred viewing times
            
        Returns:
            Optimized viewing schedule
        """
        # Get user availability for next 2 weeks
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        
        available_slots = self.get_availability(start_date, end_date, duration_minutes=90)
        
        # Group properties by proximity for efficient routing
        optimal_schedule = []
        
        for i, slot in enumerate(available_slots[:len(properties)]):
            if i < len(properties):
                property_data = properties[i]
                optimal_schedule.append({
                    'property_id': property_data.get('id'),
                    'property_address': property_data.get('address'),
                    'viewing_time': slot,
                    'contact_info': property_data.get('agent_contact'),
                    'estimated_duration': 90,
                    'notes': f"Property viewing #{i+1}"
                })
        
        return optimal_schedule

    def create_viewing_event(
        self,
        property_data: Dict,
        viewing_time: Dict,
        attendees: List[str] = None
    ) -> Dict:
        """
        Create a calendar event for property viewing
        
        Args:
            property_data: Property information
            viewing_time: Selected time slot
            attendees: Email addresses to invite
            
        Returns:
            Created event details
        """
        if not self.service:
            self._authenticate()
        
        event = {
            'summary': f"Property Viewing: {property_data.get('address', 'TBD')}",
            'location': property_data.get('address'),
            'description': f"""
Property Viewing Details:
- Address: {property_data.get('address')}
- Price: {property_data.get('price')}
- Bedrooms: {property_data.get('bedrooms')}
- Agent: {property_data.get('agent_name')}
- Agent Contact: {property_data.get('agent_contact')}

Generated by RentGenius AI Assistant
            """.strip(),
            'start': {
                'dateTime': viewing_time['start'],
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': viewing_time['end'], 
                'timeZone': 'America/New_York',
            },
            'attendees': [{'email': email} for email in (attendees or [])],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                    {'method': 'popup', 'minutes': 30},        # 30 mins before
                ],
            },
        }
        
        created_event = self.service.events().insert(
            calendarId='primary', 
            body=event,
            sendUpdates='all'
        ).execute()
        
        return {
            'event_id': created_event['id'],
            'html_link': created_event['htmlLink'],
            'status': 'created',
            'property_address': property_data.get('address'),
            'viewing_time': viewing_time
        }

    def schedule_appointment(
        self,
        property_data: Dict,
        user_preferences: Dict
    ) -> Dict:
        """
        Main scheduling function - coordinates the entire process
        
        Args:
            property_data: Property information from Agent #1
            user_preferences: User scheduling preferences
            
        Returns:
            Scheduling result with calendar event details
        """
        # Find optimal viewing time
        available_slots = self.get_availability(
            user_preferences.get('start_date'),
            user_preferences.get('end_date'),
            duration_minutes=user_preferences.get('duration', 90)
        )
        
        if not available_slots:
            return {'status': 'error', 'message': 'No available time slots found'}
        
        # Select best slot (first available for now, could add AI optimization)
        selected_slot = available_slots[0]
        
        # Create calendar event
        event_result = self.create_viewing_event(
            property_data,
            selected_slot,
            attendees=[user_preferences.get('email')]
        )
        
        return {
            'status': 'scheduled',
            'event_details': event_result,
            'viewing_time': selected_slot,
            'next_steps': [
                'Calendar invite sent',
                'Will contact property agent to confirm',
                'Reminder set for 30 minutes before viewing'
            ]
        }

    def send_calendar_invite(self, event_id: str, additional_emails: List[str]) -> Dict:
        """Send calendar invite to additional attendees"""
        if not self.service:
            self._authenticate()
            
        # Get existing event
        event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
        
        # Add new attendees
        existing_attendees = event.get('attendees', [])
        for email in additional_emails:
            existing_attendees.append({'email': email})
        
        event['attendees'] = existing_attendees
        
        # Update event
        updated_event = self.service.events().update(
            calendarId='primary',
            eventId=event_id,
            body=event,
            sendUpdates='all'
        ).execute()
        
        return {
            'status': 'invites_sent',
            'event_id': event_id,
            'attendees': [att['email'] for att in updated_event.get('attendees', [])]
        }