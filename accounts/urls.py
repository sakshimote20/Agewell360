from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('features/', views.features_view, name='features'),
    path('logout/', views.logout_view, name='logout'),
]
