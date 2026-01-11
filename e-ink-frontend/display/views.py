from django.shortcuts import render
import datetime
import requests

def current_weather():
    city = "Bardia"
    url = "https://wttr.in/" + city + "?format=j1"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    current = data['current_condition'][0]
    return current

def index(request):
    context = {}

    # Date
    wd = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    today = datetime.datetime.today()
    day = wd[today.weekday()]
    today.weekday
    context['day'] = day
    context['date'] = "12 Jan"

    # Weather
    current = current_weather()
    context['current_temp'] = current["temp_C"]
    context['feels_like_temp'] = current["FeelsLikeC"]

    return render(request, "display/index.html", context)
