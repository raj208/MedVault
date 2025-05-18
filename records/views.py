from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from .models import MedicalDocument, PatientProfile, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .forms import RegistrationForm


def home(request):
    return render(request, 'records/home.html')



class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.role == 'doctor':
            return reverse('doctor_search')  # Redirect to form to enter patient public key
        elif user.role == 'patient':
            return reverse('patient_dashboard')
        else:
            return reverse('home')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_patient:
                return redirect('patient_dashboard')
            elif user.is_doctor:
                return redirect('doctor_dashboard')
        else:
            return render(request, 'records/login.html', {'error': 'Invalid credentials'})
    return render(request, 'records/login.html')

from .models import MedicalDocument, PatientProfile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

@login_required
def patient_dashboard(request):
    """
    Renders the patient dashboard if a PatientProfile exists for the logged-in user.
    If not, displays an error message and a fallback page.
    """
    try:
        patient_profile = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        messages.error(request, "Patient profile does not exist for the current user.")
        return render(request, 'records/user_not_found.html')  # Or use: redirect('home')

    documents = MedicalDocument.objects.filter(patient=patient_profile).order_by('-uploaded_at')
    return render(request, 'records/patient_dashboard.html', {
        'documents': documents,
        'profile': patient_profile,
    })

@login_required
def doctor_dashboard(request):
    patient_id = request.session.get('view_patient_id')
    if not patient_id:
        return redirect('custom_login')

    patient_user = get_object_or_404(User, id=patient_id)
    patient_documents = MedicalDocument.objects.filter(patient__user=patient_user)

    return render(request, 'records/doctor_dashboard.html', {
        'patient_user': patient_user,
        'documents': patient_documents,
    })

@login_required
def upload_document(request):
    if request.method == 'POST':
        file = request.FILES['file']
        description = request.POST.get('description', '')
        patient_profile = PatientProfile.objects.get(user=request.user)
        MedicalDocument.objects.create(
            patient=patient_profile,
            file=file,
            description=description
        )
        return redirect('patient_dashboard')
    return HttpResponse(status=405)




# class RegistrationForm(UserCreationForm):
#     ROLE_CHOICES = (
#         ('patient', 'Patient'),
#         ('doctor', 'Doctor'),
#     )
#     role = forms.ChoiceField(choices=ROLE_CHOICES)

#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2', 'role')


from .forms import RegistrationForm


##UTILS
# import hashlib
# from .models import UserProfile, PatientProfile
# def generate_public_key(aadhar, dob):
#     data = f"{aadhar}_{dob}"
#     return hashlib.sha256(data.encode()).hexdigest()

# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import serialization

# def generate_public_key(aadhar, dob):
#     # You can optionally use aadhar/dob for some metadata or encryption later
#     private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
#     public_key = private_key.public_key()

#     pem_public_key = public_key.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     ).decode('utf-8')

#     return pem_public_key

from django.contrib.auth import get_user_model
from .utils import generate_public_key  # assuming this exists
from django.contrib import messages
User = get_user_model()

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             role = form.cleaned_data['role']
#             aadhar = form.cleaned_data.get('aadhar_number')
#             date_of_birth = form.cleaned_data.get('date_of_birth')

#             # Ensure required fields for patient
#             if role == 'patient' and (not aadhar or not date_of_birth):
#                 form.add_error(None, "Aadhar number and Date of Birth are required for patients.")
#                 return render(request, 'records/register.html', {'form': form})

#             user = form.save(commit=False)
#             user.role = role

#             if role == 'patient':
#                 user.aadhar_number = aadhar
#                 user.date_of_birth = date_of_birth
#                 user.public_key = generate_public_key(aadhar, date_of_birth)

#             user.save()

#             # Create associated profiles
#             UserProfile.objects.create(user=user, role=role)

#             if role == 'patient':
#                 PatientProfile.objects.create(user=user, aadhar_number=aadhar, date_of_birth=date_of_birth)

#             messages.success(request, "Registration successful. Please log in.")
#             return redirect('login')
#     else:
#         form = RegistrationForm()

#     return render(request, 'records/register.html', {'form': form})

