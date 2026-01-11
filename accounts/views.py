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
        # if already logged in, direct to profile if incomplete
        try:
            profile = request.user.profile
            if not profile.is_profile_completed:
                return redirect('profile')
        except Exception:
            pass
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Ensure profile exists and redirect based on completion flag
            profile, _ = Profile.objects.get_or_create(user=user)
            if not profile.is_profile_completed:
                return redirect('profile')
            return redirect('/home/')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if not username or not password:
            messages.error(request, 'Please fill all fields')
        elif password != password2:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created. Please login.')
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
        return redirect('/home/')

    return render(request, 'accounts/profile.html', {'profile': profile})
