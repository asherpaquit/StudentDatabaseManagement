from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .models import Student

# View to display all students
def student_display(request):
    students = Student.objects.all()  # Fetch all students from the database
    return render(request, 'sdm/student_display.html', {'students': students})  # Pass students to the template

# View to register a new student
def register_student(request):
    if request.method == "POST":
        student_name = request.POST['student_name']
        email = request.POST['email']
        password = request.POST['password']

        # Hash the password before saving
        hashed_password = make_password(password)

        try:
            student = Student(student_name=student_name, email=email, password=hashed_password)
            student.save()
            messages.success(request, "Student registered successfully!")
            return redirect('login')  # Redirect to login page after successful registration
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
                request.session['student_name'] = student.student_name  # Store name in session
                return redirect('home')  # Redirect to home page
            else:
                messages.error(request, "Invalid password.")
        except Student.DoesNotExist:
            messages.error(request, "Student not found.")

    return render(request, 'sdm/login.html')



# View to display the home page
@login_required
def home_view(request):
    student_name = request.session.get('student_name')  # Get name from session
    return render(request, 'sdm/home.html', {'student_name': student_name})

# Add custom LoginView and LogoutView if needed (optional)
class CustomLoginView(LoginView):
    template_name = 'sdm/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'  # Redirect to the login page after logout
