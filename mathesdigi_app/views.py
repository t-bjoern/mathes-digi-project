from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse

from .evaluation import Evaluate
from .models import User, Aufgaben, Teilaufgaben, Ergebnisse

from mathesdigi_app import helpers


def startpage(request):
    if "heft" in request.session.keys():
        del request.session["heft"]
    # zum testen immer gleiche user_id nutzen
    if User.objects.filter(id=14095).exists():
        request.session["user"] = 14095
    elif "user" in request.session.keys():
        del request.session["user"]
    if request.method == 'POST':
        request.session["heft"] = request.POST["Mathes2"]
        return redirect(registration)
    return render(request, 'mathesdigi_app/startpage.html')


def registration(request):
    context = {}
    if request.method == 'POST':
        # TODO Currently check for old users at each new registration later as a cronjob or celery task every day.
        helpers.delete_old_users()

        post_data = dict(request.POST).copy()
        for key in post_data:
            post_data[key] = post_data[key][0]
        del post_data["csrfmiddlewaretoken"]
        try:
            if not request.session.get("heft"):
                raise ValidationError("Bitte starte auf der ersten Seite und wähle dort ein Heft aus!")
            user_id = request.session["user"] if request.session.get("user") else None
            user = helpers.validate_registration_create_or_update_user(post_data, user_id)
            request.session["user"] = user.id
            user.heft = request.session["heft"]
            user.save()
            return redirect(reverse('main_view', args=(request.session["heft"], "1_example")))
        except ValidationError as e:
            context = post_data
            context["error_message"] = str(e)
    if request.session.get("user"):
        user = User.objects.get(id=request.session["user"])
        context.update({"user_name": user.user_name, "mail": user.mail})
    return render(request, 'mathesdigi_app/registration.html', context)


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
            ergebnis = post_data["input"]
            print(teilaufgaben_id, ergebnis)
            helpers.save_answer(teilaufgaben_id, ergebnis, user_id)
        elif this_task_process == "drag_and_drop":
            # preprocess ...
            # helpers.save_answer(teilaufgaben_id, ergebnis, user_id)
            pass
    if next_task_name == "evaluation":
        return redirect(evaluation)
    return render(request, f'mathesdigi_app/{heft}/{next_task_name}.html')


def evaluation(request):
    user_id = request.session["user"]
    user = User.objects.get(id=user_id)
    context = {"user_name": user.user_name, "mail": user.mail}
    return render(request, 'mathesdigi_app/evaluation.html', context)


def evaluation_send(request):
    user_id = request.session["user"]
    user = User.objects.get(id=user_id)
    context = {"mail": user.mail}
    Evaluate(user)
    # eva_obj.send_evaluation()
    # eva_obj.save_results_for_statistic()
    # save values for statistics
    return render(request, 'mathesdigi_app/end.html', context)


def evaluation_change_user_data(request):
    user_id = request.session["user"]
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        post_data = dict(request.POST).copy()
        post_data = {key: value[0] for key, value in post_data.items()}
        user_name = post_data["user_name"]
        mail = post_data["mail"]

        user.user_name = user_name
        user.mail = mail
        user.save()
    context = {"user_name": user.user_name, "mail": user.mail}
    return render(request, 'mathesdigi_app/evaluation.html', context)
