from mathesdigi_app.models import User


class Evaluate:
    def __init__(self, user: User):
        self.user_mail = user.mail
        self.evaluate()

    def evaluate(self):
        # Ergebnisse des Users aus DB abrufen und aufsummieren (count True values)
        # In Wertung schauen was dem Rohwert entspricht
        # Leistungseinschätzung machen (siehe Excel)
        pass

    def send_evaluation(self):
        # Dann alles an Lehrer per Mail schicken
        pass

    def save_evaluation_for_statistic(self):
        # Die Ergebnisse speichern für die Erstellung neuer Auswertungszeiträume
        pass


