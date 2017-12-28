from django.http import HttpResponse
from django.contrib.auth.models import User


def index(request):
    return HttpResponse("Hello, world. PyColos greets you")


def newuser(request):
    return HttpResponse("New user created!")
