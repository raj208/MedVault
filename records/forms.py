from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('patient', 'Patient'), ('doctor', 'Doctor')])
    patient_public_key = forms.CharField(required=False, help_text="For doctors only")




class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    # Add Aadhar Number and DOB fields
    aadhar_number = forms.CharField(required=False, label="Aadhar Number")
    date_of_birth = forms.DateField(
        required=False,
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'role', 'aadhar_number', 'date_of_birth')