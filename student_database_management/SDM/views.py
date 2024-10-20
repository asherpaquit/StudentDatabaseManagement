from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .models import Student


def student_display(request):
    students = Student.objects.all()  
    return render(request, 'sdm/student_display.html', {'students': students})  # Pass students to the template


def register_student(request):
    if request.method == "POST":
        student_name = request.POST['student_name']
        email = request.POST['email']
        password = request.POST['password']

        
        hashed_password = make_password(password)

        try:
            student = Student(student_name=student_name, email=email, password=hashed_password)
            student.save()
            messages.success(request, "Student registered successfully!")
            return redirect('login')  
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'sdm/register.html')


def login_student(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            student = Student.objects.get(email=email)
            if check_password(password, student.password):
                # Successful login
                request.session['student_name'] = student.student_name  
                request.session['email'] = student.email
                return redirect('home')  
            else:
                messages.error(request, "Invalid password.")
        except Student.DoesNotExist:
            messages.error(request, "Student not found.")

    return render(request, 'sdm/login.html')

@login_required
def aboutus(request):
    student_name = request.session.get('student_name')
    return render(request, 'sdm/aboutus.html', {'student_name': student_name})

@login_required
def academics(request):
    student_name = request.session.get('student_name')
    return render(request, 'sdm/academics.html', {'student_name': student_name})


@login_required
def home_view(request):
    student_name = request.session.get('student_name') 
    #Francis Nino Yap ----------#
    return render(request, 'sdm/home.html', {'student_name': student_name})

@login_required
def studentservice(request):
    student_name = request.session.get('student_name')
    email = request.session.get('email')
    return render(request, 'sdm/studentservice.html', {'student_name': student_name, 'student_email': email})


# Terence John Duterte ------------ #
class CustomLoginView(LoginView):
    template_name = 'sdm/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'  

