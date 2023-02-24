import time

import pytest

from mathesdigi_app.models import User, Aufgaben, Teilaufgaben, Ergebnisse
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from mathesdigi_app.views import registration


@pytest.fixture(scope="function")
def setup_test_data(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        aufgabe = Aufgaben.objects.create(aufgaben_nr=1, heft_nr=2, bezeichnung="Zählen", punktzahl=2)
        Teilaufgaben.objects.create(teilaufgaben_id="2A1A", loesung=23, aufgabe=aufgabe)
        User.objects.create(id=123, user_name="Test", mail="test@mail.de", heft="Mathes2")
    yield


@pytest.mark.django_db
@pytest.mark.parametrize("user_name, user_mail, count_user, error", [
    ("test_user", "test@mail.de", 1, False),
    ("", "test@mail.de", 0, True),
    (" test_user  ", "test@mail.de", 1, False),
])
def test_registration_view(user_name, user_mail, count_user, error):
    # Erstellen Sie eine Test-Request-Instanz
    request = RequestFactory().post(reverse('registration'))
    # Fügen Sie die Middleware hinzu, um Sitzungsdaten zu simulieren
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session['heft'] = 'Mathes2'
    request.POST = {'csrfmiddlewaretoken': ['sRsPS74ilPwQ6PbsDBvXOqSJ5UPBAGhg7Cd61PboqJ8bRUBN5w1wEc3ZUjuqe0ll'],
                    'user_name': [user_name],
                    'mail': [user_mail]}
    response = registration(request)

    if not error:
        user = User.objects.get(user_name=user_name.strip(),
                                mail=user_mail.strip())
        assert user
    assert User.objects.count() == count_user
    assert bool("Bitte überprüfen Sie die Eingabe. Die Felder dürfen nicht leer sein!" \
                in str(response.content, "utf-8")) == error


class TestMainView:
    @pytest.mark.django_db
    def test_main_view_redirects_to_startpage_if_no_user_in_session(self, client):
        response = client.get(reverse('main_view', kwargs={'heft': 'Mathes2', 'direct_to_task_name': '1_task_A'}))
        assert response.status_code == 302
        assert response.url == reverse('startpage')

    @pytest.mark.django_db
    def test_main_view_renders_template_for_get_request(self, client, monkeypatch, setup_test_data):
        teilaufgabe = Teilaufgaben.objects.get(teilaufgaben_id="2A1A")
        Ergebnisse.objects.create(user_id=123, teilaufgabe=teilaufgabe, eingabe="23")
        session = client.session
        session['user'] = 123
        session.save()
        response = client.get(reverse('main_view', kwargs={'heft': 'Mathes2', 'direct_to_task_name': '1_task_A'}))
        assert response.status_code == 200
        assert 'mathesdigi_app/Mathes2/1_task_A.html' in [t.name for t in response.templates]
        # Tests if a possible solution is displayed on a page. (helpers.get_previous_solution())
        assert response.context['2A1A'] == "23"

    @pytest.mark.django_db
    def test_main_view_processes_post_request(self, client, monkeypatch, setup_test_data):
        session = client.session
        session['user'] = 123
        session['start_time'] = time.time()
        session.save()
        data = {'csrfmiddlewaretoken': ['Ixcpy0dqU5jngCh7EsNCIFGQefxkdBKLniXGHIkwZZVI1HHs6njbyrR63Ec9RVOQ'],
                'this_task_process': ['task_normal'],
                '2A1A': ['23']}
        response = client.post(reverse('main_view', kwargs={'heft': 'Mathes2', 'direct_to_task_name': '1_task_A'}),
                               data=data)
        assert response.status_code == 200
        assert Ergebnisse.objects.count() == 1
        assert Ergebnisse.objects.get(user_id=123, teilaufgabe__teilaufgaben_id="2A1A").eingabe == "23"

    @pytest.mark.django_db
    def test_main_view_sets_start_time_in_session(self, client, monkeypatch, setup_test_data):
        session = client.session
        session['user'] = 123
        session.save()
        response = client.get(reverse('main_view', kwargs={'heft': 'Mathes2', 'direct_to_task_name': '1_task_A'}))
        assert response.status_code == 200
        assert 'start_time' in client.session
        assert (time.time() - client.session["start_time"]) <= 1


class TestCheckUserData:
    @pytest.mark.django_db
    def test_check_user_data_view_with_valid_user(self, client, setup_test_data):
        session = client.session
        session['user'] = 123
        session.save()
        url = reverse('check_user_data')
        response = client.get(url)
        assert response.status_code == 200
        assert 'mathesdigi_app/check_user_data.html' in [t.name for t in response.templates]
        assert response.context['user_name'] == "Test"
        assert response.context['mail'] == "test@mail.de"
        assert response.context['heft'] == "Mathes2"

    @pytest.mark.django_db
    def test_check_user_data_view_with_invalid_user(self, client):
        session = client.session
        session['user'] = 999
        session.save()
        url = reverse('check_user_data')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == reverse('startpage')


class TestChangeUserData:
    @pytest.mark.django_db
    def test_change_user_data_updates_user_information(self, client, setup_test_data):
        session = client.session
        session["user"] = 123
        session.save()
        data = {"user_name": "New Name", "mail": "new_email@example.com", "heft": "Mathes2"}
        response = client.post(reverse("change_user_data"), data)
        updated_user = User.objects.get(id=123)
        assert updated_user.user_name == "New Name"
        assert updated_user.mail == "new_email@example.com"
        assert response.status_code == 200
        assert 'mathesdigi_app/check_user_data.html' in [t.name for t in response.templates]

    @pytest.mark.django_db
    def test_change_user_data_renders_form_for_get_request(self, client, setup_test_data):
        session = client.session
        session["user"] = 123
        session.save()
        response = client.get(reverse("change_user_data"))
        assert response.status_code == 200
        assert b"Test" in response.content
        assert b"test@mail.de" in response.content
