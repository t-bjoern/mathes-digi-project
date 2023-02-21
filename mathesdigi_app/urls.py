from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.startpage, name='startpage'),
    path('registration/', views.registration, name='registration'),
    path("<str:heft>/<str:direct_to_task_name>/", views.main_view, name="main_view"),
    path('evaluation/', views.evaluation, name='evaluation'),
    path('evaluation/change_user_data', views.evaluation_change_user_data, name='evaluation_change_user_data'),
    path('evaluation/send', views.evaluation_send, name='evaluation_send'),
]
