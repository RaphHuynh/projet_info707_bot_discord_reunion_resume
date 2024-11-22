from django.db import models
from .managers import DiscordUserOAuth2Manager


class DiscordUser(models.Model):
    objects = DiscordUserOAuth2Manager()

    id = models.BigIntegerField(primary_key=True)
    discord_tag = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    public_flags = models.IntegerField(null=True)
    global_name = models.CharField(max_length=100)
    flags = models.IntegerField(null=True)
    locale = models.CharField(max_length=100, null=True)
    mfa_enabled = models.BooleanField(null=True)
    last_login = models.DateTimeField(null=True)

    def is_authenticated(self):
        return True
