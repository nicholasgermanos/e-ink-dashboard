import datetime
import itertools
from collections import defaultdict
from datetime import date, datetime, timedelta

import pytz
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from icalevents.icalevents import events


def get_word_of_the_day():
    today = datetime.today()
    date = (
        today.strftime("%Y") + "-" + today.strftime("%m") + "-" + today.strftime("%d")
    )
    response = requests.get("https://www.merriam-webster.com/word-of-the-day/" + date)
    soup = BeautifulSoup(response.text)
    description_div = soup.find_all("div", class_="wod-definition-container")
    word_container = soup.find_all("h2", class_="word-header-txt")
    breakdown = {}
    breakdown["word"] = word_container[0].get_text()
    word = word_container[0].get_text()

    for div in itertools.islice(description_div[0].findChildren(), 4):
        if div.name == "em":
            continue
        text = div.get_text()
        if "// " in text:
            breakdown["quote"] = text.replace("// ", "")
        elif "See the entry >" in text:
            break
        elif "What It Means" not in text:
            breakdown["description"] = text

    return breakdown


def current_weather():
    city = "Bardia"
    url = "https://wttr.in/" + city + "?format=j1"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    print(data)

    current = data["current_condition"][0]

    return current


def get_ical():
    ical_url = "webcal://p123-caldav.icloud.com/published/2/MTA0ODgzODA0MTEwNDg4M04dWs7LRR4z1Kr4_jOx8I5II3vFh9GYSbJ22eWggG6gbIuJCQ-LYt-QvpczWO-JE_n35D2wAlks2Lv_4WBmMKI"
    start = datetime.now()
    end = start + timedelta(days=7)
    my_tz = pytz.timezone("Australia/Sydney")
    es = events(url=ical_url, start=start, end=end, fix_apple=True, tzinfo=my_tz)

    events_dict = defaultdict(list)

    today = datetime.now().date()
    tomorrow = (datetime.now() + timedelta(days=1)).date()

    for event in es:
        if not event.start:
            continue

        event_date = event.start.date()

        if event_date == today:
            key = "Today"
        elif event_date == tomorrow:
            key = "Tomorrow"
        else:
            key = event.start.strftime("%A")  # Day name

        event_data = {
            "summary": event.summary,
            "start_time": event.start.strftime("%H:%M") if event.start else None,
            "end_time": event.end.strftime("%H:%M") if event.end else None,
            "description": event.description,
            "location": event.location,
            "date": (
                event.start.strftime("%d") + get_ordinal(event.start.day)
                if event.start
                else None
            ),
        }

        events_dict[key].append(event_data)

    return dict(events_dict)


def get_ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return suffix


def index(request):
    context = {}
    # Date
    today = date.today()
    day = today.strftime("%A")
    day_number = today.strftime("%d") + get_ordinal(today.day)
    context["day"] = day
    context["day_number"] = day_number
    context["month"] = today.strftime("%B")

    # Weather
    current = current_weather()
    context["current_temp"] = current["temp_C"]
    context["feels_like_temp"] = current["FeelsLikeC"]

    # Calendar
    context["events"] = get_ical()

    # Word of the day
    context["word_of_the_day"] = get_word_of_the_day()

    return render(request, "display/index.html", context)
