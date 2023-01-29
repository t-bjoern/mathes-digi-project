from urllib.parse import urlencode
import pytest
from django.urls import reverse
from mathesdigi_app.models import User


@pytest.mark.django_db
def test_user_create():
    User.objects.create(user_name="Test", mail="test@mail.de")
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_registration_view(client):
    url = reverse("registration")
    data = urlencode({'csrfmiddlewaretoken': 'something',
                      'user_name': 'something',
                      'mail': 'something_2'})
    response = client.post(url, data, content_type="application/x-www-form-urlencoded")
    print(response)
    print(User.objects.get(user_name="something"))
    assert False
