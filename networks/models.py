from django.db import models
from users.models import User
from myadmin.models import Region, Languages

class Network(models.Model):
    #id = models.TextField(unique=True, primary_key=True, editable=False)
    id = models.CharField(
        max_length=200, unique=True, primary_key=True, editable=False
    )
    owner = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    languages = models.ForeignKey(
        Languages, null=True, blank=True, on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=200
    )
    description = models.TextField(
        null=True, blank=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

class Views(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    ip = models.CharField(
        max_length=100
    )
    date = models.DateTimeField(
        auto_now_add=True
    )
    user_agent = models.CharField(
        max_length=100
    )