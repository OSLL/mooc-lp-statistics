from django.db import models


class Update(models.Model):
    date_from = models.CharField(max_length=255)
    date_to = models.CharField(max_length=255)
    event = models.CharField(max_length=10)
