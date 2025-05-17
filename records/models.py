from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


# Extend user for patients and doctors
class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    public_key = models.TextField(blank=True, null=True)  # For crypto-based auth
    private_key = models.TextField(blank=True, null=True) # Not recommended to store raw, use secure approach

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    allergies = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    previous_diagnoses = models.TextField(blank=True)

class MedicalDocument(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='documents/')
    verified = models.BooleanField(default=False)
    description = models.TextField(blank=True)

class AccessRequest(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="access_requests")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)
