import datetime

from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=20, null=False, blank=False)
    # klassen_schlüssel = models.CharField(max_length=8)
    mail = models.EmailField(null=False, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    heft = models.CharField(max_length=50)


class Aufgaben(models.Model):
    aufgaben_nr = models.IntegerField()
    heft_nr = models.IntegerField()
    bezeichnung = models.CharField(max_length=200)
    punktzahl = models.IntegerField()


class Teilaufgaben(models.Model):
    teilaufgaben_id = models.CharField(max_length=5)
    loesung = models.IntegerField()
    aufgabe = models.ForeignKey(Aufgaben, on_delete=models.CASCADE)


class Ergebnisse(models.Model):
    eingabe = models.CharField(max_length=200, null=True)
    wertung = models.BooleanField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    teilaufgabe = models.ForeignKey(Teilaufgaben, on_delete=models.CASCADE)
