from django import forms
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    student_name = forms.CharField(max_length=100, required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, help_text='Required.', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ('student_name', 'email')


