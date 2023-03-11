from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.startpage, name='startpage'),
    path('registration/', views.registration, name='registration'),
    path("<str:heft>/<str:direct_to_task_name>/", views.main_view, name="main_view"),
    path('evaluation/', views.evaluation, name='evaluation'),
    path('change_user_data/', views.change_user_data, name='change_user_data'),
    path('check_user_data/', views.check_user_data, name='check_user_data'),
    path('evaluation/show', views.evaluation_show, name='evaluation_show'),
    path('evaluation/download', views.evaluation_download, name='evaluation_download'),
    path('evaluation/send', views.evaluation_send, name='evaluation_send'),
]
