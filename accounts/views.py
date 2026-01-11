from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
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
