from django.urls import path,include
from . import views

app_name='mechanzo'
urlpatterns = [
    path("", views.display_kits, name="mechanzo_kits"),
    path("<slug:slug>/", views.display_models, name="models_list")
]