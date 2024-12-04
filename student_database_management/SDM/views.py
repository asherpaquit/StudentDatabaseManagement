from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .models import Student, Teacher, Grade, Course, Admin,CourseTeacher, CourseEnrollment

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

def login_admin(request):
    if request.method == "POST":
        admin_email = request.POST['admin_email']
        admin_pass = request.POST['admin_pass']

        try:
            # Check if the admin exists
            admin = Admin.objects.get(admin_email=admin_email)
            # Check if the password matches
            if check_password(admin_pass, admin.admin_pass):
                # If the password is correct, log the user in
                # You can store the session or do other login related tasks
                messages.success(request, "Login successful!")
                return redirect('admin_dashboard')  # Replace 'dashboard' with your desired redirect page
            else:
                messages.error(request, "Invalid email or password.")
        except Admin.DoesNotExist:
            messages.error(request, "Admin not found.")

    return render(request, 'sdm/login_admin.html')

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

@login_required
def admin_dashboard(request):
    teachers = Teacher.objects.all()
    courses = Course.objects.all()
    students = Student.objects.all()

    # Create a list to hold course and teacher information
    courses_with_teachers = []
    for course in courses:
        teachers_assigned = CourseTeacher.objects.filter(course=course).select_related('teacher')
        for ct in teachers_assigned:
            courses_with_teachers.append({
                'course_id': course.id,
                'course_name': course.name,
                'teacher_email': ct.teacher.email,
                'teacher_name': ct.teacher.teacher_name
            })

    # Create a list to hold student information
    students_info = []
    for student in students:
        enrollments = CourseEnrollment.objects.filter(student=student).prefetch_related('course__courseteacher_set__teacher')
        student_courses = []
        for enrollment in enrollments:
            course = enrollment.course
            teacher = course.courseteacher_set.first().teacher if course.courseteacher_set.exists() else None
            student_courses.append({
                'course_name': course.name,
                'teacher_name': teacher.teacher_name if teacher else 'No teacher assigned'
            })
        students_info.append({
            'student_name': student.student_name,
            'student_email': student.email,
            'courses': student_courses
        })

    if request.method == "POST":
        # Handle course creation
        if 'add_course' in request.POST:
            course_name = request.POST['course_name']
            teacher_email = request.POST['teacher_email']

            # Check if course already exists
            if Course.objects.filter(name=course_name).exists():
                messages.error(request, "Course already exists.")
            else:
                # Create course without a teacher
                new_course = Course.objects.create(name=course_name)
                messages.success(request, f"Course '{course_name}' created successfully.")

                # If a teacher was selected, assign them to the course via the CourseTeacher model
                if teacher_email:
                    try:
                        teacher = Teacher.objects.get(email=teacher_email)
                        CourseTeacher.objects.create(course=new_course, teacher=teacher)
                        messages.success(request, f"Teacher {teacher.teacher_name} assigned to {new_course.name}.")
                    except Teacher.DoesNotExist:
                        messages.error(request, "Teacher not found.")
            
            return redirect('admin_dashboard')

        # Handle teacher assignment to course
        elif 'assign_teacher' in request.POST:
            course_id = request.POST['course_id']
            teacher_email = request.POST['teacher_email']

            try:
                # Get course and teacher
                course = Course.objects.get(id=course_id)
                teacher = Teacher.objects.get(email=teacher_email)
                
                # Use the CourseTeacher through model to assign the teacher to the course
                CourseTeacher.objects.create(course=course, teacher=teacher)
                messages.success(request, f"Teacher {teacher.teacher_name} assigned to {course.name}.")
            except Course.DoesNotExist:
                messages.error(request, "Course not found.")
            except Teacher.DoesNotExist:
                messages.error(request, "Teacher not found.")
            return redirect('admin_dashboard')

        # Handle student enrollment
        elif 'enroll_student' in request.POST:
            course_id = request.POST['course_id']
            teacher_email = request.POST['teacher_email']
            student_email = request.POST['student_email']

            try:
                # Get course, teacher, and student
                course = Course.objects.get(id=course_id)
                teacher = Teacher.objects.get(email=teacher_email)
                student = Student.objects.get(email=student_email)
                
                # Check if the course and teacher pair is valid
                if CourseTeacher.objects.filter(course=course, teacher=teacher).exists():
                    # Use the CourseEnrollment through model to enroll the student in the course
                    CourseEnrollment.objects.create(course=course, student=student)
                    messages.success(request, f"Student {student.student_name} enrolled in {course.name} with {teacher.teacher_name}.")
                else:
                    messages.error(request, "Invalid course and teacher combination.")
            except Course.DoesNotExist:
                messages.error(request, "Course not found.")
            except Teacher.DoesNotExist:
                messages.error(request, "Teacher not found.")
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")
            return redirect('admin_dashboard')

    context = {
        'teachers': teachers,
        'courses': courses,
        'students': students,
        'courses_with_teachers': courses_with_teachers,
        'students_info': students_info,
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
            grade = Grade.objects.filter(student=student, course=course).first()  # Use `course` field instead of `subject`
            courses_with_grades.append({
                'course': course.name,
                'grade': grade.grade if grade else 'N/A'
            })

        return render(request, 'sdm/studentservice.html', {
            'student_name': student_name,
            'student_email': email,
            'courses_with_grades': courses_with_grades,  # Pass courses with grades
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

        try:
            teacher = Teacher(teacher_name=teacher_name, email=email, password=password)
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
    teacher_email = request.session.get('teacher_email')

    try:
        teacher = Teacher.objects.get(email=teacher_email)
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher not found.")
        return redirect('login_teacher')

    # Get courses taught by this teacher
    courses = teacher.courses.all()
    students_with_grades = []

    for course in courses:
        # Get students enrolled in the course
        students_in_course = Student.objects.filter(enrolled_courses=course)
        for student in students_in_course:
            grade = Grade.objects.filter(student=student, course=course).first()
            students_with_grades.append({
                'student': student,
                'grade': grade.grade if grade else 'N/A',
                'course': course
            })

    enrolled_students = list(set([entry['student'] for entry in students_with_grades]))

    if request.method == "POST" and 'add_grade' in request.POST:
        student_email = request.POST['student_email']
        grade_value = request.POST['grade']
        course_name = request.POST['course_name']
        try:
            student = Student.objects.get(email=student_email)
            course = Course.objects.get(name=course_name)

            if course in student.enrolled_courses.all():
                grade, created = Grade.objects.update_or_create(
                    student=student, teacher=teacher, course=course,
                    defaults={'grade': grade_value}
                )
                messages.success(request, f"Grade {grade_value} added for {student.student_name} in {course.name}.")
            else:
                messages.error(request, "Student not enrolled in this course.")
            return redirect('teacher_dashboard')

        except Student.DoesNotExist:
            messages.error(request, "Student not found.")

    context = {
        'teacher_name': teacher.teacher_name,
        'students_with_grades': students_with_grades,
        'courses': courses,  # For displaying the courses the teacher is teaching
        'enrolled_students': enrolled_students,  # For adding grades to students
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