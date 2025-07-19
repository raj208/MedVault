from django import forms
from django.contrib.auth.models import User
from .models import Doctor, Patient, UserProfile

# A common form for creating the base User object
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

# Form for Doctor specific details
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('specialization', 'license_number')

# Form for Patient specific details
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('date_of_birth', 'medical_history')
