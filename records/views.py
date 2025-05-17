from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from .models import MedicalDocument, PatientProfile
from django.contrib.auth.forms import UserCreationForm
from django import forms

def home(request):
    return render(request, 'records/home.html')

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
    patient_profile = PatientProfile.objects.get(user=request.user)
    documents = MedicalDocument.objects.filter(patient=patient_profile).order_by('-uploaded_at')
    return render(request, 'records/patient_dashboard.html', {
        'documents': documents,
        'profile': patient_profile,
    })

@login_required
def doctor_dashboard(request):
    return render(request, 'records/doctor_dashboard.html')


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




class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            if role == 'patient':
                user.is_patient = True
            elif role == 'doctor':
                user.is_doctor = True
            user.save()

            if user.is_patient:
                PatientProfile.objects.create(user=user)

            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'records/register.html', {'form': form})


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
