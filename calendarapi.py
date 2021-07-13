from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from os import path

if path.exists('token.pkl') == False:
    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=scopes)
    credentials = flow.run_console()
    pickle.dump(credentials, open('token.pkl', 'wb'))

credentials = pickle.load(open('token.pkl', 'rb'))
service = build('calendar', 'v3', credentials=credentials)


