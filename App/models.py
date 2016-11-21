from django.db import models


class Find_in_database(models.Model):
    date_from = models.CharField(max_length=255)
    date_to = models.CharField(max_length=255)
    event = models.CharField(max_length=100)
    interval = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    offset = models.CharField(max_length=100)



