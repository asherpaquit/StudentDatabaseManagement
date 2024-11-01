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
from .views import register_student, login_student, home_view, aboutus, studentservice, academics, register_teacher, login_teacher, teacher_dashboard, college, senior_high, elementary

urlpatterns = [
    path('register/', register_student, name='register'),
    path('login/', login_student, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', login_student, name='logout'),  # Use the custom logout view
    path('aboutus/',aboutus, name='aboutus'),
    path('studentservice/',studentservice, name='studentservice'),
    # path('academics/',academics, name='academics'),
    path('register_teacher/', register_teacher, name='register_teacher'),
    path('login_teacher/', login_teacher, name='login_teacher'),
    path('teacher_dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('academics/', academics, name='academics'),   #-- yap academics
    path('academics/elementary/', elementary, name='elementary'),
    path('academics/senior_high/', senior_high, name='senior_high'),
    path('academics/college/', college, name='college'),
    # path('add_grade/', add_grade, name='add_grade'),
]

