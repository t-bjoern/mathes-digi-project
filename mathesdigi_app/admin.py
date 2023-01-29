from django.contrib import admin
from .models import User, Aufgaben, Teilaufgaben, Ergebnisse


class TeilaufgabenAdmin(admin.ModelAdmin):
    list_display = ('teilaufgaben_id', 'loesung')


class AufgabenAdmin(admin.ModelAdmin):
    list_display = ('heft_nr', 'aufgaben_nr', 'bezeichnung', 'punktzahl')


class ErgebnisseAdmin(admin.ModelAdmin):
    list_display = ('user', 'teilaufgaben_name', 'eingabe', 'wertung')

    def teilaufgaben_name(self, obj):
        return obj.teilaufgabe.teilaufgaben_id
    teilaufgaben_name.short_description = 'Teilaufgaben ID'


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'mail', 'pub_date', 'heft')


admin.site.register(Teilaufgaben, TeilaufgabenAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Aufgaben, AufgabenAdmin)
admin.site.register(Ergebnisse, ErgebnisseAdmin)