import time
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
        teilaufgabe1 = Teilaufgaben.objects.create(teilaufgaben_id="2A1A", aufgabe=aufgabe)
        teilaufgabe2 = Teilaufgaben.objects.create(teilaufgaben_id="2A1B", aufgabe=aufgabe)
        teilaufgabe3 = Teilaufgaben.objects.create(teilaufgaben_id="2A1C", aufgabe=aufgabe)

        Ergebnisse.objects.create(teilaufgabe=teilaufgabe1, user=user, eingabe='1', wertung=True)
        Ergebnisse.objects.create(teilaufgabe=teilaufgabe2, user=user, eingabe='2', wertung=False)
        Ergebnisse.objects.create(teilaufgabe=teilaufgabe3, user=user, eingabe='3', wertung=True)

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


@pytest.mark.django_db
@pytest.mark.parametrize("prozentrang, performance_evaluation", [
    (9, ("weit unterdurchschnittlich", "red")),
    (25, ("unterdurchschnittlich", "orange")),
    (75, ("durchschnittlich", "forestgreen")),
    (90, ("überdurchschnittlich", "mediumblue")),
    (100, ("weit überdurchschnittlich", "mediumpurple")),
])
def test_get_performance_evaluation(setup_test_data, prozentrang, performance_evaluation):
    user = User.objects.get(id=123)
    eval_obj = Evaluate(user)
    eval_obj.prozentrang = prozentrang

    assert eval_obj.get_performance_evaluation() == performance_evaluation


@pytest.mark.django_db
def test_create_evaluation_context(setup_test_data):
    user = User.objects.get(id=123)
    eval_obj = Evaluate(user)
    assert eval_obj.create_evaluation_context() == {
        'teilaufgaben': [
            {'beschreibung': 'Zählen', 'aufgabe': 1, 'wert': '1', 'bewertung': 'Richtig', 'bearbeitungszeit': None},
            {'beschreibung': 'Zählen', 'aufgabe': 1, 'wert': '2', 'bewertung': 'Falsch', 'bearbeitungszeit': None},
            {'beschreibung': 'Zählen', 'aufgabe': 1, 'wert': '3', 'bewertung': 'Richtig', 'bearbeitungszeit': None}
        ],
        'aufgaben': [{'aufgaben_nr': 1, 'bezeichnung': 'Zählen', 'punkte': 2, 'punktzahl': 2}],
        'summed_task_points': 2,
        'name': 'Test_User',
        'pub_date': f"{datetime.now().day}.{datetime.now().month}.{datetime.now().year}",
        'rohwert': 2,
        'prozentrang': 50,
        'negativ_prozentrang': 50,
        't_wert': '3',
        'leistungseinschätzung': 'durchschnittlich', 'performance_color': 'forestgreen'
    }
