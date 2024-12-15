from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    print(request.build_absolute_uri()) #optional
    return render(
        request,
        'home.html'
    )