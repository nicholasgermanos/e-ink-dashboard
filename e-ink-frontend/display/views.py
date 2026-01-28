import datetime
import math
from collections import defaultdict
from datetime import date, datetime, timedelta

import pytz
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from icalevents.icalevents import events


def get_word_of_the_day():
    response = requests.get("https://www.merriam-webster.com/word-of-the-day/")
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
    url = "https://api.open-meteo.com/v1/forecast?latitude=-33.9776690401036&longitude=150.85373113387638&daily=uv_index_max,weather_code,rain_sum,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_probability_max&hourly=temperature_2m,weather_code,showers,rain&timezone=Australia%2FSydney&forecast_days=3"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    def get_weather_icon(code):
        descriptions = {
            0: "sun.png",
            1: "sun.png",
            2: "cloudy.png",
            3: "breezy.png",
            45: "breezy.png",
            48: "breezy.png",
            51: "umbrella.png",
            53: "umbrella.png",
            55: "umbrella.png",
            61: "snowflake.png",
            63: "umbrella.png",
            65: "snowflake.png",
            71: "snowflake.png",
            73: "snowflake.png",
            75: "snowflake.png",
            80: "umbrella.png",
            81: "umbrella.png",
            82: "umbrella.png",
            95: "lightning.png",
            96: "lightning.png",
            99: "lightning.png",
        }

        return descriptions.get(code, "Unknown")

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
        {"name": "Afternoon", "start": 11, "end": 17},
        {"name": "Night", "start": 17, "end": 23},
    ]

    today_periods = []
    for period in periods:
        start_idx = period["start"]
        end_idx = period["end"]
        temps = data["hourly"]["temperature_2m"][start_idx:end_idx]
        codes = data["hourly"]["weather_code"][start_idx:end_idx]

        today_periods.append(
            {
                "name": period["name"],
                "temp_avg": math.ceil(sum(temps) / len(temps)),
                "condition": get_weather_description(max(set(codes), key=codes.count)),
                "icon_src": get_weather_icon(max(set(codes), key=codes.count)),
            }
        )

    weather = {
        "daily": data["daily"],
        "hourly": data["hourly"],
        "today_periods": today_periods,
        "tomorrow_temp_min": math.ceil(data["daily"]["temperature_2m_min"][1]),
        "tomorrow_temp_max": math.ceil(data["daily"]["temperature_2m_max"][1]),
        "tomorrow_condition": get_weather_description(data["daily"]["weather_code"][1]),
        "tomorrow_icon_src": get_weather_icon(data["daily"]["weather_code"][1]),
        "next_day_temp_min": math.ceil(data["daily"]["temperature_2m_min"][2]),
        "next_day_temp_max": math.ceil(data["daily"]["temperature_2m_max"][2]),
        "next_day_condition": get_weather_description(data["daily"]["weather_code"][2]),
        "next_day_icon_src": get_weather_icon(data["daily"]["weather_code"][2]),
        "next_day_name": (datetime.now() + timedelta(days=2)).date().strftime("%A"),
    }

    return weather


def get_ical():
    ical_url = "webcal://p123-caldav.icloud.com/published/2/MTA0ODgzODA0MTEwNDg4M04dWs7LRR4z1Kr4_jOx8I5II3vFh9GYSbJ22eWggG6gbIuJCQ-LYt-QvpczWO-JE_n35D2wAlks2Lv_4WBmMKI"
    start = datetime.now()
    end = start + timedelta(days=14)
    my_tz = pytz.timezone("Australia/Sydney")
    es = events(url=ical_url, start=start, end=end, fix_apple=True, tzinfo=my_tz)

    events_dict = defaultdict(list)

    today = datetime.now().date()
    tomorrow = (datetime.now() + timedelta(days=1)).date()

    def sort_by_day(e):
        return e.start

    es.sort(key=sort_by_day)

    for event in es:
        if not event.start:
            continue

        event_date = event.start.date()

        if event_date == today:
            key = "Today"
        elif event_date == tomorrow:
            key = "Tomorrow"
        else:
            key = event.start.strftime("%A")

        start_time = event.start.strftime("%H:%M") if event.start else None
        end_time = event.end.strftime("%H:%M") if event.end else None
        all_day = False

        if event.start and event.end:
            all_day = (event.end - event.start).total_seconds() / 60 == 1440

        event_data = {
            "summary": event.summary,
            "start_time": start_time,
            "end_time": end_time,
            "all_day": all_day,
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
    context["weather"] = current_weather()

    # Calendar
    context["events"] = get_ical()

    # Word of the day
    context["word_of_the_day"] = get_word_of_the_day()

    return render(request, "display/index.html", context)
