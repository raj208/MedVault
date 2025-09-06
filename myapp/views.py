# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserForm, DoctorForm, PatientForm, UserUpdateForm, DoctorProfileUpdateForm, PatientProfileUpdateForm
from .models import User, Doctor, Patient # We no longer import UserProfile
from django.contrib import messages # Import the messages framework


def home(request):
    return render(request, 'users/home.html')


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
            
            # Create the Doctor profile, linking it directly to the user
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save() # The custom ID is generated here by the model's save() method
            
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

            # Create the Patient profile, linking it directly to the user
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save() # The custom ID is generated here by the model's save() method
            
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
    We use hasattr() to check if a related doctor or patient object exists.
    """
    if hasattr(request.user, 'doctor'):
        return redirect('doctor_dashboard')
    elif hasattr(request.user, 'patient'):
        return redirect('patient_dashboard')
    else:
        # Handle cases for other users (like superuser) or redirect to a default page
        return redirect('home')

@login_required
def doctor_dashboard(request):
    return render(request, 'users/doctor_dashboard.html')

@login_required
def patient_dashboard(request):
    return render(request, 'users/patient_dashboard.html')



@login_required
def update_profile(request):
    profile_form = None # Initialize profile_form to None
    
    if request.method == 'POST':
        # Instantiate the form with the POST data and the user's current instance
        user_form = UserUpdateForm(request.POST, instance=request.user)

        # Check if the user is a doctor or patient to use the correct profile form
        if hasattr(request.user, 'doctor'):
            profile_form = DoctorProfileUpdateForm(request.POST, instance=request.user.doctor)
        elif hasattr(request.user, 'patient'):
            profile_form = PatientProfileUpdateForm(request.POST, instance=request.user.patient)

        # Check if both forms are valid
        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            
            # Add a success message
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('dashboard_redirect')

    else:
        # If it's a GET request, pre-fill the form with the user's current data
        user_form = UserUpdateForm(instance=request.user)
        
        if hasattr(request.user, 'doctor'):
            profile_form = DoctorProfileUpdateForm(instance=request.user.doctor)
        elif hasattr(request.user, 'patient'):
            profile_form = PatientProfileUpdateForm(instance=request.user.patient)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'users/update_profile.html', context)
