from urllib.parse import urlencode
import pytest
from django.urls import reverse
from mathesdigi_app.models import User


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
def test_registration_view(client, user_name, user_mail, count_user, error):
    url = reverse("registration")
    data = urlencode({'csrfmiddlewaretoken': 'some_token',
                      'user_name': user_name,
                      'mail': user_mail})
    response = client.post(url,
                           data,
                           content_type="application/x-www-form-urlencoded")
    if not error:
        user = User.objects.get(user_name=user_name.strip(),
                                mail=user_mail.strip())
        assert user
    assert User.objects.count() == count_user
    assert bool("Bitte überprüfen Sie die Eingabe. Die Felder dürfen nicht leer sein!" \
           in str(response.content, "utf-8")) == error
