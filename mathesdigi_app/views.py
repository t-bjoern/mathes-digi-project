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
        del post_data["csrfmiddlewaretoken"]

        if any(a != [""] for a in post_data.values()):
            # context = check_answer_example(post_data)
            context = helpers.display_solution_example(post_data)

            return render(request, 'mathesdigi_app/1_example.html', context)

    return render(request, 'mathesdigi_app/1_example.html')



