from django.shortcuts import render


def index(request):
    context = {}
    return render(request, "display/index.html", context)
