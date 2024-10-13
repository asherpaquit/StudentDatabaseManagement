from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student

class StudentRegistrationForm(UserCreationForm):
    student_name = forms.CharField(max_length=100, required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'student_name')

    def save(self, commit=True):
        user = super().save(commit)
        student = Student(user=user, student_name=self.cleaned_data['student_name'])
        student.save()  # Save the student instance with the automatically generated student number
        return user

