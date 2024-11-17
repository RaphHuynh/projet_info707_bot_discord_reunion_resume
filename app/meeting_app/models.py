from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    id_discord = models.CharField(max_length=200)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()


class Resume(models.Model):
    id = models.AutoField(primary_key=True)
    text_resume = models.TextField()
    text_complete = models.TextField()
    users = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message)
