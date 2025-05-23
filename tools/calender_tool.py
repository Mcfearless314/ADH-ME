from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']


class CalendarTool:
    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.credentials_file = os.path.join(script_dir, credentials_file)
        self.token_file = os.path.join(script_dir, token_file)

    def get_credentials(self):
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        return creds

    def create_event(self, summary, description, start_dt, end_dt):
        creds = self.get_credentials()
        service = build('calendar', 'v3', credentials=creds)

        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_dt.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_dt.isoformat(),
                'timeZone': 'UTC',
            },
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {created_event.get('htmlLink')}")
        return created_event.get('htmlLink')

    def create_events(self, events):
        links = []
        for ev in events:
            link = self.create_event(
                ev['summary'],
                ev['description'],
                ev['start_dt'],
                ev['end_dt']
            )
            links.append(link)
        return links
