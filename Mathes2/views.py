from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# from .forms import MyForm
from .models import User


def example1(request):
    return render(request, 'Mathes2/1_example.html')


def registration(request):
    if request.method == 'POST':
        data = request.POST
        user_name = data["pseudonym"]
        klasse = data["klasse"]
        schule = data["schule"]
        jahrgang = data["jahrgang"]
        mail = data["mailadresse"]

        try:
            # User.objects.create(user_name=user_name, user_id=23, klasse=klasse, schule=schule, lehrer_mail=mail)
            return redirect(example1)
        except Exception as e:
            print(e)
            return redirect(request.path_info)
            # return render(request, 'Mathes2/start.html')
    else:
        return render(request, 'Mathes2/start.html')


    #
    #     print(request.POST)
    #     # form = MyForm(request.POST)
    #     # if form.is_valid():
    #         # Speichern Sie die Daten in der Datenbank
    #         # data = form.cleaned_data
    #         # MyModel.objects.create(**data)
    #         # Weiterleiten an die nächste Seite
    #         # return redirect('next_page')
    # else:
    #     print(False)

