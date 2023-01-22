import random

from django.shortcuts import render, redirect
from .models import User


def startpage(request):
    if request.method == 'POST':
        request.session["heft"] = request.POST["Mathes2"]
        return redirect(registration)
    if "user" in request.session.keys():
        del request.session["user"]
    return render(request, 'mathesdigi_app/startpage.html')


def registration(request):
    if request.method == 'POST':
        post_data = dict(request.POST).copy()
        for key in post_data:
            post_data[key] = post_data[key][0]
        del post_data["csrfmiddlewaretoken"]

        user_name = post_data["user_name"].strip()
        mail = post_data["mail"].strip()

        try:
            # Validierung der Eingabedaten
            if user_name == "" or mail == "":
                raise Exception("Bitte überprüfen Sie die Eingabe. Die Felder dürfen nicht leer sein!")

            if "user" not in request.session.keys():
                user = User.objects.create(id=create_random_user_id(),
                                           user_name=user_name,
                                           mail=mail)
                # Speichern der user_id in der request.session, um auf den nächsten Seiten
                # eine Identifikation des Nutzers zu ermöglichen.
                request.session["user"] = user.id

            if request.session["heft"] == "Mathes2":
                return redirect(heft2_example1)

        except Exception as e:
            # Context füllen, um Daten und Fehlermeldungen im Fomrular anzzuzeigen.
            context = post_data
            context["error_message"] = str(e)

            return render(request, 'mathesdigi_app/registration.html', context)
    else:
        if "user" in request.session.keys():
            user = User.objects.get(id=request.session["user"])
            context = {"user_name": user.user_name,
                       "mail": user.mail}
            return render(request, 'mathesdigi_app/registration.html', context)

        return render(request, 'mathesdigi_app/registration.html')


def heft2_example1(request):
    if request.method == 'POST':
        post_data = dict(request.POST).copy()


    user_id = request.session.get("user")

    return render(request, 'mathesdigi_app/1_example.html')


def create_random_user_id():
    """
    Erstellen einer zufälligen user_id welche noch nicht in der Datenbank verwendet wird.
    Returns:
        user_id: int
    """
    while True:
        user_id = random.randint(10000, 99999)
        if not User.objects.filter(id=user_id).exists():
            break
    return user_id
