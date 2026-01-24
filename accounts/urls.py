from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('features/', views.features_view, name='features'),
    path('logout/', views.logout_view, name='logout'),
    path('caregiver-dashboard/', views.caregiver_dashboard, name='caregiver_dashboard'),
    path('family-dashboard/', views.family_dashboard, name='family_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    # Role-specific profile pages
    path('caregiver-profile/', views.caregiver_profile, name='caregiver_profile'),
    path('family-profile/', views.family_profile, name='family_profile'),
    path('doctor-profile/', views.doctor_profile, name='doctor_profile'),
    # Role-specific home pages
    path('caregiver-home/', views.caregiver_home, name='caregiver_home'),
    path('family-home/', views.family_home, name='family_home'),
    path('doctor-home/', views.doctor_home, name='doctor_home'),
    # Role-specific features pages
    path('caregiver-features/', views.caregiver_features, name='caregiver_features'),
    path('family-features/', views.family_features, name='family_features'),
    path('doctor-features/', views.doctor_features, name='doctor_features'),
]
