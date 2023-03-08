from django.utils import timezone

from mathesdigi_app.models import User, Ergebnisse, Wertung, Aufgaben, Teilaufgaben
from datetime import datetime


class Evaluate:
    def __init__(self, user: User):
        self.user = user
        self.summed_points = Ergebnisse.objects.filter(user_id=self.user.id, wertung=True).count()
        self.t_wert, self.prozentrang = self.translate_rohwert()
        self.performance_evaluation, self.performance_color = self.get_performance_evaluation()

    def translate_rohwert(self):
        user_pub_date = self.user.pub_date.date()
        comparable_date = timezone.make_aware(datetime(2000, user_pub_date.month, user_pub_date.day))
        wertung_time_period = Wertung.objects.filter(start_time__lte=comparable_date, end_time__gte=comparable_date)
        wertung = wertung_time_period.get(rohwert=self.summed_points)
        return wertung.t_wert, wertung.prozentrang

    def get_performance_evaluation(self):
        if self.prozentrang < 10:
            return "weit unterdurchschnittlich", "red"
        if self.prozentrang <= 25:
            return "unterdurchschnittlich", "orange"
        if self.prozentrang <= 75:
            return "durchschnittlich", "forestgreen"
        if self.prozentrang <= 90:
            return "überdurchschnittlich", "mediumblue"
        if self.prozentrang <= 100:
            return "weit überdurchschnittlich", "mediumpurple"

    def create_evaluation_context(self):
        aufgaben_list, summed_task_points = self.create_aufgaben_list()
        teilaufgaben_ergebnis_list = self.create_teilaufgaben_ergebnis_list()

        context = {'teilaufgaben': teilaufgaben_ergebnis_list,
                   'aufgaben': aufgaben_list,
                   'summed_task_points': summed_task_points,
                   'name': str(self.user.user_name),
                   'pub_date': f"{self.user.pub_date.day}.{self.user.pub_date.month}.{self.user.pub_date.year}",
                   'rohwert': self.summed_points,
                   'prozentrang': self.prozentrang,
                   'negativ_prozentrang': 100 - self.prozentrang,
                   't_wert': self.t_wert,
                   'leistungseinschätzung': self.performance_evaluation,
                   'performance_color': self.performance_color}
        return context

    def send_evaluation(self):
        # Alles an Lehrer per Mail schicken
        pass

    def save_results_for_statistic(self):
        # Die Ergebnisse speichern für die Erstellung neuer Auswertungszeiträume
        pass

    def delete_user_data(self):
        self.save_results_for_statistic()
        # Löschen des Users und aller Ergebnisse des Users
        pass

    def create_teilaufgaben_ergebnis_list(self):
        teilaufgaben_ergebnis_list = []
        for teilaufgabe in Teilaufgaben.objects.filter(aufgabe__heft_nr=2):
            try:
                ergebnis = Ergebnisse.objects.get(teilaufgabe=teilaufgabe, user=self.user)
            except Ergebnisse.DoesNotExist:
                ergebnis = None

            teilaufgaben_ergebnis_list.append(
                {
                    "beschreibung": teilaufgabe.aufgabe.bezeichnung,
                    "aufgabe": teilaufgabe.beschreibung,
                    "wert": ergebnis.eingabe if ergebnis else "Keine Eingabe vorhanden",
                    "bewertung": "Richtig" if ergebnis and ergebnis.wertung else "Falsch",
                    "bearbeitungszeit": ergebnis.time_required if ergebnis else 0
                })
        return teilaufgaben_ergebnis_list

    def create_aufgaben_list(self):
        heft_nr = self.user.heft
        aufgaben = Aufgaben.objects.filter(heft_nr=2).all()
        aufgaben_list = []
        for aufgabe in aufgaben:
            aufgaben_points = Ergebnisse.objects.filter(user=self.user, teilaufgabe__aufgabe=aufgabe, wertung=True).count()
            aufgaben_list.append({
                "aufgaben_nr": aufgabe.aufgaben_nr,
                "bezeichnung": aufgabe.bezeichnung,
                "punkte": aufgaben_points,
                "punktzahl": aufgabe.punktzahl
            })
        summed_task_points = sum(aufgabe.punktzahl for aufgabe in aufgaben)
        return aufgaben_list, summed_task_points
