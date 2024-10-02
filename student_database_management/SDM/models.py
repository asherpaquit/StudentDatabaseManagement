from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)

    def __str__(self):
        return self.student_name
    
class Teacher(models.Model):
    id = models.IntegerField(primary_key=True)
    teacher_name = models.CharField(max_length=200)
    teacher_number = models.CharField(max_length=200)

    def __str__(self):
        return self.teacher_name
