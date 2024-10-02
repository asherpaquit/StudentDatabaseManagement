from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Student
        fields = ['student_name']

    def save(self, commit=True):
        user = User.objects.create_user(self.cleaned_data['username'], password=self.cleaned_data['password'])
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student
