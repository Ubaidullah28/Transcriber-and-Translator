# speech/urls.py
from django.urls import path
from . import views

app_name = 'speech'

urlpatterns = [
    path('', views.home, name='home'),
    path('transcribe/', views.transcribe_view, name='transcribe'),
    path('transcribe/record/', views.transcribe_record_view, name='transcribe_record'),
    path('translate/', views.translate_view, name='translate'),
]
