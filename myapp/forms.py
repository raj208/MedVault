# myapp/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Doctor
# Make sure UserProfile is NOT imported here
from .models import Doctor, Patient

# This form creates the main User object (for username, password, etc.)
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

# # This form is for the extra Doctor details
# class DoctorForm(forms.ModelForm):
#     class Meta:
#         model = Doctor
#         # Note: We do NOT include the 'user' or 'doctor_id' fields here,
#         # as they are handled automatically in the view and model.
#         fields = ('specialization', 'license_number')

# doctors/forms.py


# If you exposed LANGUAGE_CODES in models.py, you can import it.
# Otherwise define choices here:
LANGUAGE_CHOICES = [
    ('en','English'), ('hi','Hindi'), ('bn','Bengali'), ('te','Telugu'),
    ('ta','Tamil'), ('mr','Marathi'), ('gu','Gujarati'), ('kn','Kannada'),
    ('ml','Malayalam'), ('pa','Punjabi'),
]

class DoctorForm(forms.ModelForm):
    # UI helpers that map into JSON fields:
    specialties_input = forms.CharField(
        label="Specialties (comma-separated)",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Cardiology, Internal Medicine"})
    )
    treatments_input = forms.CharField(
        label="Treatments (comma-separated)",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Angioplasty, ECG, ..."})
    )
    languages = forms.MultipleChoiceField(
        choices=LANGUAGE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Doctor
        # Do NOT expose user/doctor_id/text_block/geo/timestamps here
        exclude = (
            "user", "doctor_id", "specialties", "treatments", "text_block",
            "latitude", "longitude", "created_at", "updated_at",
        )
        fields = (
            "license_number", "years_of_experience", "hospital", "about",
            "city", "pincode", "phone","is_active", "languages",
            # The two virtual inputs live on the form (not the model fields):
            # specialties_input, treatments_input
        )

    # --- Cleaners: turn comma-separated strings into Python lists ---
    def clean_specialties_input(self):
        raw = self.cleaned_data.get("specialties_input", "")
        return [s.strip() for s in raw.split(",") if s.strip()]

    def clean_treatments_input(self):
        raw = self.cleaned_data.get("treatments_input", "")
        return [t.strip() for t in raw.split(",") if t.strip()]

    # --- Save: push lists into the model’s JSONFields ---
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.specialties = self.cleaned_data.get("specialties_input", [])
        instance.treatments = self.cleaned_data.get("treatments_input", [])
        if commit:
            instance.save()
        return instance

    # --- Editing existing doctor: prefill the virtual fields ---
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["specialties_input"].initial = ", ".join(self.instance.specialties or [])
            self.fields["treatments_input"].initial = ", ".join(self.instance.treatments or [])


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
