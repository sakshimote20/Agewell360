from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile


def features_view(request):
    return render(request, 'accounts/features.html')


def login_view(request):
    if request.user.is_authenticated:
        # if already logged in, direct based on role and profile completion
        try:
            profile = request.user.profile
            if not profile.is_profile_completed:
                return redirect('profile')
            # Redirect based on role
            if profile.role == 'elderly':
                return redirect('home')
            elif profile.role == 'caregiver':
                return redirect('caregiver_dashboard')
            elif profile.role == 'family':
                return redirect('family_dashboard')
            elif profile.role == 'doctor':
                return redirect('doctor_dashboard')
        except Exception:
            pass
        return redirect('home')
    if request.method == 'POST':
        email_phone = request.POST.get('email_phone', '').strip()
        password = request.POST.get('password', '').strip()
        role = request.POST.get('role', '').strip()
        
        # Authenticate using email_phone as username
        user = authenticate(request, username=email_phone, password=password)
        if user is not None:
            login(request, user)
            # Ensure profile exists (role should already be set from signup)
            profile, _ = Profile.objects.get_or_create(user=user)
            
            if not profile.is_profile_completed:
                # Redirect to role-specific profile page
                if profile.role == 'elderly':
                    return redirect('profile')
                elif profile.role == 'caregiver':
                    return redirect('caregiver_profile')
                elif profile.role == 'family':
                    return redirect('family_profile')
                elif profile.role == 'doctor':
                    return redirect('doctor_profile')
                else:
                    return redirect('profile')
            
            # Redirect to role-specific home page after profile is completed
            if profile.role == 'elderly':
                return redirect('home')
            elif profile.role == 'caregiver':
                return redirect('caregiver_home')
            elif profile.role == 'family':
                return redirect('family_home')
            elif profile.role == 'doctor':
                return redirect('doctor_home')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid email/phone or password')
    return render(request, 'accounts/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email_phone = request.POST.get('email_phone', '').strip()
        password = request.POST.get('password', '').strip()
        password2 = request.POST.get('password2', '').strip()
        role = request.POST.get('role', '').strip()
        
        # Validate all fields are filled
        if not email_phone or not password or not password2 or not role:
            messages.error(request, 'Please fill all fields')
        # Validate passwords match
        elif password != password2:
            messages.error(request, 'Passwords do not match')
        # Validate password length
        elif len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
        # Use email_phone as username
        elif User.objects.filter(username=email_phone).exists():
            messages.error(request, 'This email/phone is already registered')
        else:
            # Create user with email_phone as username
            user = User.objects.create_user(username=email_phone, password=password, email=email_phone)
            # Store role in profile
            profile = user.profile
            profile.role = role
            profile.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    return render(request, 'accounts/signup.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    # GET shows profile; POST saves profile and marks as completed
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        age = request.POST.get('age')
        phone = request.POST.get('phone', '').strip()
        family_contact = request.POST.get('family_contact', '').strip()
        address = request.POST.get('address', '').strip()
        # Update profile
        profile.full_name = full_name
        try:
            profile.age = int(age) if age else None
        except ValueError:
            profile.age = None
        profile.phone = phone
        profile.family_contact = family_contact
        profile.address = address
        # handle uploaded photo if present
        if request.FILES.get('photo'):
            profile.photo = request.FILES['photo']
        # mark completed
        profile.is_profile_completed = True
        profile.save()
        # also update User.get_full_name if desired (optional)
        if full_name:
            request.user.first_name = full_name
            request.user.save()
        
        # Redirect to role-specific home page after profile completion
        if profile.role == 'elderly':
            return redirect('home')
        elif profile.role == 'caregiver':
            return redirect('caregiver_home')
        elif profile.role == 'family':
            return redirect('family_home')
        elif profile.role == 'doctor':
            return redirect('doctor_home')
        else:
            return redirect('home')

    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def caregiver_dashboard(request):
    """Caregiver dashboard - only accessible to caregivers"""
    profile = request.user.profile
    if profile.role != 'caregiver':
        return redirect('home')
    return render(request, 'dashboards/caregiver.html')


@login_required
def family_dashboard(request):
    """Family Member dashboard - only accessible to family members"""
    profile = request.user.profile
    if profile.role != 'family':
        return redirect('home')
    return render(request, 'dashboards/family.html')


@login_required
def doctor_dashboard(request):
    """Doctor dashboard - only accessible to doctors"""
    profile = request.user.profile
    if profile.role != 'doctor':
        return redirect('home')
    return render(request, 'dashboards/doctor.html')


# Role-specific profile pages
@login_required
def caregiver_profile(request):
    """Caregiver profile completion - only accessible to caregivers"""
    profile = request.user.profile
    if profile.role != 'caregiver':
        return redirect('home')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        age = request.POST.get('age')
        phone = request.POST.get('phone', '').strip()
        family_contact = request.POST.get('family_contact', '').strip()
        address = request.POST.get('address', '').strip()
        
        profile.full_name = full_name
        try:
            profile.age = int(age) if age else None
        except ValueError:
            profile.age = None
        profile.phone = phone
        profile.family_contact = family_contact
        profile.address = address
        
        if request.FILES.get('photo'):
            profile.photo = request.FILES['photo']
        
        profile.is_profile_completed = True
        profile.save()
        
        if full_name:
            request.user.first_name = full_name
            request.user.save()
        
        return redirect('caregiver_home')
    
    return render(request, 'profiles/caregiver_profile.html', {'profile': profile})


@login_required
def family_profile(request):
    """Family Member profile completion - only accessible to family members"""
    profile = request.user.profile
    if profile.role != 'family':
        return redirect('home')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        age = request.POST.get('age')
        phone = request.POST.get('phone', '').strip()
        family_contact = request.POST.get('family_contact', '').strip()
        address = request.POST.get('address', '').strip()
        
        profile.full_name = full_name
        try:
            profile.age = int(age) if age else None
        except ValueError:
            profile.age = None
        profile.phone = phone
        profile.family_contact = family_contact
        profile.address = address
        
        if request.FILES.get('photo'):
            profile.photo = request.FILES['photo']
        
        profile.is_profile_completed = True
        profile.save()
        
        if full_name:
            request.user.first_name = full_name
            request.user.save()
        
        return redirect('family_home')
    
    return render(request, 'profiles/family_profile.html', {'profile': profile})


@login_required
def doctor_profile(request):
    """Doctor profile completion - only accessible to doctors"""
    profile = request.user.profile
    if profile.role != 'doctor':
        return redirect('home')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        age = request.POST.get('age')
        phone = request.POST.get('phone', '').strip()
        family_contact = request.POST.get('family_contact', '').strip()
        address = request.POST.get('address', '').strip()
        
        profile.full_name = full_name
        try:
            profile.age = int(age) if age else None
        except ValueError:
            profile.age = None
        profile.phone = phone
        profile.family_contact = family_contact
        profile.address = address
        
        if request.FILES.get('photo'):
            profile.photo = request.FILES['photo']
        
        profile.is_profile_completed = True
        profile.save()
        
        if full_name:
            request.user.first_name = full_name
            request.user.save()
        
        return redirect('doctor_home')
    
    return render(request, 'profiles/doctor_profile.html', {'profile': profile})


# Role-specific home pages
@login_required
def caregiver_home(request):
    """Caregiver home page - only accessible to caregivers"""
    profile = request.user.profile
    if profile.role != 'caregiver':
        return redirect('home')
    return render(request, 'homes/caregiver_home.html')


@login_required
def family_home(request):
    """Family Member home page - only accessible to family members"""
    profile = request.user.profile
    if profile.role != 'family':
        return redirect('home')
    return render(request, 'homes/family_home.html')


@login_required
def doctor_home(request):
    """Doctor home page - only accessible to doctors"""
    profile = request.user.profile
    if profile.role != 'doctor':
        return redirect('home')
    return render(request, 'homes/doctor_home.html')
