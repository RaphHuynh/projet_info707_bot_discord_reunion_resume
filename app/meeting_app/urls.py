from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("login", views.login, name="login"),
    path("tutorial/", views.tutorial, name="tutorial"),
    path("summaries/", views.summaries, name="summaries"),
    path("my_summaries/", views.my_summaries, name="my_summaries"),
    path("summary/<int:id>/", views.summary, name="summary"),
    path("profile", views.profile, name="profile"),
]
