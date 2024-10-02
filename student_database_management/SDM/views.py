from django.shortcuts import render, redirect  # Ensure you import redirect
from .models import Student
from .forms import StudentRegistrationForm  # Import your registration form

# View to display all students
def student_display(request):
    students = Student.objects.all()  # Fetch all students from the database
    return render(request, 'sdm/student_display.html', {'students': students})  # Pass students to the template

# View to register a new student
def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)  # Instantiate the form with POST data
        if form.is_valid():
            form.save()  # Save the new student
            return redirect('login')  # Redirect to the login page after registration
    else:
        form = StudentRegistrationForm()  # Create an empty form for GET requests
    
    return render(request, 'sdm/register.html', {'form': form})  # Pass the form to the template

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'sdm/student_display.html', {'student_name': request.user.username})

