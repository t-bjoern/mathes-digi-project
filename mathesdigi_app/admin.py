import datetime

import pandas as pd

from django.contrib import admin
from django import forms
from django.shortcuts import redirect, render
from django.urls import path

from .models import User, Aufgaben, Teilaufgaben, Ergebnisse, Wertung


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


class CsvImportForm(forms.Form):
    heft_nr = forms.IntegerField()
    start_month = forms.CharField()
    end_month = forms.CharField()
    csv_file = forms.FileField()


@admin.register(Wertung)
class WertungAdmin(admin.ModelAdmin):
    month_names = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober",
                   "November", "Dezember"]
    list_display = ('heft_nr', 'zeitraum', 'rohwert', 't_wert', 'prozentrang')

    def zeitraum(self, obj):
        return f"{self.month_names[obj.start_month-1]} - {self.month_names[obj.end_month-1]}"

    change_list_template = "entities/changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            df = pd.read_excel(csv_file)

            def create_objects(row):
                start_month_number = self.month_names.index(request.POST["start_month"]) + 1
                end_month_number = self.month_names.index(request.POST["end_month"]) + 1
                Wertung.objects.get_or_create(heft_nr=request.POST["heft_nr"],
                                              start_month=start_month_number,
                                              end_month=end_month_number,
                                              rohwert=row["Rohwert"],
                                              t_wert=row["T-Wert"],
                                              prozentrang=row["Prozentrang"])

            df.apply(create_objects, axis=1)

            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )


admin.site.register(Teilaufgaben, TeilaufgabenAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Aufgaben, AufgabenAdmin)
admin.site.register(Ergebnisse, ErgebnisseAdmin)
