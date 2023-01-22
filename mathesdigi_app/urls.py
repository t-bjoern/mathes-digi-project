from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.startpage, name='startpage'),
    path('registration/', views.registration, name='registration'),
    path('Mathes2/example1/', views.heft2_example1, name='heft2_example1'),
    path('admin/', admin.site.urls),
]
