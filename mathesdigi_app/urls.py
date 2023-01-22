from django.urls import path

from . import views

urlpatterns = [
    path('', views.startpage, name='startpage'),
    path('registration/', views.registration, name='registration'),
    # path('registration/save', views.save_registration, name='save_registration'),
    path('Mathes2/example1/', views.heft2_example1, name='heft2_example1')
]
