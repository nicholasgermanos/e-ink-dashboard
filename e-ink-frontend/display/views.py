from django.shortcuts import render
import datetime

def index(request):
    context = {}

    # Date
    wd = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    today = datetime.datetime.today()
    day = wd[today.weekday()]
    context['day'] = day
    context['date'] = day, " 12 Jan"
    return render(request, "display/index.html", context)
