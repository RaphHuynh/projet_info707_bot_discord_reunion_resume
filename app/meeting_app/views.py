from django.shortcuts import render
from meeting_app.models import User, Message, Resume


def index(request):
    return render(request, "index.html")


def resume(request):
    resumes = Resume.objects.all()
    return render(request, "resume.html", {"resumes": resumes})


def login(request):
    return render(request, "login.html")


def tutorial(request):
    return render(request, "tutorial.html")

