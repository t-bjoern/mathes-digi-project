import datetime
import time
import pytest
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



# def validate_registration_create_or_update_user(registration_data: dict, user_id=None)
# def save_answer(teilaufgaben_id: str, ergebnis: int, user_id: int, time_required: int)
# def get_previous_solution(heft, direct_to_task_name, user_id, context)
# def create_or_update_wertung_apply(row, heft_nr, start_month, start_day, end_month, end_day)
# def read_and_validate_file(file, max_file_size=1048576)
# def preprocess_request_post_data(post_data: dict)