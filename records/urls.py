from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, doctor_search, patient_detail


from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.user_login, name='login'),
    # path('login/', views.custom_login_view, name='custom_login'), 
    path('login/', views.CustomLoginView.as_view(), name='login'),  # this is important
    path('doctor/search/', doctor_search, name='doctor_search'),
    path('patient/<int:patient_id>/detail/', patient_detail, name='patient_detail'),
    path('patient/<int:patient_id>/detail/', views.patient_detail, name='patient_detail'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/upload/', views.upload_document, name='upload_document'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_document, name='upload_document'),
    path('delete/<int:doc_id>/', views.delete_document, name='delete_document'),

]

