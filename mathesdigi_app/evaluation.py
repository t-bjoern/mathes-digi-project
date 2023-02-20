from mathesdigi_app.models import User


class Evaluate:
    def __init__(self, user: User):
        self.summed_points = None
        self.sum_points()
        self.user = user
        self.evaluate()

    def sum_points(self):
        self.summed_points = 0
        # Ergebnisse des Users aus DB abrufen, aufsummieren (count True values) und in user speichern.
        pass

    def evaluate(self):
        # In Wertung schauen was dem Rohwert entspricht
        # Leistungseinschätzung machen (siehe Excel)
        pass

    def send_evaluation(self):
        # Alles an Lehrer per Mail schicken
        pass

    def save_evaluation_for_statistic(self):
        # Die Ergebnisse speichern für die Erstellung neuer Auswertungszeiträume
        pass
