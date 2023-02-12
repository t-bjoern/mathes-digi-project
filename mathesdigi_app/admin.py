import datetime

import pandas as pd

from django.contrib import admin
from django import forms
from django.shortcuts import redirect, render
from django.urls import path

from . import helpers
from .models import User, Aufgaben, Teilaufgaben, Ergebnisse, Wertung


@admin.register(Teilaufgaben)
class TeilaufgabenAdmin(admin.ModelAdmin):
    list_display = ('teilaufgaben_id', 'loesung')


@admin.register(Aufgaben)
class AufgabenAdmin(admin.ModelAdmin):
    list_display = ('heft_nr', 'aufgaben_nr', 'bezeichnung', 'punktzahl')


@admin.register(Ergebnisse)
class ErgebnisseAdmin(admin.ModelAdmin):
    list_display = ('user', 'teilaufgaben_name', 'eingabe', 'wertung')

    def teilaufgaben_name(self, obj):
        return obj.teilaufgabe.teilaufgaben_id

    teilaufgaben_name.short_description = 'Teilaufgaben ID'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'mail', 'pub_date', 'heft')


class CsvImportForm(forms.Form):
    heft_nr = forms.IntegerField()
    start_time = forms.CharField()
    end_time = forms.CharField()
    file = forms.FileField()


@admin.register(Wertung)
class WertungAdmin(admin.ModelAdmin):
    month_names = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober",
                   "November", "Dezember"]
    list_display = ('heft_nr', 'zeitraum', 'rohwert', 't_wert', 'prozentrang')

    def zeitraum(self, obj):
        return f"{obj.start_day}.{self.month_names[obj.start_month - 1]} - " \
               f"{obj.end_day}.{self.month_names[obj.end_month - 1]} "

    change_list_template = "entities/changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        form = CsvImportForm()
        context = {"form": form}
        if request.method == "POST":
            file = request.FILES["file"]
            df, error_message = helpers.read_and_validate_file(file)
            if df is not None:
                try:
                    start_day, start_month = request.POST["start_time"].split(".")
                    end_day, end_month = request.POST["end_time"].split(".")
                    result = df.apply(helpers.create_or_update_wertung_apply,
                                      args=(request.POST["heft_nr"], start_month, start_day, end_month, end_day), axis=1)
                    updated = result.apply(lambda x: x[0]).sum()
                    created = result.apply(lambda x: x[1]).sum()
                    self.message_user(request, f"Your file has been imported. Updated: {updated} Created: {created}")
                    return redirect("..")
                except ValueError:
                    error_message.append("Datum ist im falschen Format. Bitte im Format dd.mm angeben. Beispiel: 01.02")
                except Exception as e:
                    error_message.append(str(e))
            if error_message:
                form = CsvImportForm(initial={'heft_nr': request.POST.get('heft_nr'),
                                              'start_time': request.POST.get('start_time'),
                                              'end_time': request.POST.get('end_time'),
                                              'file': request.POST.get('file')})
                context = {'form': form, "error_message": error_message}
        return render(request, "admin/csv_form.html", context)
