from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .models import Student, Teacher, Grade, Course, Admin

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

def register_admin(request):
    if request.method == "POST":
        admin_user = request.POST['admin_user']
        admin_email = request.POST['admin_email']
        admin_pass = request.POST['admin_pass']
        confirm_admin_pass = request.POST['confirm_admin_pass']
        
        if admin_pass != confirm_admin_pass:
            messages.error(request, "Passwords do not match.")
            return redirect('registeradmin')

        try:
            admin = Admin(admin_user=admin_user, admin_email=admin_email, admin_pass=make_password(admin_pass))
            admin.save()
            messages.success(request, "Admin registered successfully")
            return redirect('registeradmin')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        
    return render(request, 'sdm/register_admin.html')

def login_admin(request):
    if request.method == "POST":
        admin_email = request.POST['email']
        admin_pass = request.POST['password']
        
        try:
            admin = Admin.objects.get(admin_email=admin_email)
            if check_password(admin_pass, admin.admin_pass):
                # Set session variables
                request.session['admin_user'] = admin.admin_user
                request.session['admin_email'] = admin.admin_email
                messages.success(request, "Login successful")
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid email or password")
        except Admin.DoesNotExist:
            messages.error(request, "Admin not found")
    
    return render(request, 'sdm/login_admin.html')


@login_required
def admin_dashboard(request):
    admin_user = request.session.get('admin_user')
    admin_email = request.session.get('admin_email')

    try:
        admin = Admin.objects.get(admin_email=admin_email)
    except Admin.DoesNotExist:
        messages.error(request, "Admin not found.")
        return redirect('login_admin')

    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    selected_teacher = None
    students_with_grades = []
    enrolled_students = []
    non_enrolled_students = []

    # Determine the active tab based on the URL parameter or default to 'select-teacher'
    active_tab = request.GET.get('tab', 'select-teacher')

    if request.method == "POST":
        if 'add_subject' in request.POST:
            subject_name = request.POST.get('subject_name')
            if subject_name:
                Subject.objects.get_or_create(name=subject_name)
                messages.success(request, f"Subject '{subject_name}' added.")
            active_tab = 'select-teacher'

        elif 'assign_subject' in request.POST:
            selected_teacher_email = request.POST.get('teacher_email')
            subject_name = request.POST.get('subject')
            try:
                selected_teacher = Teacher.objects.get(email=selected_teacher_email)
                subject = Subject.objects.get(name=subject_name)
                selected_teacher.subjects.add(subject)
                selected_teacher.save()
                messages.success(request, f"Subject '{subject_name}' assigned to {selected_teacher.teacher_name}.")
            except Teacher.DoesNotExist:
                messages.error(request, "Teacher not found.")
            except Subject.DoesNotExist:
                messages.error(request, "Subject not found.")
            active_tab = 'select-teacher'

        else:
            selected_teacher_email = request.POST.get('teacher_email')
            try:
                selected_teacher = Teacher.objects.get(email=selected_teacher_email)
                course = Course.objects.filter(teacher=selected_teacher, name=selected_teacher.subject).first()

                if course:
                    enrolled_students = Student.objects.filter(enrolled_courses=course)
                    for student in enrolled_students:
                        grade = Grade.objects.filter(student=student, subject=selected_teacher.subject).first()
                        students_with_grades.append({
                            'student': student,
                            'grade': grade.grade if grade else 'N/A'
                        })
                    non_enrolled_students = Student.objects.exclude(enrolled_courses=course)

                active_tab = 'dashboard'

            except Teacher.DoesNotExist:
                messages.error(request, "Teacher not found.")

    context = {
        'admin_user': admin_user,
        'teachers': teachers,
        'subjects': subjects,
        'selected_teacher': selected_teacher,
        'students_with_grades': students_with_grades,
        'students': enrolled_students,
        'non_enrolled_students': non_enrolled_students,
        'active_tab': active_tab,
    }

    return render(request, 'sdm/admin_dashboard.html', context)


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
        # Get the student using the email from the POST data or session
        email = request.POST.get('email')  # Make sure your form sends the email
        try:
            student = Student.objects.get(email=email)  # Get student based on the email from the form
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

        # Update student details
        student.student_name = student_name
        if new_password:
            student.password = make_password(new_password)  # Hash the new password
        student.save()

        messages.success(request, 'Your details have been updated.')
        return redirect('studentservice')  # Ensure you have a 'profile' URL

    # If GET request, render the update form
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
        
        # Prepare a list of courses with grades
        courses_with_grades = []
        for course in student.enrolled_courses.all():
            grade = Grade.objects.filter(student=student, subject=course.name).first()
            courses_with_grades.append({
                'course': course.name,
                'grade': grade.grade if grade else 'N/A'
            })

        return render(request, 'sdm/studentservice.html', {
            'student_name': student_name,
            'student_email': email,
            'courses_with_grades': courses_with_grades,  # Pass courses with grades
              # Assuming 'year' is a field in Student model
        })
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect('login')  # Redirect if the student is not found
    

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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Teacher, Student, Course, Grade

