from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.startpage, name='startpage'),
    path('registration/', views.registration, name='registration'),
    path('Mathes2/example1/', views.heft2_task1_example, name='heft2_task1_example'),
    path('Mathes2/task1/', views.heft2_task1_1, name='heft2_task1_1')

]
