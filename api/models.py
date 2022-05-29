from django.db import models


class Date(models.Model):
    month = models.CharField(max_length=20, default="")
    day = models.IntegerField()
    fact = models.CharField(max_length=256, default="")
    popularity = models.IntegerField(default=0)

    class Meta:
        unique_together = ("month", "day")
