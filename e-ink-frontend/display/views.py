import datetime
import math
import random
import zoneinfo
from collections import defaultdict
from datetime import date, datetime, timedelta

import pytz
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from icalevents.icalevents import events


def get_word_of_the_day():
    response = requests.get("https://www.merriam-webster.com/word-of-the-day/")
    # response = requests.get(
    #     "https://www.merriam-webster.com/word-of-the-day/vendetta-2026-01-16"
    # )
    soup = BeautifulSoup(response.text)
    description_div = soup.find_all("div", class_="wod-definition-container")
    word_container = soup.find_all("h2", class_="word-header-txt")
    breakdown = {}
    breakdown["word"] = word_container[0].get_text()

    for div in description_div[0].findChildren():
        print(div)
        if div.name != "p":
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
    url = "https://api.open-meteo.com/v1/forecast?latitude=-33.9776690401036&longitude=150.85373113387638&daily=uv_index_max,weather_code,rain_sum,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_probability_max&hourly=temperature_2m,weather_code,showers,rain&timezone=Australia%2FSydney&forecast_days=4"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    def get_weather_icon(code):
        overcast = "overcast.svg"
        sunny = "sunny.svg"
        cloudy_night = "cloudy_night.svg"
        clear_night = "clear_night.svg"
        rainy = "rainy.svg"
        partial_cloud = "cloudy_2.svg"
        stormy = "stormy.svg"
        snowy = "snowflake.svg"

        icons = {
            0: sunny,
            1: sunny,
            2: partial_cloud,
            3: overcast,
            45: overcast,
            48: overcast,
            51: rainy,
            53: rainy,
            55: rainy,
            61: rainy,
            63: rainy,
            65: stormy,
            71: snowy,
            73: snowy,
            75: snowy,
            80: rainy,
            81: rainy,
            82: rainy,
            95: stormy,
            96: stormy,
            99: stormy,
        }

        return icons.get(code, partial_cloud)

    def get_weather_description(code):
        descriptions = {
            0: "Clear",
            1: "Mostly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light Drizzle",
            53: "Drizzle",
            55: "Heavy Drizzle",
            61: "Light Rain",
            63: "Rain",
            65: "Heavy Rain",
            71: "Light Snow",
            73: "Snow",
            75: "Heavy Snow",
            80: "Light Showers",
            81: "Moderate Showers",
            82: "Heavy Showers",
            95: "Thunderstorm",
            96: "Light Hail",
            99: "Heavy Hail!",
        }

        return descriptions.get(code, "Unknown")

    periods = [
        {"name": "Morning", "start": 5, "end": 11},
        {"name": "Afternoon", "start": 11, "end": 19},
        {"name": "Evening", "start": 19, "end": 23},
    ]

    today_periods = []
    for period in periods:
        start_idx = period["start"]
        end_idx = period["end"]
        temps = data["hourly"]["temperature_2m"][start_idx:end_idx]
        weather_codes = data["hourly"]["weather_code"][start_idx:end_idx]

        today_periods.append(
            {
                "name": period["name"],
                "temp_avg": math.ceil(max(set(temps))),
                "condition": get_weather_description(max(set(weather_codes))),
                "icon_src": get_weather_icon(max(set(weather_codes))),
            }
        )

    days = [
        {"name": "Today"},
        {"name": "Tomorrow"},
        {
            "name": (
                datetime.now(zoneinfo.ZoneInfo("Australia/Sydney")) + timedelta(days=2)
            )
            .date()
            .strftime("%A")
        },
        {
            "name": (
                datetime.now(zoneinfo.ZoneInfo("Australia/Sydney")) + timedelta(days=3)
            )
            .date()
            .strftime("%A")
        },
    ]

    for index, day in enumerate(days):
        day["min_temp"] = math.ceil(data["daily"]["temperature_2m_min"][index])
        day["max_temp"] = math.ceil(data["daily"]["temperature_2m_max"][index])
        day["condition"] = get_weather_description(data["daily"]["weather_code"][index])
        day["icon_src"] = get_weather_icon(data["daily"]["weather_code"][index])
        day["max_uv"] = math.ceil(data["daily"]["uv_index_max"][index])
        day["rain_chance"] = data["daily"]["precipitation_probability_max"][index]

    weather = {
        "today_periods": today_periods,
        "days": days,
    }

    return weather


