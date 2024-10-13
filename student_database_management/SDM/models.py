from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_number = models.CharField(max_length=15, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.student_number:  # Check if student_number is empty
            last_student = Student.objects.order_by('id').last()  # Get the last student
            if last_student:
                # Extract the numeric part of the student_number and increment it
                last_number = int(last_student.student_number.split('-')[-1])  # Increment last number
                new_number = last_number + 1
                self.student_number = f"24-0000-{new_number:03}"  # Generate new student number
            else:
                self.student_number = "24-0000-000"  # Starting point if no students exist
        super().save(*args, **kwargs)  # Call the original save method
        
    def __str__(self):
        return self.student_name
    
class Teacher(models.Model):
    id = models.IntegerField(primary_key=True)
    teacher_name = models.CharField(max_length=200)
    teacher_number = models.CharField(max_length=200)

    def __str__(self):
        return self.teacher_name
