from datetime import datetime
import os
import random
import re
import dns.resolver
from email.utils import parseaddr

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives

import pandas as pd
from django.utils import timezone

from .models import User, Teilaufgaben, Ergebnisse, Wertung
from bs4 import BeautifulSoup


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


def is_valid_email(email):
    # Überprüfen, ob das Format der E-Mail-Adresse korrekt ist
    try:
        addr = parseaddr(email)
        if not addr[1]:
            return False
    except:
        return False

    # Überprüfen, ob der Domain-Name existiert
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
    except:
        return False

    return True


def validate_registration_create_or_update_user(registration_data: dict, user_id=None):
    user_name = registration_data["user_name"].strip()
    mail = registration_data["mail"].strip()
    # Validierung der Eingabedaten
    if user_name == "" or mail == "":
        raise ValidationError("Bitte überprüfen Sie die Eingabe. Die Felder dürfen nicht leer sein!")
    if not is_valid_email(mail):
        raise ValidationError("Die eingegebene E-Mail ist ungültig!")
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


def delete_old_users():
    one_day_future = timezone.now() + timezone.timedelta(days=1)
    one_week_ago = timezone.now() - timezone.timedelta(days=7)
    old_and_future_users = User.objects.filter(pub_date__lt=one_week_ago) | \
                           User.objects.filter(pub_date__gt=one_day_future)
    old_and_future_users.delete()


def save_answer(teilaufgaben_id: str, ergebnis: str, user_id: int, time_required: int):
    teilaufgabe = Teilaufgaben.objects.get(teilaufgaben_id=teilaufgaben_id)

    if Ergebnisse.objects.filter(user_id=user_id, teilaufgabe=teilaufgabe).exists():
        ergebnis_obj = Ergebnisse.objects.get(user_id=user_id, teilaufgabe=teilaufgabe)
        ergebnis_obj.eingabe = ergebnis
        ergebnis_obj.wertung = bool(ergebnis == teilaufgabe.loesung)
        ergebnis_obj.time_required += time_required
        ergebnis_obj.save()
    else:
        Ergebnisse.objects.create(user_id=user_id,
                                  teilaufgabe=teilaufgabe,
                                  eingabe=ergebnis,
                                  wertung=bool(ergebnis == teilaufgabe.loesung),
                                  time_required=time_required)


def get_previous_solution(heft, direct_to_task_name, user_id, context):
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates', 'mathesdigi_app')
    template_path = os.path.join(templates_dir, heft, f'{direct_to_task_name}.html')
    with open(template_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        field_names = [field.get('name') for field in soup.find_all(['input', 'textarea'])
                       if re.match(r"^\d\w\d\w$", str(field.get('name')))]
    for field_name in field_names:
        teilaufgabe = Teilaufgaben.objects.get(teilaufgaben_id=field_name)
        if Ergebnisse.objects.filter(user_id=user_id, teilaufgabe=teilaufgabe).exists():
            previous_solution = Ergebnisse.objects.get(user_id=user_id, teilaufgabe=teilaufgabe)
            context.update({field_name: previous_solution.eingabe})
    return context


def create_or_update_wertung_apply(row, heft_nr, start_month, start_day, end_month, end_day):
    updated, created = 0, 0
    start_time = timezone.make_aware(datetime(day=start_day, month=start_month, year=2000))
    end_time = timezone.make_aware(datetime(day=end_day, month=end_month, year=2000))
    wertung_exists = Wertung.objects.filter(heft_nr=heft_nr,
                                            start_time=start_time,
                                            end_time=end_time,
                                            rohwert=row["Rohwert"]).exists()
    if wertung_exists:
        wertung = Wertung.objects.get(heft_nr=heft_nr,
                                      start_time=start_time,
                                      end_time=end_time,
                                      rohwert=row["Rohwert"])
        wertung.t_wert = row["T-Wert"]
        wertung.prozentrang = row["Prozentrang"]
        wertung.save()
        updated += 1
    else:
        Wertung.objects.create(heft_nr=heft_nr,
                               start_time=start_time,
                               end_time=end_time,
                               rohwert=row["Rohwert"],
                               t_wert=row["T-Wert"],
                               prozentrang=row["Prozentrang"])
        created += 1
    return updated, created


def read_and_validate_file(file, max_file_size=1048576):
    error_message = []
    ext = os.path.splitext(str(file))[-1].lower()
    if ext not in ['.csv', '.xls', '.xlsx']:
        error_message.append("File is not in the correct format. You can only upload Excel or CSV files.")
        return None, error_message
    file.seek(0, 2)  # move the cursor to the end of the file to get its size
    file_size = file.tell()
    if file_size > max_file_size:
        error_message.append("File size exceeds the limit of {} MB".format(max_file_size / 1024 / 1024))
        return None, error_message
    file.seek(0)  # move the cursor back to the beginning of the file
    try:
        df = pd.read_excel(file)
    except Exception as e:
        error_message.append("No excel file try to read with csv reader!")
        try:
            df = pd.read_csv(file)
        except Exception as e:
            error_message.append(str(e))
    if "df" not in locals():
        return None, error_message

    if not all(col in df.columns for col in ["Rohwert", "T-Wert", "Prozentrang"]):
        error_message.append(
            "Table format is incorrect. Rohwert, T-Wert, and Prozentrang must be in the header.")
        return None, error_message
    if len(df.columns) != 3:
        error_message.append(
            "Table format is incorrect. The table contains too many columns.")
        return None, error_message
    return df, error_message


def preprocess_request_post_data(post_data: dict):
    # Convert lists in dict to single values
    post_data = {key: value[0] for key, value in post_data.items()}
    # Delete unnecessary information in post_data
    del post_data["csrfmiddlewaretoken"]
    teilaufgaben_ids = [key for key in post_data.keys() if re.match(r"^\d\w\d\w$", key)]
    this_task_process = post_data.get("this_task_process")
    return post_data, teilaufgaben_ids, this_task_process


def send_email(from_email, to_email, subject, context):
    template = get_template('evaluation_template.html')
    html_content = render_to_string(template, context)
    text_content = 'Dies ist eine Beispiel-E-Mail, die mit einem HTML-Template erstellt wurde.'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
