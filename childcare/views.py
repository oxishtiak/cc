from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
import uuid


# Create your views here.
def Home(request):
    return render(request, 'home.html')def Home(request):
    return render(request, 'home.html')

def signup_parent(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup_parent')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken')
            return redirect('signup_parent')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        Parent.objects.create(user=user, phone=phone)
        login(request, user)
        return redirect('home')
    
    return render(request, 'auth/signup_parent.html')

def signup_staff(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        mobile = request.POST['mobile']
        is_staff = 'is_staff' in request.POST
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup_staff')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken')
            return redirect('signup_staff')
        
        # Create the user with is_active set to False
        user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
        Staff.objects.create(user=user, mobile=mobile, is_staff=is_staff, is_active=True)
        
        messages.success(request, 'Staff registration is successful. Please wait for admin approval.')
        return redirect('staff_login')
    
    return render(request, 'auth/signup_staff.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'auth/login.html')

def staff_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                messages.error(request, 'Your account is not yet approved by the admin.')
                return redirect('staff_login')
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'auth/staff_login.html')



@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def staff_logout(request):
    logout(request)
    return redirect('home')


