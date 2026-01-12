import datetime
from collections import defaultdict
from datetime import date, datetime, timedelta

import pytz
import requests
from django.shortcuts import render
from icalevents.icalevents import events
from icalevents.icalparser import parse_events


def current_weather():
    city = "Bardia"
    url = "https://wttr.in/" + city + "?format=j1"

    # response = requests.get(url)
    # response.raise_for_status()

    # data = response.json()

    data = {}
    current_condition = {}
    current_condition['temp_C'] = "19"
    current_condition['FeelsLikeC'] = "19"
    data["current_condition"] = current_condition

    # current = data['current_condition'][0]
    current = data['current_condition']

    return current

def get_ical():
    ical_url = 'webcal://p123-caldav.icloud.com/published/2/MTA0ODgzODA0MTEwNDg4M04dWs7LRR4z1Kr4_jOx8I5II3vFh9GYSbJ22eWggG6gbIuJCQ-LYt-QvpczWO-JE_n35D2wAlks2Lv_4WBmMKI'
    start = datetime.now()
    end = start + timedelta(days=7)
    my_tz = pytz.timezone('Australia/Sydney')
    es = events(url=ical_url, start=start, end=end, fix_apple=True, tzinfo=my_tz)
    days = {}
    formatted_events = {}

    events_dict = defaultdict(list)

    today = datetime.now().date()
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    
    for event in es:
        if not event.start:
            continue
            
        event_date = event.start.date()
        
        # Determine key
        if event_date == today:
            key = "Today"
        elif event_date == tomorrow:
            key = "Tomorrow"
        else:
            key = event.start.strftime('%A')  # Day name
        
        # Format event data
        event_data = {
            'summary': event.summary,
            'start_time': event.start.strftime('%H:%M') if event.start else None,
            'end_time': event.end.strftime('%H:%M') if event.end else None,
            'description': event.description,
            'location': event.location
        }
        
        events_dict[key].append(event_data)
    
    return dict(events_dict)


def index(request):
    context = {}
    # Date
    wd = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    today = date.today()
    day = wd[today.weekday()]
    today.weekday
    context['day'] = day
    context['date'] = "12 Jan"

    # Weather
    current = current_weather()
    context['current_temp'] = current["temp_C"]
    context['feels_like_temp'] = current["FeelsLikeC"]

    # Calendar
    context['events'] = get_ical()

    return render(request, "display/index.html", context)
