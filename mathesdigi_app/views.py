import time

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from .evaluation import Evaluate
from .models import User

from mathesdigi_app import helpers
from xhtml2pdf import pisa


def startpage(request):
    if "heft" in request.session.keys():
        del request.session["heft"]
    # zum testen immer gleiche user_id nutzen
    # if User.objects.filter(id=61478).exists():
    #     request.session["user"] = 61478
    if "user" in request.session.keys():
        del request.session["user"]
    if request.method == 'POST':
        request.session["heft"] = request.POST["Mathes2"]
        return redirect(registration)
    return render(request, 'mathesdigi_app/startpage.html')


def registration(request):
    if not request.session.get("heft"):
        return redirect(startpage)
    context = {}
    if request.session.get("user"):
        user = User.objects.get(id=request.session["user"])
        context.update({"user_name": user.user_name, "mail": user.mail})
        return redirect(check_user_data)
    elif request.method == 'POST':
        # TODO Currently check for old users at each new registration later as a cronjob or celery task every day.
        helpers.delete_old_users()

        post_data = dict(request.POST).copy()
        for key in post_data:
            post_data[key] = post_data[key][0]
        del post_data["csrfmiddlewaretoken"]
        try:
            user_id = request.session["user"] if request.session.get("user") else None
            user = helpers.validate_registration_create_or_update_user(post_data, user_id)
            request.session["user"] = user.id
            user.heft = request.session["heft"]
            user.save()
            return redirect(check_user_data)
        except ValidationError as e:
            context = post_data
            context["error_message"] = str(e)
    return render(request, 'mathesdigi_app/registration.html', context)


def main_view(request, heft, direct_to_task_name):
    if not request.session.get("user"):
        return redirect(startpage)
    user_id = request.session.get("user")
    context = {}
    if request.method == 'POST':
        time_required = round(time.time() - request.session.get("start_time"))
        post_data, teilaufgaben_ids, this_task_process = helpers.preprocess_request_post_data(dict(request.POST).copy())
        if this_task_process in ["task_normal", "drag_and_drop"]:
            for teilaufgaben_id in teilaufgaben_ids:
                ergebnis = post_data.get(teilaufgaben_id)
                helpers.save_answer(teilaufgaben_id, ergebnis, user_id, time_required)
    if "task" in direct_to_task_name:
        context = helpers.get_previous_solution(heft, direct_to_task_name, user_id, context)
    if direct_to_task_name == "evaluation":
        return redirect(evaluation)
    request.session["start_time"] = time.time()
    return render(request, f'mathesdigi_app/{heft}/{direct_to_task_name}.html', context=context)


def check_user_data(request):
    if not request.session.get("user"):
        return redirect(startpage)
    user_id = request.session["user"]
    try:
        user = User.objects.get(id=user_id)
    except Exception:
        return redirect(startpage)
    context = {"user_name": user.user_name, "mail": user.mail, "heft": user.heft}
    return render(request, 'mathesdigi_app/check_user_data.html', context)


def change_user_data(request):
    user_id = request.session["user"]
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        post_data = dict(request.POST).copy()
        post_data = {key: value[0] for key, value in post_data.items()}

        user = helpers.validate_registration_create_or_update_user(post_data, user_id)

    context = {"user_name": user.user_name, "mail": user.mail, "heft": user.heft}
    return render(request, 'mathesdigi_app/check_user_data.html', context)


def get_template_and_evaluate(request):
    user_id = request.session["user"]
    user = User.objects.get(id=user_id)
    # Template laden und mit Daten füllen
    template = get_template('evaluation_template.html')
    eval_obj = Evaluate(user)
    context = eval_obj.create_evaluation_context()
    return template, context


def evaluation(request):
    try:
        user_id = request.session["user"]
        user = User.objects.get(id=user_id)

        from_email = "lasttest@mathes-digi.de"
        to_email = user.mail
        subject = f"Auswertung des Testes von {user.user_name}"

        template, context = get_template_and_evaluate(request)

        html_content = template.render(context)
        text_content = 'Dies ist eine Beispiel-E-Mail, die mit einem HTML-Template erstellt wurde.'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        context = {"error": str(e)}
    return render(request, 'mathesdigi_app/evaluation.html', context)


def evaluation_send(request):
    user_id = request.session["user"]
    user = User.objects.get(id=user_id)

    from_email = "test@md-staging.django.group"
    to_email = user.mail
    subject = f"Auswertung des Testes von {user.user_name}"

    template, context = get_template_and_evaluate(request)

    html_content = template.render(context)
    text_content = 'Dies ist eine Beispiel-E-Mail, die mit einem HTML-Template erstellt wurde.'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return redirect(evaluation)


def evaluation_show(request):
    template, context = get_template_and_evaluate(request)
    html = template.render(context)
    return HttpResponse(html)


def evaluation_download(request):
    template, context = get_template_and_evaluate(request)
    context.update({'width': 150})
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Auswertung.pdf"'
    # Generate the PDF from the HTML content
    pisa_status = pisa.CreatePDF(html, dest=response)
    # Check if the PDF was generated successfully
    if pisa_status.err:
        return HttpResponse('Error generating PDF file')
    return response
