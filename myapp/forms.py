# myapp/forms.py

from django import forms
from django.contrib.auth.models import User
# Make sure UserProfile is NOT imported here
from .models import Doctor, Patient

# This form creates the main User object (for username, password, etc.)
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

# This form is for the extra Doctor details
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        # Note: We do NOT include the 'user' or 'doctor_id' fields here,
        # as they are handled automatically in the view and model.
        fields = ('specialization', 'license_number')

# This form is for the extra Patient details
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        # Note: We do NOT include the 'user' or 'patient_id' fields here.
        fields = ('date_of_birth', 'medical_history')

class UserUpdateForm(forms.ModelForm):
    # We don't want users to change their email this way, but you can add it if you want
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class DoctorProfileUpdateForm(forms.ModelForm):
    # specializations = forms.ModelMultipleChoiceField(
    #     queryset=Specialization.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False,
    # )
    class Meta:
        model = Doctor
        # Users can update these fields
        fields = ['specialization']
        # widgets = {
        #     'specializations': forms.CheckboxSelectMultiple,  # or SelectMultiple
        # }

class PatientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        # Users can update these fields
        fields = ['date_of_birth', 'medical_history', 'contact_number', 'blood_group', 'gender', 'allergies']
