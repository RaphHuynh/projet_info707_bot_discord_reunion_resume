from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def resume(request):
    return render(request, "resume.html")


def login(request):
    return render(request, "login.html")


def tutorial(request):
    return render(request, "tutorial.html")

