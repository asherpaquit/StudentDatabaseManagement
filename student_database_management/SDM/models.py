from django.db import models

# Create your models here.
class Student(models.Model):
    student_name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    # id = models.IntegerField()
    teacher_name = models.CharField(max_length = 200)
    teacher_number = models.CharField(max_length = 200)


    def __str__(self):
        return self.title