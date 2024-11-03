from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .models import Student, Teacher, Grade, Course


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
    #Francis Nino Yap ----------#
    return render(request, 'sdm/home.html', {'student_name': student_name})

@login_required
def studentservice(request):
    student_name = request.session.get('student_name')
    email = request.session.get('email')

    try:
        # Fetch the student object
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
    

# Terence John Duterte ------------ #
class CustomLoginView(LoginView):
    template_name = 'sdm/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'  

# Teacher Registration (optional)
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

# Teacher Login
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

    course = Course.objects.filter(teacher=teacher, name=teacher.subject).first()
    students_with_grades = []
    enrolled_students = []
    non_enrolled_students = []

    if course:
        enrolled_students = Student.objects.filter(enrolled_courses=course)
        for student in enrolled_students:
            grade = Grade.objects.filter(student=student, subject=teacher.subject).first()
            students_with_grades.append({
                'student': student,
                'grade': grade.grade if grade else 'N/A'
            })
        non_enrolled_students = Student.objects.exclude(enrolled_courses=course)

    if request.method == "POST":
        # Handling adding grades
        if 'add_grade' in request.POST:
            student_email = request.POST['student_email']
            grade_value = request.POST['grade']
            try:
                student = Student.objects.get(email=student_email)
                if student in enrolled_students:
                    # Create and save the grade
                    grade, created = Grade.objects.update_or_create(
                        student=student, teacher=teacher, subject=teacher.subject,
                        defaults={'grade': grade_value}
                    )
                    messages.success(request, f"Grade {grade_value} added for {student.student_name}.")
                else:
                    messages.error(request, "Student not enrolled in your subject.")
                return redirect('teacher_dashboard')  # Redirect to avoid resubmission

            except Student.DoesNotExist:
                messages.error(request, "Student not found.")

        # Handling enrolling students
        elif 'enroll_student' in request.POST:
            student_email = request.POST['student_email']
            try:
                student = Student.objects.get(email=student_email)
                # Get or create the course for the teacher's subject
                course, created = Course.objects.get_or_create(name=teacher.subject, teacher=teacher)
                # Enroll the student in the course if not already enrolled
                if course not in student.enrolled_courses.all():
                    student.enrolled_courses.add(course)
                    messages.success(request, f"{student.student_name} has been enrolled in {teacher.subject}.")
                else:
                    messages.info(request, f"{student.student_name} is already enrolled in {teacher.subject}.")
                return redirect('teacher_dashboard')

            except Student.DoesNotExist:
                messages.error(request, "Student not found.")

        # Handling dropping students
        elif 'drop_student' in request.POST:
            student_email = request.POST['student_email']
            try:
                student = Student.objects.get(email=student_email)
                if course in student.enrolled_courses.all():
                    student.enrolled_courses.remove(course)
                    messages.success(request, f"{student.student_name} has been dropped from {teacher.subject}.")
                else:
                    messages.info(request, f"{student.student_name} is not enrolled in {teacher.subject}.")
                return redirect('teacher_dashboard')

            except Student.DoesNotExist:
                messages.error(request, "Student not found.")

    context = {
        'teacher_name': teacher_name,
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