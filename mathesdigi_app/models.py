import datetime

from django.db import models
from django.utils import timezone


class User(models.Model):
    user_name = models.CharField(max_length=20, null=False, blank=False)
    # klassen_schlüssel = models.CharField(max_length=8)
    mail = models.EmailField(null=False, blank=False)
    pub_date = models.DateTimeField(default=datetime.datetime.now(tz=timezone.utc))
    heft = models.CharField(max_length=50)


class Aufgaben(models.Model):
    aufgaben_nr = models.IntegerField()
    heft_nr = models.IntegerField()
    bezeichnung = models.CharField(max_length=200)
    punktzahl = models.IntegerField()

    class Meta:
        verbose_name = "Aufgabe"
        verbose_name_plural = "Aufgaben"


class Teilaufgaben(models.Model):
    teilaufgaben_id = models.CharField(max_length=5)
    loesung = models.IntegerField()
    aufgabe = models.ForeignKey(Aufgaben, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Teilaufgabe"
        verbose_name_plural = "Teilaufgaben"


class Ergebnisse(models.Model):
    eingabe = models.CharField(max_length=200, null=True)
    wertung = models.BooleanField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    teilaufgabe = models.ForeignKey(Teilaufgaben, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ergebnis"
        verbose_name_plural = "Ergebnisse"


class Wertung(models.Model):
    heft_nr = models.IntegerField()
    rohwert = models.IntegerField()
    t_wert = models.CharField(max_length=4)
    prozentrang = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        verbose_name = "Wertung"
        verbose_name_plural = "Wertungen"

