import pytest
import pandas as pd

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from io import BytesIO

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
    # def test_read_and_validate_file_valid_excel(self):
    #     df = pd.DataFrame({"Rohwert": [1, 2, 3], "T-Wert": [4, 5, 6], "Prozentrang": [7, 8, 9]})
    #     excel_string = df.to_excel(index=False)
    #     file_obj = BytesIO(excel_string.encode())
    #     file = InMemoryUploadedFile(file_obj, field_name=None, name='sample_file.csv', content_type='text/csv',
    #                                 size=len(excelstring), charset=None)
    #     df_result, error_message = helpers.read_and_validate_file(file)
    #     pd.testing.assert_frame_equal(df_result, df)
    #     assert error_message == []
    #
    # Test that the function returns an error message when given a CSV file with an incorrect header
    def test_read_and_validate_file_invalid_csv_header(self):
        df = pd.DataFrame({"Rohwert": [1, 2, 3], "T-Wert": [4, 5, 6], "Incorrect Header": [7, 8, 9]})
        csv_string = df.to_csv(index=False)
        file_obj = BytesIO(csv_string.encode())
        file = InMemoryUploadedFile(file_obj, field_name=None, name='sample_file.csv', content_type='text/csv',
                                    size=len(csv_string), charset=None)
        df_result, error_message = helpers.read_and_validate_file(file)
        assert df_result is None
        assert "Table format is incorrect. Rohwert, T-Wert, and Prozentrang must be in the header." in error_message

    # Test that the function returns an error message when given an Excel file with an incorrect header
    # def test_read_and_validate_file_invalid_excel_header(self):
    #     df = pd.DataFrame({"Rohwert": [1, 2, 3], "T-Wert": [4, 5, 6], "Incorrect Header": [7, 8, 9]})
    #     df.to_excel("invalid_file.xlsx", index=False)
    #     with open("invalid_file.xlsx", "rb") as f:
    #         df_result, error_message = helpers.read_and_validate_file(f)
    #     assert df_result is None
    #     assert "Table format is incorrect. Rohwert, T-Wert, and Prozentrang must be in the header." in error_message
    #
    # # Test that the function returns an error message when given an Excel file with too many columns
    # def test_read_and_validate_file_invalid_excel_columns(self):
    #     df = pd.DataFrame(
    #         {"Rohwert": [1, 2, 3], "T-Wert": [4, 5, 6], "Prozentrang": [7, 8, 9], "Extra Column": [10, 11, 12]})
    #     df.to_excel("invalid_file.xlsx", index=False)
    #     with open("invalid_file.xlsx", "rb") as f:
    #         df_result, error_message = helpers.read_and_validate_file(f)
    #     assert df_result is None
    #     assert "Table format is incorrect. The table contains too many columns." in error_message
    #
    # Test that the function returns an error message when given an invalid CSV file




# def create_or_update_wertung_apply(row, heft_nr, start_month, start_day, end_month, end_day)
# def preprocess_request_post_data(post_data: dict)