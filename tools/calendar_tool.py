import os
import json
from datetime import datetime
from typing import Annotated

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = '/token.json'
CREDENTIALS_FILE = '/credentials.json'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_credentials():
    creds = None
    if os.path.exists(BASE_DIR+TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(BASE_DIR+TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(BASE_DIR+CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(BASE_DIR+TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds


def schedule_event_handler(title: Annotated[str, "The title of the event"],
                           description: Annotated[str, "A brief description of the event"],
                           start: Annotated[str, "Start time in 'YYYY-MM-DD HH:MM' format"],
                           end: Annotated[str, "End time in 'YYYY-MM-DD HH:MM' format"]) -> Annotated[str, "Whether or not the event was booked successfully and a link to the event"]:
    creds = get_credentials()
    try:
        start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")
    except Exception as e:
        return f"Error parsing event dates: {e}"

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': 'UTC+2',
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': 'UTC+2',
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {created_event.get('htmlLink')}")
    return created_event.get('htmlLink')

