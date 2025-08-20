import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# SCOPES defines the permission we request: calendar events
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    # token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)  # <-- Put your JSON filename here
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def add_birthday_event(service, name, date):
    event = {
        'summary': f"{name}",
        'start': {
            'date': date,  # YYYY-MM-DD format
            'timeZone': 'America/Argentina/Buenos_Aires',
        },
        'end': {
            'date': date,
            'timeZone': 'America/Argentina/Buenos_Aires',
        }
    }
    service.events().insert(calendarId='primary', body=event).execute()
    print(f'Added "{name}" for {date}')

def main():
    service = get_calendar_service()
    current_year = datetime.date.today().year
    start_date = datetime.date(current_year, 1, 1)
    end_date = datetime.date(current_year, 12, 31)

    current_date = start_date
    while current_date <= end_date:
        day = current_date.day
        month = current_date.strftime("%B")  # Full month name
        # choice = input(f"Today is {day} of {month}. Do you want to input a birthday? y/n\n-").strip().lower()
        choice = input(f"Today is {day} of {month}. Do you want to input a birthday? y/n\n-").strip()

        if choice != 'n' and choice != '':
            while True:
                date_str = current_date.strftime("%Y-%m-%d")
                add_birthday_event(service, choice, date_str)
            #     name = input("Please input name\n-").strip()
            #     date_str = current_date.strftime("%Y-%m-%d")
            #     add_birthday_event(service, name, date_str)

                choice = input("Do you want to add another? y/n\n-").strip()
                if choice == 'n' or choice == '':
                    break

        current_date += datetime.timedelta(days=1)

if __name__ == '__main__':
    main()

