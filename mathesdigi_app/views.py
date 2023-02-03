from django.shortcuts import render, redirect
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
            if request.session["heft"] == "Mathes2":
                return redirect(heft2_task1_example)
                # Mit neuen views in etwa so...
                # return redirect(example_view(request, heft=request.session["heft"], template_name="2A1E"))

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


def task_view(request, heft, template_name):
    if request.method == 'POST':
        post_data = dict(request.POST).copy()
        del post_data["csrfmiddlewaretoken"]

        user_id = request.session["user"]
        helpers.save_answer(post_data, user_id)

    return render(request, f'mathesdigi_app/{heft}/{template_name}.html')


def example_view(request, heft, template_name):
    context = helpers.get_example_solution(template_name)

    return render(request, f'mathesdigi_app/{heft}/{template_name}.html', context)


# Alte Views können entfernt werden sobald alle .html angepasst sind.

def heft2_task1_example(request):
    context = {}
    if request.method == 'POST':
        post_data = dict(request.POST).copy()
        del post_data["csrfmiddlewaretoken"]

        if "example_showed" in request.session.keys():
            del request.session["example_showed"]
            return redirect(heft2_task1_1)
        if any(a != [""] for a in post_data.values()):
            request.session["example_showed"] = True
            context = helpers.display_solution_example(post_data)
        else:
            context = {"empty_field": True}

    return render(request, 'mathesdigi_app/1_example.html', context)


def heft2_task1_1(request):
    context = {}
    if request.method == 'POST':
        post_data = dict(request.POST).copy()
        del post_data["csrfmiddlewaretoken"]

        user_id = request.session["user"]

        helpers.save_answer(post_data, user_id)

    return render(request, 'mathesdigi_app/1_task_1.html', context)
