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


@login_required(login_url='staff_login')

def dashboard(request):
    # Most booked package
    most_booked_package = Package.objects.annotate(num_bookings=Count('bookings')).order_by('-num_bookings').first()

    # Total children booked
    total_children_booked = Child.objects.filter(bookings__is_paid=True).distinct().count()

    # Recent booked children with parent & package info
    recent_bookings = Booking.objects.filter(is_paid=True).order_by('-created_at')[:5]

    # Total revenue from bookings
    total_revenue = Booking.objects.filter(is_paid=True).aggregate(total=Sum('total_price'))['total'] or 0

    # Total active packages
    total_active_packages = Package.objects.filter(is_active=True).count()

    context = {
        'most_booked_package': most_booked_package,
        'total_children_booked': total_children_booked,
        'recent_bookings': recent_bookings,
        'total_revenue': total_revenue,
        'total_active_packages': total_active_packages
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='staff_login')
def staff_profile(request):
    staff = get_object_or_404(Staff, user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            mobile = request.POST.get('mobile')
            address = request.POST.get('address')

            if not mobile or not address:
                messages.error(request, "All fields are required to update profile.")
            else:
                staff.mobile = mobile
                staff.address = address
                staff.save()
                messages.success(request, "Profile updated successfully.")

        elif 'delete_profile' in request.POST:
            user = staff.user
            staff.delete()
            user.delete()
            messages.success(request, "Your profile has been deleted.")
            return redirect('staff_login')

    return render(request, 'profile/staff_profile.html', {'staff': staff})


# Staff Views
@login_required(login_url='staff_login')
def staff_profile(request):
    staff = get_object_or_404(Staff, user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            mobile = request.POST.get('mobile')
            address = request.POST.get('address')

            if not mobile or not address:
                messages.error(request, "All fields are required to update profile.")
            else:
                staff.mobile = mobile
                staff.address = address
                staff.save()
                messages.success(request, "Profile updated successfully.")

        elif 'delete_profile' in request.POST:
            user = staff.user
            staff.delete()
            user.delete()
            messages.success(request, "Your profile has been deleted.")
            return redirect('staff_login')

    return render(request, 'profile/staff_profile.html', {'staff': staff})


@login_required(login_url='staff_login')
def reports(request):
    staff = get_object_or_404(Staff, user=request.user)

    staff_reports = Report.objects.filter(staff=staff).order_by('-created_at')

    reported_bookings = staff.reports.values_list("booking_id", flat=True)
    bookings_without_reports = Booking.objects.exclude(id__in=reported_bookings)

    return render(request, 'dashboard/reports.html', {
        'reports': staff_reports,
        'bookings': bookings_without_reports
    })


@login_required(login_url='staff_login')
def generate_report(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    staff = get_object_or_404(Staff, user=request.user)

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        selected_children_ids = request.POST.getlist('children')

        if not selected_children_ids:
            messages.error(request, "Please select at least one child.")
            return redirect('generate_report', booking_id=booking.id)

        report = Report.objects.create(
            booking=booking,
            staff=staff,
            title=title,
            description=description,
            status="Pending"
        )
        report.children.set(Child.objects.filter(id__in=selected_children_ids))

        messages.success(request, "Report submitted successfully and is pending admin approval!")
        return redirect('reports')

    children = booking.children.all()
    return render(request, 'dashboard/generate_report.html', {'booking': booking, 'children': children})


@login_required(login_url='staff_login')
def see_bookings(request):
    bookings = Booking.objects.all().\get.method(Post.method)
    return render(request, 'dashboard/see_bookings.html', {'bookings': bookings})



