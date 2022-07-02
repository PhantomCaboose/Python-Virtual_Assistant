###########################################################
#------------------------ IMPORTS ------------------------#
###########################################################
from __future__ import print_function

import datetime, os.path, pytz, main

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import Style

###########################################################
#----------------------- VARIABLES -----------------------#
###########################################################
SCOPES = ['https://www.googleapis.com/auth/calendar']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENSIONS = ["rd", "th", "st", "nd"]

###########################################################
#----------------------- FUNCTIONS -----------------------#
###########################################################
def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_date(text):
    text = text.lower()
    today = datetime.date.today()
    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year
    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for extention in DAY_EXTENSIONS:
                found = word.find(extention)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    if month < today.month and month != -1:
        year = year + 1
    if day < today.day and month == -1 and day != -1:
        month = month + 1
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        difference = day_of_week - current_day_of_week
        if difference < 0:
            difference += 7
            if text.count("next") >= 1:
                difference += 7
        return today + datetime.timedelta(difference)
    if month == -1 or day == -1:
        return None
    return datetime.date(month = month, day = day, year = year)

def get_events(day, service):
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId = 'primary', timeMin = date.isoformat(),
                                          timeMax = end_date.isoformat(), singleEvents = True,
                                          orderBy = 'startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print(f'You have no upcoming events found for {day}.')
        main.speak(f"You have no upcoming events found for {day}.")
    else:
        print(f"You have {len(events)} events on this day.")
        main.speak(f"You have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            start_time = str(start.split("T")[1].split("-")[0])
            end_time = str(end.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0]) - 12)
                if start_time > "0":
                    start_time = start_time + "pm"
                else:
                    start_time = "12 pm"

            if int(end_time.split(":")[0]) < 12:
                end_time = end_time + "am"
            else:
                end_time = str(int(end_time.split(":")[0]) - 12)
                if end_time > "0":
                    end_time = end_time + "pm"
                else:
                    end_time = "12 pm"
            i = 0
            while i < len(events):
                print(f"[{i + 1}] {Style.YELLOW}{event['summary']}{Style.RESET} at {start_time} until {end_time}")
                main.speak(f"{event['summary']} at {start_time} until {end_time}")
                i = i + 1

