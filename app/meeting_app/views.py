from django.shortcuts import render
from meeting_app.models import User, Message, Resume


def home(request):
    recent_summaries = [
        {
            "id": 1,
            "title": "Team Sync - Nov 15",
            "short_description": "A summary of the team sync meeting covering major updates and next steps.",
        },
        {
            "id": 2,
            "title": "Project Kickoff - Nov 10",
            "short_description": "Discussion on project goals, timelines, and team responsibilities.",
        },
    ]
    return render(request, "home/home.html", {"recent_summaries": recent_summaries})


def login(request):
    return render(request, "logging/login.html")


def tutorial(request):
    return render(request, "tutorial/tutorial.html")


def search_summaries(request):
    searched_summary = Resume.objects.all()
    return render(
        request,
        "summaries/summaries.html",
        {"summaries": searched_summary},
    )


def summaries(request):
    my_summaries = Resume.objects.all()
    return render(
        request,
        "summaries/summaries.html",
        {"summaries": my_summaries},
    )


def public_meetings(request):
    my_summaries = Resume.objects.all()
    return render(
        request,
        "summaries/summaries.html",
        {"summaries": my_summaries},
    )
