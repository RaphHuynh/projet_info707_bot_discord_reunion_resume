from django.db import models
from discord_login.models import DiscordUser


class Message(models.Model):
    id = models.AutoField(primary_key=True)

    author = models.ForeignKey(DiscordUser, on_delete=models.CASCADE)

    date = models.DateTimeField()
    duration = models.DurationField()

    content = models.TextField()


class Resume(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=50)
    date = models.DateTimeField()
    duration = models.DurationField()

    text_sum_up = models.TextField()

    attendees = models.ManyToManyField(DiscordUser)
    messages = models.ManyToManyField(Message)
