import random

from .models import User, Aufgaben, Teilaufgaben, Ergebnisse


def display_solution_example(post_data: dict):
    for key in post_data.keys():
        teilaufgaben_id = key
        teilaufgabe = Teilaufgaben.objects.get(teilaufgaben_id=teilaufgaben_id)
        post_data[key] = teilaufgabe.loesung

    return post_data


def check_answer_example(post_data: dict):
    dicti = {}
    for key, value in post_data.items():
        teilaufgaben_id = key
        ergebnis = int(value[0])

        teilaufgabe = Teilaufgaben.objects.get(teilaufgaben_id=teilaufgaben_id)
        if ergebnis == teilaufgabe.loesung:
            wert = "Richtig"
        else:
            wert = "Falsch"

        dicti[teilaufgaben_id] = wert

    return dicti


def create_random_user_id():
    """
    Erstellen einer zufälligen user_id welche noch nicht in der Datenbank verwendet wird.
    Returns:
        user_id: int
    """
    while True:
        user_id = random.randint(10000, 99999)
        if not User.objects.filter(id=user_id).exists():
            break
    return user_id


def validate_registration_create_user(registration_data: dict):
    user_name = registration_data["user_name"].strip()
    mail = registration_data["mail"].strip()

    # Validierung der Eingabedaten
    if user_name == "" or mail == "":
        raise Exception("Bitte überprüfen Sie die Eingabe. Die Felder dürfen nicht leer sein!")

    user = User.objects.create(id=create_random_user_id(),
                               user_name=user_name,
                               mail=mail)
    return user
