from mathesdigi_app.models import User, Ergebnisse


class Evaluate:
    def __init__(self, user: User):
        self.user = user
        self.summed_points = Ergebnisse.objects.filter(user_id=self.user.id, wertung=True).count()
        self.evaluate()

    def evaluate(self):
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