def get_ical():
    ical_url = "webcal://p123-caldav.icloud.com/published/2/MTA0ODgzODA0MTEwNDg4M04dWs7LRR4z1Kr4_jOx8I5II3vFh9GYSbJ22eWggG6gbIuJCQ-LYt-QvpczWO-JE_n35D2wAlks2Lv_4WBmMKI"
    australian_holidays_url = "https://calendars.icloud.com/holidays/au_en-au.ics/"
    start = datetime.now(zoneinfo.ZoneInfo("Australia/Sydney"))
    end = start + timedelta(days=28)
    my_tz = pytz.timezone("Australia/Sydney")
    es = events(url=ical_url, start=start, end=end, fix_apple=True, tzinfo=my_tz)
    holidays_es = events(url=australian_holidays_url, start=start, end=end, fix_apple=True, tzinfo=my_tz)
    holidays_es = list(filter(lambda k: 'NSW' in str(k.summary) or ("(" not in str(k.summary) and ")" not in str(k.summary)), holidays_es))
    es = es + holidays_es

    events_dict = defaultdict(list)

    today = datetime.now(zoneinfo.ZoneInfo("Australia/Sydney")).date()
    tomorrow = (datetime.now(zoneinfo.ZoneInfo("Australia/Sydney")) + timedelta(days=1)).date()

    def sort_by_day(e):
        return e.start

    es.sort(key=sort_by_day)

    new_week_counter = 0
    for event in es:
        if not event.start:
            continue

        event_date = event.start.date()
        key = event_date

        day_name = str()
        if event_date == today:
            day_name = "Today"
        elif event_date == tomorrow:
            day_name = "Tomorrow"
        else:
            day_name = event.start.strftime("%A")

        start_time = event.start.strftime("%-H:%M") if event.start else None
        end_time = event.end.strftime("%-H:%M") if event.end else None
        all_day = False

        if event.start and event.end:
            all_day = (event.end - event.start).total_seconds() / 60 == 1440

        
        description = str()
        if "observed in your region" not in str(event.description): 
            description = event.description

        new_week = False
        if abs(event.start.date() - today).days / 7 > new_week_counter:
            new_week_counter = new_week_counter + 1
            new_week = True
        elif new_week_counter == 0 and event.start.date() != today:
            new_week = True

        event_data = {
            "new_week": new_week_counter - 1 if new_week else None,
            "day_of_week": day_name, 
            "summary": event.summary,
            "start_time": start_time,
            "end_time": end_time,
            "all_day": all_day,
            "description": description,
            "location": event.location,
            "date": (
                event.start.strftime("%-d") + get_ordinal(event.start.day)
                if event.start
                else None
            ),
        }

        events_dict[key].append(event_data)

    return dict(events_dict)


def get_fun():

    fun = {}

    # titles
    titles = [
        "Psst",
        "I gotta tell you something",
        "Guess what",
        "You're gonna love this",
        "Guys guess what",
        "I bet you've never heard this",
        "Can I tell you something?",
    ]

    fun["title"] = random.choice(titles)

    dice_roll = random.randrange(0, 2)

    print(dice_roll)
    if dice_roll == 0:
        url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
        response = requests.get(url)
        data = response.json()
        fun["text"] = data["text"]

    elif dice_roll == 1:
        url = "https://icanhazdadjoke.com/"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        data = response.json()
        print(data)
        fun["text"] = data["joke"]

    return fun

def get_train_game():
    a = random.randrange(0,9)
    b = random.randrange(0,9)
    c = random.randrange(0,9)
    d = random.randrange(0,9)
    return [a, b, c, d]

def get_ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return suffix


def index(request):
    context = {}

    # Date
    today = datetime.now(zoneinfo.ZoneInfo("Australia/Sydney"))
    day = today.strftime("%A")
    day_number = today.strftime("%-d") + get_ordinal(today.day)
    context["day"] = day
    context["day_number"] = day_number
    context["month"] = today.strftime("%B")

    # Weather
    context["weather"] = current_weather()

    # Calendar
    context["events"] = get_ical()

    # Word of the day
    context["word_of_the_day"] = get_word_of_the_day()

    #context["fun"] = get_fun()
    context["train_game"] = get_train_game()

    return render(request, "display/index.html", context)
