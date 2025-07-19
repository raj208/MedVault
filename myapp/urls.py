from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Main registration page
    path('register/', views.register, name='register'),
    
    # Role-specific registration pages
    path('register/doctor/', views.doctor_register, name='doctor_register'),
    path('register/patient/', views.patient_register, name='patient_register'),
    
    # Login and Logout
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboards
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Homepage
    path('', views.home, name='home'),
]
