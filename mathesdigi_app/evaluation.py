from mathesdigi_app.models import User, Ergebnisse, Wertung


class Evaluate:
    def __init__(self, user: User):
        self.user = user
        self.summed_points = Ergebnisse.objects.filter(user_id=self.user.id, wertung=True).count()
        self.evaluate()

    def evaluate(self):
        print(f"{self.user.pub_date.date().day}.{self.user.pub_date.date().month}")
        user_day = self.user.pub_date.date().day
        user_month = self.user.pub_date.date().month
        wertung_time_period = Wertung.objects.filter(start_day__lt=user_day,
                                                     start_month__lte=user_month, end_month__gte=user_month)
        wertung = wertung_time_period.get(rohwert=self.summed_points)
        print(wertung.rohwert, wertung.t_wert, wertung.prozentrang)
        # In Wertung schauen was dem Rohwert entspricht
        # Leistungseinschätzung machen (siehe Excel)
        pass

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
