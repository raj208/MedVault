from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Patient, PastSurgery, Doctor


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

    aadhar_number = forms.CharField(required=True, label="Aadhar Number")
    dob = forms.DateField(
        required=True,
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'role', 'aadhar_number', 'dob')



class PatientForm(forms.ModelForm):
    # aadhar_number = forms.CharField(required=False, label="Aadhar Number")
    # date_of_birth = forms.DateField(
    #     required=False,
    #     label="Date of Birth",
    #     widget=forms.DateInput(attrs={'type': 'date'})
    # )


    class Meta:
        model = Patient
        fields = [
            'first_name', 'middle_name', 'last_name' ,'age', 'gender', 'contact_number', 'email',
            'address', 'emergency_contact_name', 'emergency_contact_number',
            'blood_group', 'allergies', 'ongoing_medications'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
            'ongoing_medications': forms.Textarea(attrs={'rows': 2}),
        }

class PastSurgeryForm(forms.ModelForm):
    class Meta:
        model = PastSurgery
        fields = ['surgery_name', 'year', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization',  'experience_years'] 
        widgets = {
            'specialization': forms.Textarea(attrs={'rows': 2}),
        }
