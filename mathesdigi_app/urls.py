from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.startpage, name='startpage'),
    path('registration/', views.registration, name='registration'),
    path("<str:heft>/<str:next_task_name>/", views.main_view, name="main_view")
]
