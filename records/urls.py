from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/upload/', views.upload_document, name='upload_document'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_document, name='upload_document'),
    path('delete/<int:doc_id>/', views.delete_document, name='delete_document'),

]

