from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import dotenv
import pickle
import datefinder
from datetime import timedelta
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim

def create_event(timezone, start_time_str, title, duration, description=None, location=None):

    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
    
    event = {
        'summary': title,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 15},
            ],
        },
    }

    service.events().insert(calendarId='primary', body=event).execute()

def delete_event(name):

    page_token = None
    while True:
        events = service.events().list(calendarId='primary', pageToken=page_token).execute()

        for event in events['items']:
            if name == event['summary']:
                event_ID = event['id']
        
        page_token = events.get('nextPageToken')
        if not page_token:
            break

    service.events().delete(calendarId='primary', eventId=event_ID).execute()

def find_timezone(timezone_city):
    
    geoLocator = Nominatim(user_agent='geoapiExercises')
    location = geoLocator.geocode(timezone_city)
    obj = TimezoneFinder()

    return obj.timezone_at(lng=location.longitude, lat=location.latitude)

dotenv.load_dotenv()

if os.path.exists(str(os.getenv('TOKEN'))) == False:
    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file(str(os.getenv('CLIENT_SECRET')), scopes=scopes)
    credentials = flow.run_console()
    pickle.dump(credentials, open(str(os.getenv('TOKEN')), 'wb'))

credentials = pickle.load(open(str(os.getenv('TOKEN')), 'rb'))
service = build('calendar', 'v3', credentials=credentials)