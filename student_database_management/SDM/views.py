from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from .models import Student, Teacher, Grade, Course, Admin, CourseTeacher, CourseEnrollment

# Function to display all students
def student_display(request):
    students = Student.objects.all()
    return render(request, 'sdm/student_display.html', {'students': students})

# Function to register a student
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

# Function to handle admin login
def login_admin(request):
    if request.method == "POST":
        admin_email = request.POST['admin_email']
        admin_pass = request.POST['admin_pass']

        try:
            admin = Admin.objects.get(admin_email=admin_email)
            if check_password(admin_pass, admin.admin_pass):
                messages.success(request, "Login successful!")
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        except Admin.DoesNotExist:
            messages.error(request, "Admin not found.")

    return render(request, 'sdm/login_admin.html')

# Scholarship and Financial Aid page
def scholarship(request):
    if request.method == "POST":
        # Process scholarship or financial aid form submission if applicable
        student_email = request.POST.get('email')
        try:
            student = Student.objects.get(email=student_email)
            messages.success(request, f"Scholarship details for {student.student_name} will be processed.")
        except Student.DoesNotExist:
            messages.error(request, "Student not found.")
        return redirect('scholarship')

    scholarship_requirements = {
        'eligible_grades': ['A+', 'A', 'B+'],
        'financial_documents': ['Proof of income', 'Tax returns', 'Other supporting documents']
    }
    return render(request, 'sdm/scholarship.html', {'requirements': scholarship_requirements})

# Register an admin
def register_admin(request):
    if request.method == "POST":
        admin_user = request.POST['admin_user']
        admin_email = request.POST['admin_email']
        admin_pass = request.POST['admin_pass']
        confirm_admin_pass = request.POST['confirm_admin_pass']

        if admin_pass != confirm_admin_pass:
            messages.error(request, "Passwords do not match.")
            return redirect('register_admin')

        try:
            admin = Admin(admin_user=admin_user, admin_email=admin_email, admin_pass=make_password(admin_pass))
            admin.save()
            messages.success(request, "Admin registered successfully")
            return redirect('register_admin')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'sdm/register_admin.html')

@login_required
def admin_dashboard(request):
    teachers = Teacher.objects.all()
    courses = Course.objects.all()
    students = Student.objects.all()

    if request.method == "POST":
        # Handle course creation
        if 'add_course' in request.POST:
            course_name = request.POST['course_name']
            teacher_email = request.POST['teacher_email']

            if Course.objects.filter(name=course_name).exists():
                messages.error(request, "Course already exists.")
            else:
                new_course = Course.objects.create(name=course_name)
                messages.success(request, f"Course '{course_name}' created successfully.")

                if teacher_email:
                    try:
                        teacher = Teacher.objects.get(email=teacher_email)
                        CourseTeacher.objects.create(course=new_course, teacher=teacher)
                        messages.success(request, f"Teacher {teacher.teacher_name} assigned to {new_course.name}.")
                    except Teacher.DoesNotExist:
                        messages.error(request, "Teacher not found.")
            
            return redirect('admin_dashboard')

        elif 'assign_teacher' in request.POST:
            course_id = request.POST['course_id']
            teacher_email = request.POST['teacher_email']

            try:
                course = Course.objects.get(id=course_id)
                teacher = Teacher.objects.get(email=teacher_email)
                CourseTeacher.objects.create(course=course, teacher=teacher)
                messages.success(request, f"Teacher {teacher.teacher_name} assigned to {course.name}.")
            except Course.DoesNotExist:
                messages.error(request, "Course not found.")
            except Teacher.DoesNotExist:
                messages.error(request, "Teacher not found.")
            return redirect('admin_dashboard')

        elif 'enroll_student' in request.POST:
            course_id = request.POST['course_id']
            student_email = request.POST['student_email']

            try:
                course = Course.objects.get(id=course_id)
                student = Student.objects.get(email=student_email)
                CourseEnrollment.objects.create(course=course, student=student)
                messages.success(request, f"Student {student.student_name} enrolled in {course.name}.")
            except Course.DoesNotExist:
                messages.error(request, "Course not found.")
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")
            return redirect('admin_dashboard')

    context = {
        'teachers': teachers,
        'courses': courses,
        'students': students,
    }

    return render(request, 'sdm/admin_dashboard.html', context)

# Other functions for student login, profile update, etc.

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
def update_student_details(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            messages.error(request, 'Student not found.')
            return redirect('update_student')

        student_name = request.POST.get('student_name')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not check_password(old_password, student.password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('update_student')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('update_student')

        student.student_name = student_name
        if new_password:
            student.password = make_password(new_password)
        student.save()

        messages.success(request, 'Your details have been updated.')
        return redirect('studentservice')

    return render(request, 'sdm/update_student.html')

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
        courses_with_grades = [
            {'course': course.name, 'grade': (Grade.objects.filter(student=student, course=course).first() or {}).get('grade', 'N/A')}
            for course in student.enrolled_courses.all()
        ]
        return render(request, 'sdm/studentservice.html', {
            'student_name': student_name,
            'student_email': email,
            'courses_with_grades': courses_with_grades,
        })
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect('login')