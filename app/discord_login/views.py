from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
import requests
from django.contrib.auth.decorators import user_passes_test

auth_url_discord = "https://discord.com/oauth2/authorize?client_id=1305611546755338291&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogin%2Fredirect&scope=identify"


@user_passes_test(test_func=lambda u: not u.is_authenticated, login_url="/")
def discord_login(request: HttpRequest):
    return redirect(auth_url_discord)


@user_passes_test(test_func=lambda u: not u.is_authenticated, login_url="/")
def discord_login_redirect(request: HttpRequest):
    code = request.GET.get("code")
    print(code)
    user = exchange_code(code)

    discord_user = authenticate(request, user=user)
    print(discord_user)
    login(request, discord_user)
    return redirect("/")


@user_passes_test(test_func=lambda u: u.is_authenticated, login_url="/")
def discord_logout(request: HttpRequest):
    logout(request)
    return redirect("/")


def exchange_code(code: str):
    data = {
        "client_id": "1305611546755338291",
        "client_secret": "qrHiseMUv4EXFaNUulRUTb_DM8JYzoIb",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/oauth2/login/redirect",
        "scope": "identify",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "https://discord.com/api/oauth2/token", data=data, headers=headers
    )

    credentials = response.json()
    access_token = credentials["access_token"]
    response = requests.get(
        "https://discord.com/api/v6/users/@me",
        headers={"Authorization": "Bearer %s" % access_token},
    )

    user = response.json()

    return user