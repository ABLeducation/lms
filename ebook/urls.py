from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/<int:grade_id>/books/', views.ebook_list, name='ebook_list'),
    path('books/<int:book_id>/lessons/', views.display_lessons, name='display_lessons'),
]