# myapp/models.py
import uuid  # Import the built-in uuid library

from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import RegexValidator
from django.utils import timezone

# NOTE: The UserProfile model has been removed.
# We now link Doctor and Patient directly to Django's built-in User model.

# class Specialization(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name


# class Doctor(models.Model):
#     # Direct link to the User model
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='doctor')
    
#     # Field to store the custom, auto-generated ID
#     doctor_id = models.CharField(max_length=20, unique=True, blank=True)
    
#     # Doctor-specific fields
#     # specialization = models.ManyToManyField(Specialization, blank=True)
#     specialization = models.TextField(blank=True, null= True)
#     license_number = models.CharField(max_length=50, unique=True)
    
#     def __str__(self):
#         # Access the user's name directly via the 'user' field
#         return f"Dr. {self.user.first_name} {self.user.last_name}"

#     def save(self, *args, **kwargs):
#         """
#         Overrides the save method to generate a unique ID for new doctors.
#         """
#         # This logic runs only when a new Doctor is being created
#         if not self.doctor_id:
#             # Find the last doctor created to determine the next ID number
#             last_doctor = Doctor.objects.all().order_by('pk').last()
#             if not last_doctor:
#                 # This is the very first doctor
#                 self.doctor_id = 'DOC-001'
#             else:
#                 # Get the number from the last ID and increment it
#                 last_id_num = int(last_doctor.doctor_id.split('-')[1])
#                 new_id_num = last_id_num + 1
#                 # Format the new ID with leading zeros (e.g., DOC-002)
#                 self.doctor_id = f'DOC-{new_id_num:03d}'
        
#         # Call the original save method to save the instance to the database
#         super().save(*args, **kwargs)
# doctors/models.py


LANGUAGE_CODES = {"en","hi","bn","te","ta","mr","gu","kn","ml","pa"}

def validate_language_list(value):
    if not isinstance(value, list):
        raise ValueError("languages must be a list of ISO-639-1 codes")
    bad = [v for v in value if v not in LANGUAGE_CODES]
    if bad:
        raise ValueError(f"Unsupported language codes: {bad}")

class Doctor(models.Model):
    # keep your OneToOne PK and doctor_id logic
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='doctor')
    doctor_id = models.CharField(max_length=20, unique=True, blank=True)

    # --- list-like fields now use JSONField ---
    name = models.CharField(max_length=200, blank=True)
    specialties = models.JSONField(default=list, blank=True)   # e.g. ["Cardiology","Internal Medicine"]
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    hospital = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    treatments = models.JSONField(default=list, blank=True)    # e.g. ["Angioplasty","ECG"]
    city = models.CharField(max_length=120, blank=True, default="")
    pincode = models.CharField(max_length=10, db_index=True, blank=True, default="")
    languages = models.JSONField(default=list, blank=True, validators=[validate_language_list])
    phone = models.CharField(
        max_length=30, blank=True,
        validators=[RegexValidator(r'^[0-9+\-\s]+$', 'Use digits, +, -, and spaces only.')]
    )
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    # optional/back-compat with your earlier field
    specialization = models.TextField(blank=True, null=True)

    # geo + timestamps + cached text
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    text_block = models.TextField(blank=True)

    def __str__(self):
        display = self.name.strip() if self.name else f"{self.user.first_name} {self.user.last_name}".strip()
        return f"Dr. {display}".strip() or f"Dr. {self.user.username}"

    def build_text_block(self) -> str:
        spec = ", ".join(self.specialties) if self.specialties else ""
        trt = ", ".join(self.treatments) if self.treatments else ""
        about = self.about or ""
        hosp = self.hospital or ""
        return (
            f"Specialties: {spec}.\n"
            f"About: {about}\n"
            f"Treatments: {trt}\n"
            f"Hospital: {hosp}."
        )

    def save(self, *args, **kwargs):
        # Autogenerate doctor_id (DOC-001 style)
        if not self.doctor_id:
            last = Doctor.objects.order_by('doctor_id').last()
            if not last or not last.doctor_id:
                self.doctor_id = 'DOC-001'
            else:
                try:
                    n = int(last.doctor_id.split('-')[1]) + 1
                except Exception:
                    n = 1
                self.doctor_id = f'DOC-{n:03d}'

        if not self.name:
            full = f"{self.user.first_name} {self.user.last_name}".strip()
            self.name = full or self.user.get_username()

        self.text_block = self.build_text_block()
        super().save(*args, **kwargs)



class Allergy(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=50, choices=[('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')], blank=True)

    def __str__(self):
        return self.name

class Patient(models.Model):
    # Direct link to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='patient')

    # Field to store the custom, auto-generated ID
    patient_id = models.CharField(max_length=20, unique=True, blank=True)

    private_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Patient-specific fields
    @property
    def age(self):
        if self.birth_date is None:
            return None
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
    
    date_of_birth = models.DateField(null=True, blank=True)

    medical_history = models.TextField(blank=True, null=True)

    contact_number = models.CharField(max_length=15, blank=True, null=True)
    # age = models.CharField(max_length=3, blank=False, null= False)          <p>Age: {{ patient.age }}</p> 
    blood_group = models.TextField(blank=False, null=False)
    allergies = models.ManyToManyField(Allergy, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        # Access the user's name directly via the 'user' field
        return f"Patient: {self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a unique ID for new patients.
        """
        # This logic runs only when a new Patient is being created
        if not self.patient_id:
            # Find the last patient created to determine the next ID number
            last_patient = Patient.objects.all().order_by('pk').last()
            if not last_patient:
                # This is the very first patient
                self.patient_id = 'PAT-001'
            else:
                # Get the number from the last ID and increment it
                last_id_num = int(last_patient.patient_id.split('-')[1])
                new_id_num = last_id_num + 1
                # Format the new ID with leading zeros (e.g., PAT-002)
                self.patient_id = f'PAT-{new_id_num:03d}'
        
        # Call the original save method to save the instance to the database
        super().save(*args, **kwargs)