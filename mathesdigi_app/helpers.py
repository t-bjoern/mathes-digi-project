import random

from .models import User, Teilaufgaben, Ergebnisse


def save_answer(post_data: dict, user_id: int, context: dict):
    if any(a != [""] for a in post_data.values()):
        for key, value in post_data.items():
            teilaufgaben_id = key
            ergebnis = int(value[0])
            teilaufgabe = Teilaufgaben.objects.get(teilaufgaben_id=teilaufgaben_id)

            if Ergebnisse.objects.filter(user_id=user_id, teilaufgabe=teilaufgabe).exists():
                ergebnis_obj = Ergebnisse.objects.get(user_id=user_id, teilaufgabe=teilaufgabe)
                ergebnis_obj.eingabe = ergebnis
                ergebnis_obj.wertung = bool(ergebnis == teilaufgabe.loesung)
                ergebnis_obj.save()
            else:
                Ergebnisse.objects.create(user_id=user_id,
                                          teilaufgabe=teilaufgabe,
                                          eingabe=ergebnis,
                                          wertung=bool(ergebnis == teilaufgabe.loesung))
        # return redirect(heft2_task1_2)
    else:
        context["empty_field"] = True

    return context


def display_solution_example(post_data: dict):
    context = {}
    for key, value in post_data.items():
        teilaufgaben_id = key
        ergebnis = int(value[0])
        teilaufgabe = Teilaufgaben.objects.get(teilaufgaben_id=teilaufgaben_id)
        if ergebnis != teilaufgabe.loesung:
            context[f"{key}_solution"] = teilaufgabe.loesung
        context[f"{key}_value"] = ergebnis

    return context


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
