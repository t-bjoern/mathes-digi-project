import random

from django.shortcuts import render, redirect
from .models import User


def example1(request):
    user_id = request.session.get("user_id")
    return render(request, 'Mathes2/1_example.html')


def registration(request):
    if request.method == 'POST':
        post_data = dict(request.POST).copy()
        for key in post_data:
            post_data[key] = post_data[key][0]
        del post_data["csrfmiddlewaretoken"]

        user_name = post_data["pseudonym"]
        klasse = post_data["klasse"]
        schule = post_data["schule"]
        jahrgang = post_data["jahrgang"]
        pseudonym = post_data["pseudonym"]
        mail = post_data["mailadresse"]

        try:
            user_id = create_random_user_id()
            User.objects.create(user_name=user_name,
                                user_id=user_id,
                                klasse=klasse,
                                schule=schule,
                                lehrer_mail=mail,
                                pseudonym=pseudonym,
                                jahrgang=jahrgang)
            # Speichern der user_id in der request.session, um auf den nächsten Seiten
            # eine Identifikation des Nutzers zu ermöglichen.
            request.session["user_id"] = user_id
            return redirect(example1)
        except Exception as e:
            # Context füllen, um Daten und Fehlermeldungen im Fomrular anzzuzeigen.
            context = post_data
            if "pseudonym" in str(e):
                context["error_pseudonym"] = True
            if "klasse" in str(e):
                context["error_klasse"] = True
            if "schule" in str(e):
                context["error_schule"] = True
            if "jahrgang" in str(e):
                context["error_jahrgang"] = True
            if "mailadresse" in str(e):
                context["error_mailadresse"] = True

            return render(request, 'Mathes2/registration.html', context)
    else:
        return render(request, 'Mathes2/registration.html')


def create_random_user_id():
    """
    Erstellen einer zufälligen user_id welche noch nicht in der Datenbank verwendet wird.
    Returns:
        user_id: int
    """
    while True:
        user_id = random.randint(10000, 99999)
        if not User.objects.filter(user_id=user_id).exists():
            break
    return user_id
