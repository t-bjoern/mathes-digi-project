import datetime

from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=20, null=False, blank=False)
    # klasse = models.IntegerField()
    # klassen_schlüssel = models.CharField(max_length=8)
    # schule = models.CharField(max_length=200)
    mail = models.EmailField(null=False, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)