from .forms import RegistrationForm, PatientForm, PastSurgeryForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        patient_form = PatientForm(request.POST) if request.POST.get('role') == 'patient' else None
        past_Surgery_form = PastSurgeryForm(request.POST) if request.POST.get('role') == 'patient' else None

        if form.is_valid() and (not patient_form or patient_form.is_valid()):
            role = form.cleaned_data['role']
            aadhar = form.cleaned_data.get('aadhar_number')
            date_of_birth = form.cleaned_data.get('date_of_birth')

            # Required fields check
            if role == 'patient' and (not aadhar or not date_of_birth):
                form.add_error(None, "Aadhar number and Date of Birth are required for patients.")
                return render(request, 'records/register.html', {'form': form, 'patient_form': patient_form})

            user = form.save(commit=False)
            user.role = role

            if role == 'patient':
                user.aadhar_number = aadhar
                user.date_of_birth = date_of_birth
                user.public_key = generate_public_key(aadhar, date_of_birth)

            user.save()
            UserProfile.objects.create(user=user, role=role)

            if role == 'patient':
                PatientProfile.objects.create(user=user, aadhar_number=aadhar, date_of_birth=date_of_birth)

                # Save patient medical info
                patient = patient_form.save(commit=False)
                patient.user = user  # If Patient model has a ForeignKey to User
                patient.save()

            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = RegistrationForm()
        patient_form = PatientForm()
        past_Surgery_form = PastSurgeryForm()

    return render(request, 'records/register.html', {'form': form, 'patient_form': patient_form, 'past_Surgery_form': past_Surgery_form})


from .models import MedicalDocument, PatientProfile

@login_required
def delete_document(request, doc_id):
    # Get the logged-in user's patient profile
    patient_profile = get_object_or_404(PatientProfile, user=request.user)

    # Fetch the document owned by this patient
    document = get_object_or_404(MedicalDocument, id=doc_id, patient=patient_profile)

    document.file.delete()  # delete file from storage
    document.delete()       # delete record
    return redirect('patient_dashboard')




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm
from .models import UserProfile

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            patient_public_key = form.cleaned_data['patient_public_key']

            user = authenticate(username=username, password=password)

            if user:
                profile = UserProfile.objects.get(user=user)
                if role == 'patient' and profile.role == 'patient':
                    login(request, user)
                    return redirect('patient_dashboard')

                elif role == 'doctor' and profile.role == 'doctor':
                    try:
                        patient_profile = UserProfile.objects.get(public_key=patient_public_key, role='patient')
                        request.session['view_patient_id'] = patient_profile.user.id
                        login(request, user)
                        return redirect('doctor_dashboard')
                    except UserProfile.DoesNotExist:
                        form.add_error('patient_public_key', 'Invalid patient public key')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = CustomLoginForm()

    return render(request, 'records/login.html', {'form': form})


from .models import CustomUser
from .models import PatientProfile

@login_required
def doctor_search(request):
    if request.method == 'POST':
        public_key = request.POST.get('public_key')
        try:
            patient_profile = PatientProfile.objects.get(public_key=public_key)
            patient = patient_profile.user  # Get the associated CustomUser
            return redirect('patient_detail', patient_id=patient.id)
        except PatientProfile.DoesNotExist:
            return render(request, 'doctor/search.html', {'error': 'Patient not found'})
    return render(request, 'doctor/search.html')



from .models import MedicalDocument, CustomUser

@login_required
def patient_detail(request, patient_id):
    user = request.user
    if user.role != 'doctor':
        return render(request, '403.html')  # Only doctors allowed

    patient = get_object_or_404(CustomUser, id=patient_id, role='patient')
    patient_profile = patient.patientprofile
    documents = MedicalDocument.objects.filter(patient=patient_profile).order_by('-uploaded_at')

    context = {
        'patient': patient,
        'documents': documents,
    }
    return render(request, 'doctor/patient_details.html', context)


def patient_profile(request):
    user = request.user
    if user.role != 'patient':
        return render(request, '403.html')  # Only patients allowed

    patient_profile = get_object_or_404(PatientProfile, user=user)
    documents = MedicalDocument.objects.filter(patient=patient_profile).order_by('-uploaded_at')

    context = {
        'patient_profile': patient_profile,
        'documents': documents,
    }
    return render(request, 'records/profile_details.html', context)