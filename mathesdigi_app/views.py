from django.shortcuts import render, redirect
from .models import User, Aufgaben, Teilaufgaben, Ergebnisse

from mathesdigi_app import helpers


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

        try:
            if "user" not in request.session.keys():
                user = helpers.validate_registration_create_user(post_data)

                # Speichern der user_id in der Sessiondaten
                request.session["user"] = user.id
                user.heft = request.session["heft"]
                user.save()

            if request.session["heft"] == "Mathes2":
                return redirect(heft2_task1_example)

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


def heft2_task1_example(request):
    context = {}
    if request.method == 'POST':
        post_data = dict(request.POST).copy()
        del post_data["csrfmiddlewaretoken"]

        if any(a != [""] for a in post_data.values()):
            context, wertung = helpers.display_solution_example(post_data)
            if wertung:
                return redirect(heft2_task1_1)
        else:
            context = {"empty_field": True}

    return render(request, 'mathesdigi_app/1_example.html', context)


def heft2_task1_1(request):
    context = {}
    if request.method == 'POST':
        post_data = dict(request.POST).copy()
        del post_data["csrfmiddlewaretoken"]

        if any(a != [""] for a in post_data.values()):
            user_id = request.session["user"]
            helpers.save_answer(post_data, user_id)
            # return redirect(heft2_task1_2)
        else:
            context = {"empty_field": True}
    return render(request, 'mathesdigi_app/1_task_1.html', context)
