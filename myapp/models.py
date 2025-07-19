from django.db import models
from django.contrib.auth.models import User

# This model will store a flag to determine the user type after registration
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Doctor-specific profile information
class Doctor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    # Add other doctor-specific fields here
    
    def __str__(self):
        return f"Dr. {self.user_profile.user.first_name} {self.user_profile.user.last_name}"

# Patient-specific profile information
class Patient(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField()
    medical_history = models.TextField(blank=True, null=True)
    # Add other patient-specific fields here

    def __str__(self):
        return f"Patient: {self.user_profile.user.first_name} {self.user_profile.user.last_name}"