from django.contrib import admin
from .models import User, Aufgaben, Teilaufgaben, Ergebnisse

admin.site.register(User)
admin.site.register(Aufgaben)
admin.site.register(Teilaufgaben)
admin.site.register(Ergebnisse)