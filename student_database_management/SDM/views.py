from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .models import Student, Teacher, Grade, Course

# Existing functions...

def student_display(request):
    students = Student.objects.all()  
    return render(request, 'sdm/student_display.html', {'students': students})

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
    return render(request, 'sdm/home.html', {'student_name': student_name})

@login_required
def studentservice(request):
    student_name = request.session.get('student_name')
    email = request.session.get('email')

    try:
        student = Student.objects.get(email=email)
        return render(request, 'sdm/studentservice.html', {
            'student_name': student_name,
            'student_email': email,
            'student': student
        })
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect('login')

@login_required
def admission(request):
    if request.method == "POST":
        student_name = request.POST.get('student_name')
        email = request.POST.get('email')
        course_interest = request.POST.get('course_interest')

        if student_name and email and course_interest:
            messages.success(request, "Admission application submitted successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'sdm/admission.html')

# Custom login and logout views for teachers and students
class CustomLoginView(LoginView):
    template_name = 'sdm/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'

# Teacher registration and login
def register_teacher(request):
    if request.method == "POST":
        teacher_name = request.POST['teacher_name']
        email = request.POST['email']
        password = make_password(request.POST['password'])
        subject = request.POST['subject']

        try:
            teacher = Teacher(teacher_name=teacher_name, email=email, password=password, subject=subject)
            teacher.save()
            messages.success(request, "Teacher registered successfully!")
            return redirect('teacher_login')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'sdm/register_teacher.html')

def login_teacher(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            teacher = Teacher.objects.get(email=email)
            if check_password(password, teacher.password):
                request.session['teacher_name'] = teacher.teacher_name
                request.session['teacher_email'] = teacher.email
                return redirect('teacher_dashboard')
            else:
                messages.error(request, "Invalid password.")
        except Teacher.DoesNotExist:
            messages.error(request, "Teacher not found.")

    return render(request, 'sdm/login_teacher.html')

@login_required
def teacher_dashboard(request):
    teacher_name = request.session.get('teacher_name')
    teacher_email = request.session.get('teacher_email')

    try:
        teacher = Teacher.objects.get(email=teacher_email)
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher not found.")
        return redirect('login_teacher')

    if request.method == "POST":
        if 'add_grade' in request.POST:
            student_email = request.POST['student_email']
            grade_value = request.POST['grade']
            try:
                student = Student.objects.get(email=student_email)
                grade = Grade(student=student, teacher=teacher, subject=teacher.subject, grade=grade_value)
                grade.save()
                messages.success(request, f"Grade {grade_value} added for {student.student_name}.")
                return redirect('teacher_dashboard')
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")
        elif 'enroll_student' in request.POST:
            student_email = request.POST['student_email']
            try:
                student = Student.objects.get(email=student_email)
                course, created = Course.objects.get_or_create(name=teacher.subject, teacher=teacher)
                if course not in student.enrolled_courses.all():
                    student.enrolled_courses.add(course)
                    messages.success(request, f"{student.student_name} has been enrolled in {teacher.subject}.")
                else:
                    messages.info(request, f"{student.student_name} is already enrolled in {teacher.subject}.")
                return redirect('teacher_dashboard')
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")

    students = Student.objects.all()
    return render(request, 'sdm/teacher_dashboard.html', {
        'teacher_name': teacher_name,
        'students': students,
        'teacher': teacher,
    })


# @login_required
# def add_grade(request):
#     if request.method == "POST":
#         student_email = request.POST['student_email']
#         grade_value = request.POST['grade']
#         teacher_email = request.session.get('teacher_email')
        
#         try:
#             student = Student.objects.get(email=student_email)
#             teacher = Teacher.objects.get(email=teacher_email)
            
#             grade = Grade(student=student, teacher=teacher, subject=teacher.subject, grade=grade_value)
#             grade.save()
#             messages.success(request, f"Grade {grade_value} added for {student.student_name}.")
#         except Student.DoesNotExist:
#             messages.error(request, "Student not found.")
#         except Teacher.DoesNotExist:
#             messages.error(request, "Teacher not found.")

#     return render(request, 'sdm/add_grade.html')