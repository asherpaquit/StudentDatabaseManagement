# from django.urls import path
# from . import views
# from .views import register_student
# from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import LogoutView

# urlpatterns = [
#     path('', views.home_view, name='student_display'),
#     path('register/', register_student, name='register'),
#     path('login/', auth_views.LoginView.as_view(), name='login'),
#     path('logout/',LogoutView.as_view(next_page='home'),name ='logout'),
# ]

from django.urls import path
from .views import register_student, login_student, home_view, aboutus, studentservice

urlpatterns = [
    path('register/', register_student, name='register'),
    path('login/', login_student, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', login_student, name='logout'),  # Use the custom logout view
    path('aboutus/',aboutus, name='aboutus'),
    path('studentservice/',studentservice, name='studentservice'),
]

