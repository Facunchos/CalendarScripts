import datetime
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

def edit_event_to_yearly(service, event):
    event['recurrence'] = ['RRULE:FREQ=YEARLY']
    service.events().update(
        calendarId='primary',
        eventId=event['id'],
        body=event
    ).execute()
    print(f'✅ Updated "{event["summary"]}" to repeat yearly')

def main():
    service = get_calendar_service()
    current_year = datetime.date.today().year
    start_date = datetime.date(current_year, 1, 1)
    end_date = datetime.date(current_year, 12, 31)

    current_date = start_date
    while current_date <= end_date:
        day_start = current_date.isoformat() + "T00:00:00Z"
        day_end = current_date.isoformat() + "T23:59:59Z"

        events_result = service.events().list(
            calendarId='primary',
            timeMin=day_start,
            timeMax=day_end,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        # Filter for all-day events (birthdays)
        all_day_events = [
            e for e in events
            if 'date' in e.get('start', {})  # This means no time, just a date
        ]

        if all_day_events:
            print(f"\n📅 {current_date.strftime('%d %B %Y')}")
            for event in all_day_events:
                title = event.get('summary', '(No title)')
                # Verificar si el evento ya repite anualmente
                recurrence = event.get('recurrence', [])
                already_yearly = any('FREQ=YEARLY' in r for r in recurrence)
                if already_yearly:
                    print(f'🔁 "{title}" ya repite anualmente, se omite.')
                    continue
                    # Verificar si existe el evento el año siguiente
                event_date_str = event['start']['date']
                event_date = datetime.datetime.strptime(event_date_str, '%Y-%m-%d').date()
                next_year_date = event_date.replace(year=event_date.year + 1)
                next_year_start = next_year_date.isoformat() + "T00:00:00Z"
                next_year_end = next_year_date.isoformat() + "T23:59:59Z"
                next_year_events_result = service.events().list(
                    calendarId='primary',
                    timeMin=next_year_start,
                    timeMax=next_year_end,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
                next_year_events = next_year_events_result.get('items', [])
                exists_next_year = any(e.get('summary', '(No title)') == title for e in next_year_events if 'date' in e.get('start', {}))
                if exists_next_year:
                    print(f'⏩ "{title}" ya existe el próximo año, se omite.')
                    continue
                edit_event_to_yearly(service, event)
                # choice = input(f'Do you want to edit "{title}" to repeat yearly? y/n\n- ').strip().lower()
                # if choice == 'y':

        current_date += datetime.timedelta(days=1)

if __name__ == '__main__':
    main()
