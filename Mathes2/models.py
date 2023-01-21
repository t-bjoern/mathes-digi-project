import datetime

from django.db import models


class User(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=200)
    klasse = models.IntegerField()
    schule = models.CharField(max_length=200)
    lehrer_mail = models.EmailField()
    pseudonym = models.CharField(max_length=100)
    jahrgang = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
