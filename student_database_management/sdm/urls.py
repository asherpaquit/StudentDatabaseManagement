from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_display, name='student_display'),
]
