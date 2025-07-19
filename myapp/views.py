from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserForm, DoctorForm, PatientForm
from .models import UserProfile, Doctor, Patient

def register(request):
    """
    Main registration page where user chooses their role.
    """
    return render(request, 'users/register.html')

@transaction.atomic
def doctor_register(request):
    """
    Handles the registration process for a Doctor.
    """
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            # Create the base user
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            # Create the UserProfile with is_doctor set to True
            user_profile = UserProfile.objects.create(user=user, is_doctor=True)
            
            # Create the Doctor profile
            doctor = doctor_form.save(commit=False)
            doctor.user_profile = user_profile
            doctor.save()
            
            # Log the user in and redirect to their dashboard
            login(request, user)
            return redirect('doctor_dashboard')
    else:
        user_form = UserForm()
        doctor_form = DoctorForm()
    
    return render(request, 'users/doctor_register.html', {
        'user_form': user_form,
        'doctor_form': doctor_form
    })

@transaction.atomic
def patient_register(request):
    """
    Handles the registration process for a Patient.
    """
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        patient_form = PatientForm(request.POST)
        if user_form.is_valid() and patient_form.is_valid():
            # Create the base user
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Create the UserProfile with is_patient set to True
            user_profile = UserProfile.objects.create(user=user, is_patient=True)

            # Create the Patient profile
            patient = patient_form.save(commit=False)
            patient.user_profile = user_profile
            patient.save()
            
            # Log the user in and redirect to their dashboard
            login(request, user)
            return redirect('patient_dashboard')
    else:
        user_form = UserForm()
        patient_form = PatientForm()
        
    return render(request, 'users/patient_register.html', {
        'user_form': user_form,
        'patient_form': patient_form
    })

@login_required
def dashboard_redirect(request):
    """
    Redirects user to their specific dashboard based on their role.
    """
    if request.user.profile.is_doctor:
        return redirect('doctor_dashboard')
    elif request.user.profile.is_patient:
        return redirect('patient_dashboard')
    else:
        # Handle cases for other users or redirect to a default page
        return redirect('home') # You should create a homepage view

@login_required
def doctor_dashboard(request):
    # Add logic for the doctor's dashboard
    return render(request, 'users/doctor_dashboard.html')

@login_required
def patient_dashboard(request):
    # Add logic for the patient's dashboard
    return render(request, 'users/patient_dashboard.html')

def home(request):
    """
    A simple homepage.
    """
    return render(request, 'users/home.html')