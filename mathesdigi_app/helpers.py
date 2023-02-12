import random
from django.core.exceptions import ValidationError

import pandas as pd

from .models import User, Teilaufgaben, Ergebnisse, Wertung


def save_answer(teilaufgaben_id: str, ergebnis: int, user_id: int):
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


def get_example_solution(teilaufgaben_id: str):
    teilaufgabe = Teilaufgaben.objects.get(teilaufgaben_id=teilaufgaben_id)
    context = {teilaufgaben_id: teilaufgabe.loesung}

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


def validate_registration_create_or_update_user(registration_data: dict, user_id=None):
    user_name = registration_data["user_name"].strip()
    mail = registration_data["mail"].strip()

    # Validierung der Eingabedaten
    if user_name == "" or mail == "":
        raise ValidationError("Bitte überprüfen Sie die Eingabe. Die Felder dürfen nicht leer sein!")

    user, created = User.objects.get_or_create(id=user_id, defaults={
        "user_name": user_name,
        "mail": mail,
        "id": create_random_user_id()
    })

    if not created:
        user.user_name = user_name
        user.mail = mail
        user.save()

    return user


def validate_registration_update_user(registration_data: dict, user_id: int):
    user_name = registration_data["user_name"].strip()
    mail = registration_data["mail"].strip()

    return None


def create_or_update_wertung_object(row, heft_nr, start_month, start_day, end_month, end_day):
    if Wertung.objects.filter(heft_nr=heft_nr,
                              start_month=start_month,
                              start_day=start_day,
                              end_month=end_month,
                              end_day=end_day,
                              rohwert=row["Rohwert"]).exists():
        wertung = Wertung.objects.get(heft_nr=heft_nr,
                                      start_month=start_month,
                                      start_day=start_day,
                                      end_month=end_month,
                                      end_day=end_day,
                                      rohwert=row["Rohwert"])
        wertung.t_wert = row["T-Wert"]
        wertung.prozentrang = row["Prozentrang"]
        wertung.save()
    else:
        Wertung.objects.create(heft_nr=heft_nr,
                               start_month=start_month,
                               start_day=start_day,
                               end_month=end_month,
                               end_day=end_day,
                               rohwert=row["Rohwert"],
                               t_wert=row["T-Wert"],
                               prozentrang=row["Prozentrang"])


def read_and_validate_file(file):
    df = None
    error_message = []
    # TODO Dateigröße prüfen, um Server nicht zu überlasten
    try:
        df = pd.read_excel(file)
    except Exception as e:
        error_message.append(str(e))
        error_message.append("Try to read with csv reader!")
        try:
            df = pd.read_csv(file)
        except Exception as e:
            error_message.append(str(e))

    if "Rohwert" not in df.columns or "T-Wert" not in df.columns or "Prozentrang" not in df.columns:
        error_message.append(
            "Tabelle ist im falschen Format. Rohwert, T-Wert und Prozentrang müssen im Tabellenkopf sein.")
    if len(df.columns) != 3:
        error_message.append(
            "Tabelle ist im falschen Format. Tabelle enthällt zu viele Spalten")

    return df, error_message


def str2bool(string: str):
    return string.lower() in ("yes", "true", "t", "1")
