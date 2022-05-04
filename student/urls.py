from django.contrib import admin
from django.urls import path
from student.views import add_student, select_student, select2_student

urlpatterns = [
    path('add/', add_student),
    path('select/', select_student),
    path('select2/', select2_student),
]
