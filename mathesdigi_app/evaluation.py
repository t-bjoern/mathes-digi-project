from django.utils import timezone

from mathesdigi_app.models import User, Ergebnisse, Wertung
from datetime import datetime


class Evaluate:
    def __init__(self, user: User):
        self.user = user
        self.summed_points = Ergebnisse.objects.filter(user_id=self.user.id, wertung=True).count()
        self.t_wert, self.prozentrang = self.translate_rohwert()
        self.performance_evaluation = self.get_performance_evaluation()
        print(self.summed_points, self.t_wert, self.prozentrang, self.performance_evaluation)

    def translate_rohwert(self):
        user_pub_date = self.user.pub_date.date()
        comparable_date = timezone.make_aware(datetime(2000, user_pub_date.month, user_pub_date.day))
        wertung_time_period = Wertung.objects.filter(start_time__lte=comparable_date, end_time__gte=comparable_date)
        wertung = wertung_time_period.get(rohwert=self.summed_points)
        return wertung.t_wert, wertung.prozentrang

    def get_performance_evaluation(self):
        if self.prozentrang < 10:
            return "weit unterdurchschnittlich"
        if self.prozentrang <= 25:
            return "unterdurchschnittlich"
        if self.prozentrang <= 75:
            return "durchschnittlich"
        if self.prozentrang <= 90:
            return "überdurchschnittlich"
        if self.prozentrang <= 100:
            return "weit überdurchschnittlich"

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
