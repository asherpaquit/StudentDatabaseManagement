
from django.db import models
from django.utils import timezone

# Admin model remains unchanged
class Admin(models.Model):
    admin_user = models.CharField(max_length=100)
    admin_pass = models.CharField(max_length=100)
    admin_email = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return f"{self.admin_user}"

# Teacher model with many-to-many relationship to courses
class Teacher(models.Model):
    teacher_name = models.CharField(max_length=200)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128)
    courses = models.ManyToManyField('Course', through='CourseTeacher')  # Use a through model

    def __str__(self):
        return f"{self.teacher_name}"

# Course model with many-to-many relationship to teachers
class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)
    teachers = models.ManyToManyField(Teacher, through='CourseTeacher')  # Use a through model

    def __str__(self):
        return self.name

# Student model with many-to-many relationship to courses
class Student(models.Model):
    student_name = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)
    enrolled_courses = models.ManyToManyField(Course, through='CourseEnrollment')  # Use a through model

    def __str__(self):
        return self.student_name

# Grade model with foreign keys to student, teacher, and course
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student} - {self.course}: {self.grade}"

# CourseTeacher model as a through model to manage the many-to-many relationship between teachers and courses
class CourseTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher.teacher_name} teaches {self.course.name}"

# CourseEnrollment model as a through model to manage the many-to-many relationship between students and courses
class CourseEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.student_name} enrolled in {self.course.name}"
