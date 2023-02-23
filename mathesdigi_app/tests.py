from urllib.parse import urlencode
import pytest
from django.urls import reverse
from mathesdigi_app.models import User
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from mathesdigi_app.views import registration


@pytest.mark.django_db
def test_user_create():
    User.objects.create(user_name="Test", mail="test@mail.de")
    assert User.objects.count() == 1


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


# def test_main_view(client):
#     url = reverse("main_view")
#     data = urlencode( {'csrfmiddlewaretoken': ['hSA1qkMMGUbtijMEIycOg3j0dcLNC92ZWDliz2TSLONO3ocZatIn6Pug2BqCgt64'],
#                        'this_task_process': ['task_normal'],
#                        '2A1A': ['23']})
#     response = client.post(url,
#                            data,
#                            content_type="application/x-www-form-urlencoded")
#     print(response)
#     assert False


# def main_view(request, heft, direct_to_task_name):
#     if not request.session.get("user"):
#         return redirect(startpage)
#     user_id = request.session.get("user")
#     context = {}
#     if request.method == 'POST':
#         time_required = round(time.time() - request.session.get("start_time"))
#         post_data, teilaufgaben_ids, this_task_process = helpers.preprocess_request_post_data(dict(request.POST).copy())
#         if this_task_process == "task_normal":
#             for teilaufgaben_id in teilaufgaben_ids:
#                 ergebnis = post_data.get(teilaufgaben_id)
#                 helpers.save_answer(teilaufgaben_id, ergebnis, user_id, time_required)
#         elif this_task_process == "drag_and_drop":
#             # preprocess ...
#             # helpers.save_answer(teilaufgaben_id, ergebnis, user_id)
#             pass
#     if "task" in direct_to_task_name:
#         context = helpers.get_previous_solution(heft, direct_to_task_name, user_id, context)
#     if direct_to_task_name == "evaluation":
#         return redirect(evaluation)
#     request.session["start_time"] = time.time()
#     return render(request, f'mathesdigi_app/{heft}/{direct_to_task_name}.html', context=context)