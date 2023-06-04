from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class BlockedUsers(models.Model):
    user = models.CharField(max_length=50)
    count = models.IntegerField(null=True)
    time = models.DateTimeField(null=True)