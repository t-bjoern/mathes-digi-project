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
    if request.method == 'POST':
        post_data = dict(request.POST).copy()
        del post_data["csrfmiddlewaretoken"]

        if any(a != [""] for a in post_data.values()):
            # context = check_answer_example(post_data)
            context, wertung = helpers.display_solution_example(post_data)

            if wertung:
                return redirect(heft2_task1_1)

            return render(request, 'mathesdigi_app/1_example.html', context)

    return render(request, 'mathesdigi_app/1_example.html')


def heft2_task1_1(request):
    if request.method == 'POST':
        post_data = dict(request.POST).copy()
        del post_data["csrfmiddlewaretoken"]

        if any(a != [""] for a in post_data.values()):
            user = request.session["user"]

            for key, value in post_data.items():
                teilaufgaben_id = key
                ergebnis = int(value[0])
                teilaufgabe = Teilaufgaben.objects.get(teilaufgaben_id=teilaufgaben_id)

                if Ergebnisse.objects.filter(user_id=user, teilaufgabe=teilaufgabe).exists():
                    ergebnis_obj = Ergebnisse.objects.get(user_id=user, teilaufgabe=teilaufgabe)
                    ergebnis_obj.eingabe = ergebnis
                    ergebnis_obj.wertung = bool(ergebnis == teilaufgabe.loesung)
                    ergebnis_obj.save()
                else:
                    Ergebnisse.objects.create(user_id=user,
                                              teilaufgabe=teilaufgabe,
                                              eingabe=ergebnis,
                                              wertung=bool(ergebnis == teilaufgabe.loesung))

    return render(request, 'mathesdigi_app/1_task_1.html')