@login_required
def teacher_dashboard(request):
    teacher_name = request.session.get('teacher_name')
    teacher_email = request.session.get('teacher_email')

    try:
        teacher = Teacher.objects.get(email=teacher_email)
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher not found.")
        return redirect('login_teacher')

    # Get the list of subjects taught by this teacher
    subjects = teacher.subjects.all()
    
    selected_subject = request.GET.get('subject', None) if request.method == 'GET' else request.POST.get('selected_subject', None)
    course = Course.objects.filter(teacher=teacher, name=selected_subject).first() if selected_subject else None

    students_with_grades = []
    enrolled_students = []
    non_enrolled_students = []

    if course:
        enrolled_students = Student.objects.filter(enrolled_courses=course)
        for student in enrolled_students:
            grade = Grade.objects.filter(student=student, subject=selected_subject).first()
            students_with_grades.append({
                'student': student,
                'grade': grade.grade if grade else 'N/A'
            })
        non_enrolled_students = Student.objects.exclude(enrolled_courses=course)

    if request.method == "POST":
        selected_subject = request.POST.get('selected_subject')
        course, created = Course.objects.get_or_create(name=selected_subject, teacher=teacher)
        
        if 'add_grade' in request.POST:
            student_email = request.POST['student_email']
            grade_value = request.POST['grade']
            try:
                student = Student.objects.get(email=student_email)
                if student in enrolled_students:
                    grade, created = Grade.objects.update_or_create(
                        student=student, teacher=teacher, subject=selected_subject,
                        defaults={'grade': grade_value}
                    )
                    messages.success(request, f"Grade {grade_value} added for {student.student_name}.")
                else:
                    messages.error(request, "Student not enrolled in your subject.")
                return redirect('teacher_dashboard')  # Redirect to avoid resubmission

            except Student.DoesNotExist:
                messages.error(request, "Student not found.")
        
        elif 'enroll_student' in request.POST:
            student_email = request.POST['student_email']
            try:
                student = Student.objects.get(email=student_email)
                if course not in student.enrolled_courses.all():
                    student.enrolled_courses.add(course)
                    messages.success(request, f"{student.student_name} has been enrolled in {selected_subject}.")
                else:
                    messages.info(request, f"{student.student_name} is already enrolled in {selected_subject}.")
                return redirect('teacher_dashboard')
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")
        
        elif 'drop_student' in request.POST:
            student_email = request.POST['student_email']
            try:
                student = Student.objects.get(email=student_email)
                if course in student.enrolled_courses.all():
                    student.enrolled_courses.remove(course)
                    messages.success(request, f"{student.student_name} has been dropped from {selected_subject}.")
                else:
                    messages.info(request, f"{student.student_name} is not enrolled in {selected_subject}.")
                return redirect('teacher_dashboard')

            except Student.DoesNotExist:
                messages.error(request, "Student not found.")

    context = {
        'teacher_name': teacher_name,
        'subjects': subjects,
        'selected_subject': selected_subject,
        'students_with_grades': students_with_grades,
        'students': enrolled_students,  # For displaying grades
        'non_enrolled_students': non_enrolled_students,  # For enrollment form
    }

    return render(request, 'sdm/teacher_dashboard.html', context)


    # Elementary Level View
@login_required
def elementary(request):
    return render(request, 'sdm/elementary.html')

# Senior High Level View
@login_required
def senior_high(request):
    return render(request, 'sdm/senior_high.html')

# College Level View
@login_required
def college(request):
    return render(request, 'sdm/college.html')



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