from django.db import models

# Create your models here.
class Region(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    region = models.CharField(
        max_length=30
    )

    def __str__(self):
        return self.region


class Languages(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    languages = models.CharField(
        max_length=30
    )

    def __str__(self):
        return self.languages