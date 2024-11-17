from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("resume", views.resume, name="resume"),
    path("login", views.login, name="login"),
    path("tutorial", views.tutorial, name="tutorial"),
]
