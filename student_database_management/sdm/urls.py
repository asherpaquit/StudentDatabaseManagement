from django.urls import path
from . import views
from .views import register_student
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='student_display'),
    path('register/', register_student, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
