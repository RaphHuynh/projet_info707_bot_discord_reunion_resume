from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser


class DiscordAuthentificationBacken(BaseBackend):
    def authenticate(self, request, user):
        try:
            find_user = DiscordUser.objects.get(id=user["id"])
        except DiscordUser.DoesNotExist:
            new_user = DiscordUser.objects.create_new_discord_user(user=user)
            print(f"New user created : {new_user.discord_tag}")
            return new_user
        return find_user

    def get_user(self, user_id):
        try:
            return DiscordUser.objects.get(id=user_id)
        except DiscordUser.DoesNotExist:
            return None
