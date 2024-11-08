from django.db import models
from django.utils import timezone

class Admin(models.Model):
    admin_user = models.CharField(max_length=100)
    admin_pass = models.CharField(max_length=100)
    admin_email = models.CharField(max_length=100, primary_key=True)
    
    def __str__(self):
        return f"{self.admin_user}"

class Teacher(models.Model):
    teacher_name = models.CharField(max_length=200)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.teacher_name}"

class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)
    teachers = models.ManyToManyField(Teacher, related_name='subjects')

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.name

class Student(models.Model):
    student_name = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)
    enrolled_courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return self.student_name

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"