from django.shortcuts import render, redirect
from .models import Student

# Create your views here.

def student_display(request):
    students = Student.objects.all()
    return render(request, 'sdm/student_display.html', {'students':students})
    
