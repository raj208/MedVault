# myapp/models.py
import uuid  # Import the built-in uuid library

from django.db import models
from django.contrib.auth.models import User

# NOTE: The UserProfile model has been removed.
# We now link Doctor and Patient directly to Django's built-in User model.

class Doctor(models.Model):
    # Direct link to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='doctor')
    
    # Field to store the custom, auto-generated ID
    doctor_id = models.CharField(max_length=20, unique=True, blank=True)
    
    # Doctor-specific fields
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        # Access the user's name directly via the 'user' field
        return f"Dr. {self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a unique ID for new doctors.
        """
        # This logic runs only when a new Doctor is being created
        if not self.doctor_id:
            # Find the last doctor created to determine the next ID number
            last_doctor = Doctor.objects.all().order_by('pk').last()
            if not last_doctor:
                # This is the very first doctor
                self.doctor_id = 'DOC-001'
            else:
                # Get the number from the last ID and increment it
                last_id_num = int(last_doctor.doctor_id.split('-')[1])
                new_id_num = last_id_num + 1
                # Format the new ID with leading zeros (e.g., DOC-002)
                self.doctor_id = f'DOC-{new_id_num:03d}'
        
        # Call the original save method to save the instance to the database
        super().save(*args, **kwargs)


class Patient(models.Model):
    # Direct link to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='patient')

    # Field to store the custom, auto-generated ID
    patient_id = models.CharField(max_length=20, unique=True, blank=True)

    private_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Patient-specific fields
    date_of_birth = models.DateField()
    medical_history = models.TextField(blank=True, null=True)

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