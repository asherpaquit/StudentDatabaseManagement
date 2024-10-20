from django.db import models


from django.db import models

from django.db import models
from django.utils import timezone

class Student(models.Model):
    student_name = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128)  
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.student_name



    
class Teacher(models.Model):
    id = models.IntegerField(primary_key=True)
    teacher_name = models.CharField(max_length=200)
    teacher_number = models.CharField(max_length=200)

    def __str__(self):
        return self.teacher_name
