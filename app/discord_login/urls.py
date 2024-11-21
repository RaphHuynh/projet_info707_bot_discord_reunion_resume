from django.urls import path
from . import views

urlpatterns = [
    path("", views.discord_login, name="discord_login"),
    path("login", views.discord_login, name="oauth_login"),
    path(
        "login/redirect",
        views.discord_login_redirect,
        name="discord_login_redirect",
    ),
    path("logout", views.discord_logout, name="oauth_logout"),
]
