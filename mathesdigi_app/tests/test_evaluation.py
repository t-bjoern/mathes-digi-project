from datetime import timedelta

import pytest
from django.utils import timezone
from django.utils.datetime_safe import datetime

from mathesdigi_app.evaluation import Evaluate
from mathesdigi_app.models import User, Ergebnisse, Wertung, Teilaufgaben, Aufgaben


@pytest.fixture(scope="function")
def setup_test_data(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = User.objects.create(id=123, user_name='Test_User', mail="test@mail.de")
        aufgabe = Aufgaben.objects.create(heft_nr=2, aufgaben_nr=1, bezeichnung="Zählen", punktzahl=2)
        teilaufgabe = Teilaufgaben.objects.create(teilaufgaben_id="2A1A", aufgabe=aufgabe)

        Ergebnisse.objects.create(teilaufgabe=teilaufgabe, user=user, eingabe='1', wertung=True)
        Ergebnisse.objects.create(teilaufgabe=teilaufgabe, user=user, eingabe='2', wertung=False)
        Ergebnisse.objects.create(teilaufgabe=teilaufgabe, user=user, eingabe='3', wertung=True)

        # Create a Wertung object that covers the current date
        today = timezone.now().date()
        comparable_date = timezone.make_aware(datetime(2000, today.month, today.day))
        Wertung.objects.create(heft_nr=2, rohwert=2, t_wert="3", prozentrang=50, start_time=comparable_date,
                               end_time=comparable_date+timedelta(days=2))
    yield


@pytest.mark.django_db
def test_translate_rohwert(setup_test_data):
    user = User.objects.get(id=123)
    eval_obj = Evaluate(user)

    assert eval_obj.t_wert == "3"
    assert eval_obj.prozentrang == 50

# def get_performance_evaluation(self):
# def create_evaluation_context(self):
# def create_teilaufgaben_ergebnis_list(self):
# def create_aufgaben_list(self):
