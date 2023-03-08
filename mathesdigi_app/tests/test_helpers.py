import pytest
import pandas as pd

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from io import BytesIO

from mathesdigi_app import helpers
from mathesdigi_app.models import User, Aufgaben, Teilaufgaben, Ergebnisse, Wertung


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
    context = helpers.get_previous_solution(heft="Mathes2", direct_to_task_name=template_name, user_id=user.id,
                                            context={})
    assert context == output_context


class TestReadAndValidateFile:
    # Test that the function returns None and an error message when given a file with
    # an unsupported format or an invalid file
    @pytest.mark.parametrize("file_type", [
        ".txt", ".csv", ".xlsx"
    ])
    def test_read_and_validate_file_unsupported_format_and_invalid_file(self, file_type):
        with open(f"mathesdigi_app/tests/test_files/unsupported_format{file_type}", "rb") as f:
            df, error_message = helpers.read_and_validate_file(f)
        assert df is None
        assert error_message == ["File is not in the correct format. You can only upload Excel or CSV files."]

    # Test that the function returns None and an error message when given a file that exceeds the maximum file size
    def test_read_and_validate_file_exceeds_max_size(self):
        df = pd.DataFrame({"A": range(100000)})
        csv_string = df.to_csv(index=False)
        file_obj = BytesIO(csv_string.encode())
        file = InMemoryUploadedFile(file_obj, field_name=None, name='sample_file.csv', content_type='text/csv',
                                    size=len(csv_string), charset=None)
        df, error_message = helpers.read_and_validate_file(file, max_file_size=1000)
        assert df is None
        assert error_message == ["File size exceeds the limit of 0.00095367431640625 MB"]

    # Test that the function returns a DataFrame and an empty error message when given a valid CSV file
    def test_read_and_validate_file_valid_csv(self):
        df = pd.DataFrame({"Rohwert": [1, 2, 3], "T-Wert": [4, 5, 6], "Prozentrang": [7, 8, 9]})
        csv_string = df.to_csv(index=False)
        file_obj = BytesIO(csv_string.encode())
        file = InMemoryUploadedFile(file_obj, field_name=None, name='sample_file.csv', content_type='text/csv',
                                    size=len(csv_string), charset=None)
        df_result, error_message = helpers.read_and_validate_file(file)
        pd.testing.assert_frame_equal(df_result, df)
        assert error_message == ["No excel file try to read with csv reader!"]

    # Test that the function returns a DataFrame and an empty error message when given a valid Excel file
    def test_read_and_validate_file_valid_excel(self):
        df = pd.DataFrame({"Rohwert": [1, 2, 3], "T-Wert": [4, 5, 6], "Prozentrang": [7, 8, 9]})
        with BytesIO() as excel_file:
            df.to_excel(excel_file, index=False)
            excel_content = excel_file.getvalue()
        file = InMemoryUploadedFile(BytesIO(excel_content), None, 'sample_file.xlsx',
                                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                    len(excel_content), None)
        df_result, error_message = helpers.read_and_validate_file(file)
        pd.testing.assert_frame_equal(df_result, df)
        assert error_message == []

    # Test that the function returns an error message when given a CSV file with an incorrect header
    def test_read_and_validate_file_invalid_header(self):
        df = pd.DataFrame({"Rohwert": [1, 2, 3], "T-Wert": [4, 5, 6], "Incorrect Header": [7, 8, 9]})
        csv_string = df.to_csv(index=False)
        file_obj = BytesIO(csv_string.encode())
        file = InMemoryUploadedFile(file_obj, field_name=None, name='sample_file.csv', content_type='text/csv',
                                    size=len(csv_string), charset=None)
        df_result, error_message = helpers.read_and_validate_file(file)
        assert df_result is None
        assert "Table format is incorrect. Rohwert, T-Wert, and Prozentrang must be in the header." in error_message

    # Test that the function returns an error message when given an Excel file with too many columns
    def test_read_and_validate_file_invalid_columns(self):
        df = pd.DataFrame(
            {"Rohwert": [1, 2, 3], "T-Wert": [4, 5, 6], "Prozentrang": [7, 8, 9], "Extra Column": [10, 11, 12]})
        csv_string = df.to_csv(index=False)
        file_obj = BytesIO(csv_string.encode())
        file = InMemoryUploadedFile(file_obj, field_name=None, name='sample_file.csv', content_type='text/csv',
                                    size=len(csv_string), charset=None)
        df_result, error_message = helpers.read_and_validate_file(file)
        assert df_result is None
        assert "Table format is incorrect. The table contains too many columns." in error_message


@pytest.mark.django_db
def test_create_or_update_wertung_apply():
    row = pd.Series({"Rohwert": 56, "T-Wert": "73", "Prozentrang": 100})
    updated, created = helpers.create_or_update_wertung_apply(row=row, heft_nr=2, start_month=2, start_day=1,
                                                              end_month=3, end_day=31)
    assert created == 1, updated == 0
    assert Wertung.objects.count() == 1
    wertung_obj = Wertung.objects.get(rohwert=row["Rohwert"])
    assert wertung_obj.t_wert == row["T-Wert"], wertung_obj.prozentrang == row["Prozentrang"]

    # Pass an existing wertung to the function to test if it will be updated
    row = pd.Series({"Rohwert": 56, "T-Wert": "74", "Prozentrang": 90})
    updated, created = helpers.create_or_update_wertung_apply(row=row, heft_nr=2, start_month=2, start_day=1,
                                                              end_month=3, end_day=31)
    assert created == 0, updated == 1
    assert Wertung.objects.count() == 1
    wertung_obj = Wertung.objects.get(rohwert=row["Rohwert"])
    assert wertung_obj.t_wert == row["T-Wert"], wertung_obj.prozentrang == row["Prozentrang"]


def test_preprocess_request_post_data():
    post_data = {"csrfmiddlewaretoken": ["sRsPS74ilPwQ6PbsDBvXOqSJ5UPBAGhg7Cd61PboqJ8bRUBN5w1wEc3ZUjuqe0ll"],
                 "this_task_process": ["task_normal"],
                 "2A1A": [""],
                 "2A1B": [""]}
    new_post_data, teilaufgaben_ids, this_task_process = helpers.preprocess_request_post_data(post_data)

    assert not new_post_data.get("csfrmiddlewaretoken")
    assert teilaufgaben_ids == ["2A1A", "2A1B"]
    assert this_task_process == post_data.get("this_task_process")[0]
