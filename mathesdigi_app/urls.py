from django.urls import path

from . import views

urlpatterns = [
    path('', views.registration, name='registration'),
    path('registration/', views.registration, name='registration'),
    path('example1/', views.example1, name='example1')
]
