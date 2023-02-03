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
        error_message = []
        df = None
        form = CsvImportForm()
        context = {"form": form}
        if request.method == "POST":
            file = request.FILES["file"]
            try:
                df = pd.read_excel(file)
            except Exception as e:
                error_message.append(str(e))
                error_message.append("Try to read with csv reader!")
                try:
                    df = pd.read_csv(file)
                except Exception as e:
                    error_message.append(str(e))

            try:
                start_day, start_month = request.POST["start_time"].split(".")
                end_day, end_month = request.POST["end_time"].split(".")
                if df is not None:
                    def create_or_update_objects(row):
                        if Wertung.objects.filter(heft_nr=request.POST["heft_nr"],
                                                  start_month=start_month,
                                                  start_day=start_day,
                                                  end_month=end_month,
                                                  end_day=end_day,
                                                  rohwert=row["Rohwert"]).exists():
                            wertung = Wertung.objects.get(heft_nr=request.POST["heft_nr"],
                                                          start_month=start_month,
                                                          start_day=start_day,
                                                          end_month=end_month,
                                                          end_day=end_day,
                                                          rohwert=row["Rohwert"])
                            wertung.t_wert = row["T-Wert"]
                            wertung.prozentrang = row["Prozentrang"]
                            wertung.save()
                        else:
                            Wertung.objects.create(heft_nr=request.POST["heft_nr"],
                                                   start_month=start_month,
                                                   start_day=start_day,
                                                   end_month=end_month,
                                                   end_day=end_day,
                                                   rohwert=row["Rohwert"],
                                                   t_wert=row["T-Wert"],
                                                   prozentrang=row["Prozentrang"])

                    df.apply(create_or_update_objects, axis=1)
                    user_message = "Your file has been imported"
                    self.message_user(request, user_message)
                    return redirect("..")
            except ValueError:
                error_message.append("Datum ist im falschen Format. Bitte im Format dd.mm angeben. Beispiel: 01.02")
            except Exception as e:
                error_message.append(str(e))

            if error_message:
                heft_nr = request.POST.get('heft_nr')
                start_time = request.POST.get('start_time')
                end_time = request.POST.get('end_time')
                file = request.POST.get('file')
                form = CsvImportForm(initial={'heft_nr': heft_nr,
                                              'start_time': start_time,
                                              'end_time': end_time,
                                              'file': file})
                context = {'form': form, "error_message": error_message}
        return render(request, "admin/csv_form.html", context)


admin.site.register(Teilaufgaben, TeilaufgabenAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Aufgaben, AufgabenAdmin)
admin.site.register(Ergebnisse, ErgebnisseAdmin)
