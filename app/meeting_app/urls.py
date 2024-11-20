from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("login", views.login, name="login"),
    path("tutorial/", views.tutorial, name="tutorial"),
    path("summaries/", views.summaries, name="summaries"),
    path("public-meetings/", views.public_meetings, name="public_meetings"),
    path("search/", views.search_summaries, name="search_summaries"),
]
