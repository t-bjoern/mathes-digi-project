import datetime
import time
import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from mathesdigi_app import helpers
from mathesdigi_app.models import User, Aufgaben, Teilaufgaben, Ergebnisse


@pytest.mark.django_db
def test_create_random_user_id():
    num_create_users = 10000
    for i in range(num_create_users):
        id = helpers.create_random_user_id()
        User.objects.create(id=id, user_name="Test", mail="test@mail.de")
    assert User.objects.count() == num_create_users


@pytest.mark.django_db
@pytest.mark.parametrize("pub_date, count_user", [
    (timezone.now() - timezone.timedelta(days=10), 0),
    (timezone.now() + timezone.timedelta(days=10), 0),
    (timezone.now(), 1)
])
def test_delete_old_user(pub_date, count_user):
    user = User.objects.create(user_name="Test_User", mail="test@mail.de")
    user.pub_date = pub_date
    user.save()
    helpers.delete_old_users()
    assert User.objects.count() == count_user


@pytest.mark.django_db
def test_save_answer():
    user = User.objects.create(id=123, user_name='Test_User', mail="test@mail.de")
    aufgabe = Aufgaben.objects.create(heft_nr=2, aufgaben_nr=1, bezeichnung="Zählen", punktzahl=2)
    teilaufgabe = Teilaufgaben.objects.create(teilaufgaben_id="2A1A", aufgabe=aufgabe)
    helpers.save_answer(teilaufgaben_id=teilaufgabe.teilaufgaben_id, ergebnis="23", user_id=user.id, time_required=8)
    assert Ergebnisse.objects.count() == 1
    assert Ergebnisse.objects.get(user_id=user.id, teilaufgabe=teilaufgabe).eingabe == "23"
    # Update Ergbenisse object
    helpers.save_answer(teilaufgaben_id=teilaufgabe.teilaufgaben_id, ergebnis="20", user_id=user.id, time_required=8)
    assert Ergebnisse.objects.count() == 1
    assert Ergebnisse.objects.get(user_id=user.id, teilaufgabe=teilaufgabe).eingabe == "20"


@pytest.mark.django_db
@pytest.mark.parametrize("user_name, mail", [
    ("", "test@mail.de"),
    ("Test_User", ""),
])
def test_validate_registration_create_or_update_user_invalid_registration_no_user(user_name, mail):
    registration_data = {"user_name": user_name, "mail": mail}
    with pytest.raises(ValidationError) as excinfo:
        helpers.validate_registration_create_or_update_user(registration_data)
    assert str(excinfo.value) == "['Bitte überprüfen Sie die Eingabe. Die Felder dürfen nicht leer sein!']"
    assert User.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize("user_name, mail", [
    ("Test_User", "test@mail.de"),
])
def test_validate_registration_create_or_update_user_valid_registration_no_user(user_name, mail):
    registration_data = {"user_name": user_name, "mail": mail}
    helpers.validate_registration_create_or_update_user(registration_data)
    assert User.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize("user_name, mail", [
    ("Test_User", "test@mail.de"),
])
def test_validate_registration_create_or_update_user_valid_registration_user(user_name, mail):
    user_old = User.objects.create(user_name="Test_User_old", mail="test@mail.de_old")
    registration_data = {"user_name": user_name, "mail": mail}
    helpers.validate_registration_create_or_update_user(registration_data, user_old.id)
    user_new = User.objects.get(id=user_old.id)
    assert user_new.user_name == user_name
    assert user_new.mail == mail


@pytest.mark.django_db
@pytest.mark.parametrize("template_name, teilaufgaben_id, output_context, is_solution", [
    ("1_task_A", "2A1A", {'2A1A': '1'}, True),
    ("1_task_B", "2A1B", {}, False),
    ("4_task_D", "2A4D", {}, False)
])
def test_get_previous_solution(template_name, teilaufgaben_id, output_context, is_solution):
    user = User.objects.create(id=123, user_name='Test_User', mail="test@mail.de")
    aufgabe = Aufgaben.objects.create(heft_nr=2, aufgaben_nr=1, bezeichnung="Zählen", punktzahl=2)
    teilaufgabe = Teilaufgaben.objects.create(teilaufgaben_id=teilaufgaben_id, aufgabe=aufgabe)
    if is_solution:
        Ergebnisse.objects.create(teilaufgabe=teilaufgabe, user=user, eingabe='1', wertung=True)
    context = helpers.get_previous_solution(heft="Mathes2", direct_to_task_name=template_name, user_id=user.id, context={})
    assert context == output_context



# def create_or_update_wertung_apply(row, heft_nr, start_month, start_day, end_month, end_day)
# def read_and_validate_file(file, max_file_size=1048576)
# def preprocess_request_post_data(post_data: dict)