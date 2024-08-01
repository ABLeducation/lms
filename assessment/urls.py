from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('', QuizView.as_view(), name="main_view"),
    path('<pk>/', quiz_view, name="quiz_view"),
    path('<pk>/save/', quiz_data_save, name="quiz_data_save"),
    path('<pk>/data/', quiz_data_view, name="quiz_data_view"),
]