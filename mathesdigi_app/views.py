import random

from django.shortcuts import render, redirect
from .models import User


def startpage(request):
    return render(request, 'mathesdigi_app/startpage.html')


def heft2_example1(request):
    user_id = request.session.get("user")

    return render(request, 'mathesdigi_app/1_example.html')


def registration(request):
    if request.method == 'POST':
        post_data = dict(request.POST).copy()
        for key in post_data:
            post_data[key] = post_data[key][0]
        del post_data["csrfmiddlewaretoken"]

        user_name = post_data["pseudonym"]
        klasse = post_data["klasse"]
        schule = post_data["schule"]
        heft_nr = int(post_data["heft_nr"])
        mail = post_data["mailadresse"]

        try:
            user = User.objects.create(id=create_random_user_id(),
                                       user_name=user_name,
                                       klasse=klasse,
                                       schule=schule,
                                       heft_nr=heft_nr,
                                       mail=mail)
            # Speichern der user_id in der request.session, um auf den nächsten Seiten
            # eine Identifikation des Nutzers zu ermöglichen.
            request.session["user"] = user.id

            if user.heft_nr == 2:
                return redirect(heft2_example1)

        except Exception as e:
            # Context füllen, um Daten und Fehlermeldungen im Fomrular anzzuzeigen.
            context = post_data
            if "user_name" in str(e):
                context["error_pseudonym"] = True
            if "klasse" in str(e):
                context["error_klasse"] = True
            if "schule" in str(e):
                context["error_schule"] = True
            if "heft_nr" in str(e):
                context["error_heft"] = True
            if "mailadresse" in str(e):
                context["error_mailadresse"] = True

            return render(request, 'mathesdigi_app/registration.html', context)
    else:
        return render(request, 'mathesdigi_app/registration.html')


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
