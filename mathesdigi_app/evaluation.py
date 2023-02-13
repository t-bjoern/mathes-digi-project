from mathesdigi_app.models import User


class Evaluate:
    def __init__(self, user: User):
        self.user = user

    def evaluate(self):
        # Ergebnisse des Users aus DB abrufen und aufsummieren (count True values)
        # In Wertung schauen was dem Rohwert entspricht
        # Leistungseinschätzung machen (siehe Excel)
        # Dann alles an Lehrer per Mail schicken
        print("Function called with parameters:", self.user)


