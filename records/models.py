from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Extend user for patients and doctors
# class User(AbstractUser):
#     is_patient = models.BooleanField(default=False)
#     is_doctor = models.BooleanField(default=False)
#     public_key = models.TextField(blank=True, null=True)  # For crypto-based auth
#     private_key = models.TextField(blank=True, null=True) # Not recommended to store raw, use secure approach

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    public_key = models.TextField(blank=True, null=True)  # change from CharField to TextField
    dob = models.DateField(null=True, blank=True)
    aadhar_number = models.CharField(max_length=12, null=True, blank=True)

    def is_doctor(self):
        return self.role == 'doctor'

    def is_patient(self):
        return self.role == 'patient'

class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # allergies = models.TextField(blank=True)
    # current_medications = models.TextField(blank=True)
    # previous_diagnoses = models.TextField(blank=True)
    aadhar_number = models.CharField(max_length=12, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    public_key = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        if self.aadhar_number and self.date_of_birth:
            self.public_key = f"{self.aadhar_number}{self.date_of_birth.strftime('%d%m%Y')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username



class MedicalDocument(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='documents/')
    verified = models.BooleanField(default=False)
    description = models.TextField(blank=True)

class AccessRequest(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="access_requests")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    public_key = models.CharField(max_length=255, blank=True, null=True)  # For patient
    private_key = models.CharField(max_length=255, blank=True, null=True)  # For patient