def create_event(query, service):
    try:
        query = query.lower()
        title = query.split(' on ')[0].rstrip().replace('add ', '').replace(' to calendar', '')
        print("Creating event...")
        main.speak("Creating event...")

        def start_time():
            starting_time = query.split('from ')[1].rstrip().split(' to')[0].rstrip()
            if 'a.m.' in starting_time:
                starting_time = starting_time.replace('a.m.', '')
                if ' ' in starting_time:
                    starting_time = starting_time.replace(' ', '')
                if len(starting_time) == 1 or len(starting_time) == 2:
                    starting_time = (starting_time + ":00")
                if starting_time[:2] == "12":
                    start = ("00" + starting_time[2:])
                else:
                    start = starting_time
            elif 'p.m.' in starting_time:
                starting_time = starting_time.replace('p.m.', '')
                if ' ' in starting_time:
                    starting_time = starting_time.replace(' ', '')
                if len(starting_time) == 1:
                    starting_time = ("0" + starting_time + ":00")
                if len(starting_time) == 2:
                    starting_time = (starting_time + ":00")
                if len(starting_time) == 4:
                    starting_time = ("0" + starting_time)
                if starting_time[:2] == "12":
                    start = starting_time
                else:
                    start = (str(int(starting_time[:2]) + 12) + starting_time[2:5])
            else:
                print("Please specify AM or PM in the Start time of Event")
                main.speak("Please specify AM or PM in the Start time of Event")
                start = start_time()
            return start

        def end_time():
            ending_time = query.split('from ')[1].rstrip().split(' to ')[1].rstrip()
            if 'a.m.' in ending_time:
                ending_time = ending_time.replace('a.m.', '')
                if ' ' in ending_time:
                    ending_time = ending_time.replace(' ', '')
                if len(ending_time) == 1 or len(ending_time) == 2:
                    ending_time = (ending_time + ":00")
                if ending_time[:2] == "12":
                    end = ("00" + ending_time[2:])
                else:
                    end = ending_time
            elif 'p.m.' in ending_time:
                ending_time = ending_time.replace('p.m.', '')
                if ' ' in ending_time:
                    ending_time = ending_time.replace(' ', '')
                if len(ending_time) == 1:
                    ending_time = ("0" + ending_time + ":00")
                if len(ending_time) == 2:
                    ending_time = (ending_time + ":00")
                if len(ending_time) == 4:
                    ending_time = ("0" + ending_time)
                if ending_time[:2] == "12":
                    end = ending_time
                else:
                    end = (str(int(ending_time[:2]) + 12) + ending_time[2:5])

            else:
                print("Please specify AM or PM in the End time of Event")
                main.speak("Please specify AM or PM in the End time of Event")
                end = end_time()

            starting_hour = int(start[0:2])
            starting_minute = int(start[-2:])
            ending_hour = int(end[0:2])
            ending_minute = int(end[-2:])
            if (ending_hour < starting_hour or (ending_hour == starting_hour and ending_minute <= starting_minute)):
                print("End time should always be greater than start time")
                main.speak("End time should always be greater than start time")
                end = end_time()
            return end

        def convert_date():
            month = query.split('on ')[1].rstrip().split(' from')[0].rstrip().split(' ')[0].rstrip()
            day = query.split('on ')[1].rstrip().split(' from')[0].rstrip().split(' ')[1].rstrip()
            year = str(datetime.datetime.now().year)

            Month_dict = {1: 'january', 2: 'february', 3: 'march', 4: 'april',
                          5: 'may', 6: 'june', 7: 'july', 8: 'august',
                          9: 'september', 10: 'october', 11: 'november', 12: 'december'}

            Day_dict = {1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 5: '5th',
                        6: '6th', 7: '7th', 8: '8th', 9: '9th', 10: '10th',
                        11: '11th', 12: '12th', 13: '13th', 14: '14th', 15: '15th',
                        16: '16th', 17: '17th', 18: '18th', 19: '19th', 20: '20th',
                        21: '21st', 22: '22nd', 23: '23rd', 24: '24th',
                        25: '25th', 26: '26th', 27: '27th', 28: '28th',
                        29: '29th', 30: '30th', 31: '31st'}

            if month.lower() in Month_dict.values():
                for key, value in Month_dict.items():
                    if month.lower() == value:
                        month = str(key)

            if day.lower() in Day_dict.values():
                for key, value in Day_dict.items():
                    if day.lower() == value:
                        day = str(key)

            date = f"{month}-{day}-{year}"
            return date

        start = start_time()
        end = end_time()
        date = convert_date()

        new_date = datetime.datetime.strptime(date, "%m-%d-%Y")
        startdate = str(new_date).split(' ')[0].rstrip() + 'T' + start + ":00"
        enddate = str(new_date).split(' ')[0].rstrip() + 'T' + end + ":00"

        event = {'summary': title, 'start': {'dateTime': startdate, 'timeZone': 'America/Chicago'},
                 'end': {'dateTime': enddate, 'timeZone': 'America/Chicago'}}

        service.events().insert(calendarId = 'primary', body = event).execute()

        print("\n   Creating event....")
        print("     ------------------------------------")
        print(f"          EVENT TITLE: {title}")
        print(f"          DATE OF EVENT: {date}")
        print(f"          EVENT START TIME: {start}")
        print(f"          Event END TIME:   {end}")
        print("     ------------------------------------")
        print(f"Event created {Style.YELLOW}{event['summary']}{Style.RESET} on {date}")
        print(f"   {Style.GREEN}EVENT CREATED SUCCESSFULLY{Style.RESET}....")
        main.speak(f"Event created {event['summary']} on {date}")
    except:
        print("I am unable to create this event at this time.")
        main.speak("I am unable to create this event at this time.")
        print(f"   {Style.RED}FAILED TO CREATE EVENT{Style.RESET}....")

def delete_event(query, service):
    try:
        query = query.lower().replace(' from calendar', '').replace('delete ', '')
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            main.speak('No upcoming events found')
        else:
            event_name = query
            s = 0
            h = 0
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                str2 = (str(start))
                str2 = str2[-14:-9]
                date = datetime.datetime.strptime(str2, "%H:%M")
                date_2 = date.strftime("%I:%M %p")
                s = s + 1
                if event['summary'] == event_name:
                    foxs = (event['id'])
                    service.events().delete(calendarId='primary', eventId=foxs).execute()
                    print(event_name + ' event at ' + date_2 + ' deleted')
                    main.speak(event_name + ' event at ' + date_2 + ' deleted')
                    print(" Event Deleted...")
                else:
                    h = h + 1
            if s == h:
                print(event_name + ' event not found')
                main.speak(event_name + ' event not found')
    except:
        print("I am unable to delete this event...")
        main.speak("I am unable to delete this event...")
