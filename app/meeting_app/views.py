from django.shortcuts import render
from meeting_app.models import Resume


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


def my_summaries(request):
    user_summaries = Resume.objects.filter(attendees=request.user)
    return render(request, "summaries/summaries.html", {"summaries": user_summaries})

def profile(request):
    return render(request, "profile/profile.html")

def summaries(request):
    my_summaries = Resume.objects.all()
    return render(
        request,
        "summaries/summaries.html",
        {"summaries": my_summaries},
    )


def summary(request, id):
    summary = Resume.objects.get(id=id)
    return render(request, "summaries/summary.html", {"summary": summary})
