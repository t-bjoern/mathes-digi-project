from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Aufgaben, Teilaufgaben, Ergebnisse

from mathesdigi_app import helpers


def startpage(request):
    if "heft" in request.session.keys():
        del request.session["heft"]
    if "user" in request.session.keys():
        del request.session["user"]
    if request.method == 'POST':
        request.session["heft"] = request.POST["Mathes2"]
        return redirect(registration)
    return render(request, 'mathesdigi_app/startpage.html')


def registration(request):
    if request.method == 'POST':
        post_data = dict(request.POST).copy()
        for key in post_data:
            post_data[key] = post_data[key][0]
        del post_data["csrfmiddlewaretoken"]

        try:
            # Fehlermeldung wenn kein Heft auf der ertsen Seite gewählt wurde. Später dann durch Alert und
            # redirect auf startpage.
            if "heft" not in request.session.keys():
                raise Exception("Bitte starte auf der ertsen Seite und wähle dort ein Heft aus!")
            if "user" not in request.session.keys():
                user = helpers.validate_registration_create_user(post_data)
                # Speichern der user_id in der Sessiondaten
                request.session["user"] = user.id
                user.heft = request.session["heft"]
                user.save()
            return redirect(reverse('main_view', args=(request.session["heft"], "1_example")))
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


def main_view(request, heft, next_task_name):
    if request.method == 'POST':
        post_data = dict(request.POST).copy()
        # Convert lists in dict to single values
        post_data = {key: value[0] for key, value in post_data.items()}
        # Delete unnecessary information in post_data
        del post_data["csrfmiddlewaretoken"]
        this_task_process = post_data["this_task_process"]
        user_id = request.session["user"]

        if this_task_process == "example":
            pass
        elif this_task_process == "task_normal":
            teilaufgaben_id = post_data["task_id"]
            ergebnis = int(post_data["input"])
            helpers.save_answer(teilaufgaben_id, ergebnis, user_id)
        elif this_task_process == "drag_and_drop":
            # preprocess ...
            # helpers.save_answer(teilaufgaben_id, ergebnis, user_id)
            pass
    return render(request, f'mathesdigi_app/{heft}/{next_task_name}.html')
