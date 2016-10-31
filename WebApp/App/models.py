from django.db import models


class Update(models.Model):

    log_name = models.CharField(40)
    log_update = models.DecimalField()

