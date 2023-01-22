import datetime

from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=200)
    klasse = models.IntegerField()
    # klassen_schlüssel = models.CharField(max_length=8)
    schule = models.CharField(max_length=200)
    heft_nr = models.IntegerField()
    mail = models.EmailField()
    pub_date = models.DateTimeField(auto_now_add=True)
