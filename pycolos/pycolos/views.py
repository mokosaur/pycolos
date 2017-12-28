from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def newuser(request):
    return HttpResponse("New user created!")
