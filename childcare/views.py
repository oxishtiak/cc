from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
import uuid
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Count, Sum


# Create your views here.
def Home(request):
    return render(request, "home.html")


def signup_parent(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup_parent")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect("signup_parent")

        user = User.objects.create_user(username=username, email=email, password=password)
        Parent.objects.create(user=user, phone=phone)
        login(request, user)
        return redirect("home")

    return render(request, "auth/signup_parent.html")


def signup_staff(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        mobile = request.POST["mobile"]
        is_staff = "is_staff" in request.POST

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup_staff")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect("signup_staff")

        # Create the user with is_active set to False
        user = User.objects.create_user(
            username=username, email=email, password=password, is_active=False
        )
        Staff.objects.create(user=user, mobile=mobile, is_staff=is_staff, is_active=True)

        messages.success(
            request, "Staff registration is successful. Please wait for admin approval."
        )
        return redirect("staff_login")

    return render(request, "auth/signup_staff.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "auth/login.html")


def staff_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                messages.error(request, "Your account is not yet approved by the admin.")
                return redirect("staff_login")
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "auth/staff_login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def staff_logout(request):
    logout(request)
    return redirect("home")


@login_required(login_url="staff_login")
def dashboard(request):
    # Most booked package
    most_booked_package = (
        Package.objects.annotate(num_bookings=Count("bookings")).order_by("-num_bookings").first()
    )

    # Total children booked
    total_children_booked = Child.objects.filter(bookings__is_paid=True).distinct().count()

    # Recent booked children with parent & package info
    recent_bookings = Booking.objects.filter(is_paid=True).order_by("-created_at")[:5]

    # Total revenue from bookings
    total_revenue = (
        Booking.objects.filter(is_paid=True).aggregate(total=Sum("total_price"))["total"] or 0
    )

    # Total active packages
    total_active_packages = Package.objects.filter(is_active=True).count()

    context = {
        "most_booked_package": most_booked_package,
        "total_children_booked": total_children_booked,
        "recent_bookings": recent_bookings,
        "total_revenue": total_revenue,
        "total_active_packages": total_active_packages,
    }

    return render(request, "dashboard/dashboard.html", context)


# Parent Dashboard


@login_required(login_url="login")
def parent_profile(request):
    parent = get_object_or_404(Parent, user=request.user)
    children = parent.children.all()

    if request.method == "POST":
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        parent.phone = phone
        parent.address = address
        parent.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("parent_profile")

    return render(request, "profile/parent_profile.html", {"parent": parent, "children": children})


@login_required(login_url="login")
def add_child(request):
    if request.method == "POST":
        name = request.POST["name"]
        age = request.POST["age"]
        dob = request.POST["date_of_birth"]
        image = request.FILES.get("image")

        parent = get_object_or_404(Parent, user=request.user)
        Child.objects.create(
            parent=parent,
            name=name,
            age=age,
            date_of_birth=dob,
            image=image,
            unique_id=uuid.uuid4(),
        )
        messages.success(request, "Child added successfully!")
        return redirect("parent_profile")

    return render(request, "profile/add_child.html")


@login_required(login_url="login")
def edit_child(request, child_id):
    child = get_object_or_404(Child, id=child_id, parent__user=request.user)

    if request.method == "POST":
        child.name = request.POST["name"]
        child.age = request.POST["age"]
        child.date_of_birth = request.POST["date_of_birth"]
        if "image" in request.FILES:
            child.image = request.FILES["image"]
        child.save()
        messages.success(request, "Child updated successfully!")
        return redirect("parent_profile")

    return render(request, "profile/edit_child.html", {"child": child})


@login_required(login_url="login")
def delete_child(request, child_id):
    child = get_object_or_404(Child, id=child_id, parent__user=request.user)
    child.delete()
    messages.success(request, "Child deleted successfully!")
    return redirect("parent_profile")


# Package Views
def packages(request):
    packages = Package.objects.filter(is_active=True)
    return render(request, "package.html", {"packages": packages})


# Booking Views
@login_required(login_url="login")
def booking(request, package_id):
    parent = get_object_or_404(Parent, user=request.user)
    children = Child.objects.filter(parent=parent)
    package = get_object_or_404(Package, id=package_id)

    if request.method == "POST":
        selected_children_ids = request.POST.getlist("children")  # Get list of selected children
        start_date = request.POST.get("start_date")

        if not selected_children_ids:
            messages.error(request, "Please select at least one child.")
            return redirect("booking", package_id=package_id)

        # Create the booking
        booking = Booking.objects.create(
            parent=parent,
            package=package,
            total_price=package.price,
            start_date=start_date,
            end_date=now().date() + timedelta(days=package.duration_days),
            status="pending",
            is_paid=False,
        )
        booking.children.set(selected_children_ids)

        messages.success(request, "Booking initiated. Proceed to checkout.")
        return redirect("checkout", booking_id=booking.id)

    return render(request, "booking/booking.html", {"package": package, "children": children})


# Checkout Views
@login_required(login_url="login")
def checkout(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, parent__user=request.user)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")

        if payment_method not in ["card", "bkash", "nagad", "cash"]:
            messages.error(request, "Invalid payment method selected.")
            return redirect("checkout", booking_id=booking.id)

        transaction = Transaction.objects.create(
            booking=booking,
            payment_method=payment_method,
            transaction_id=uuid.uuid4(),
            is_successful=True,
        )

        # Update booking status to confirmed
        booking.is_paid = False
        booking.status = "pending"
        booking.save()

        messages.success(request, "Payment successful! wait for confirmation!!!.")
        return redirect("my_bookings")

    return render(request, "booking/checkout.html", {"booking": booking})


# My Bookings Views
@login_required(login_url="login")
def my_bookings(request):
    parent = get_object_or_404(Parent, user=request.user)
    bookings = Booking.objects.filter(parent=parent).order_by("-created_at")

    return render(request, "booking/my_bookings.html", {"bookings": bookings})


# Feedback & Reports Views


@login_required(login_url="login")
def approved_reports(request):
    parent = get_object_or_404(Parent, user=request.user)
    bookings = Booking.objects.filter(parent=parent)
    reports = Report.objects.filter(booking__in=bookings, status="Approved").order_by("-created_at")

    for report in reports:
        feedback = Feedback.objects.filter(booking=report.booking, parent=parent).first()
        report.has_feedback = feedback is not None
        report.feedback = feedback

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if booking_id and rating and comment:
            booking = get_object_or_404(Booking, id=booking_id, parent=parent)

            if not Feedback.objects.filter(booking=booking, parent=parent).exists():
                Feedback.objects.create(
                    booking=booking, parent=parent, rating=rating, comment=comment
                )
                messages.success(request, "Thank you for your feedback!")
                return redirect("approved_reports")
            else:
                messages.error(request, "You have already submitted feedback for this booking.")
        else:
            messages.error(request, "Please provide both rating and comment.")

    return render(request, "parent/approved_reports.html", {"reports": reports})


@login_required(login_url="login")  # not necessary
def submit_feedback(request, booking_id):
    parent = get_object_or_404(Parent, user=request.user)
    booking = get_object_or_404(Booking, id=booking_id, parent=parent)

    if not booking.reports.filter(status="Approved").exists():
        messages.error(request, "No approved report found for this booking.")
        return redirect("approved_reports")

    if Feedback.objects.filter(booking=booking, parent=parent).exists():
        messages.error(request, "You have already submitted feedback for this booking.")
        return redirect("approved_reports")

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if not rating or not comment:
            messages.error(request, "Please provide both rating and comment.")
            return redirect("submit_feedback", booking_id=booking.id)

        Feedback.objects.create(booking=booking, parent=parent, rating=rating, comment=comment)

        messages.success(request, "Thank you for your feedback!")
        return redirect("approved_reports")

    return render(request, "parent/submit_feedback.html", {"booking": booking})


# Staff Views
@login_required(login_url="staff_login")
def staff_profile(request):
    staff = get_object_or_404(Staff, user=request.user)

    if request.method == "POST":
        if "update_profile" in request.POST:
            mobile = request.POST.get("mobile")
            address = request.POST.get("address")

            if not mobile or not address:
                messages.error(request, "All fields are required to update profile.")
            else:
                staff.mobile = mobile
                staff.address = address
                staff.save()
                messages.success(request, "Profile updated successfully.")

        elif "delete_profile" in request.POST:
            user = staff.user
            staff.delete()
            user.delete()
            messages.success(request, "Your profile has been deleted.")
            return redirect("staff_login")

    return render(request, "profile/staff_profile.html", {"staff": staff})


@login_required(login_url="staff_login")
def reports(request):
    staff = get_object_or_404(Staff, user=request.user)

    staff_reports = Report.objects.filter(staff=staff).order_by("-created_at")

    reported_bookings = staff.reports.values_list("booking_id", flat=True)
    bookings_without_reports = Booking.objects.exclude(id__in=reported_bookings)

    return render(
        request,
        "dashboard/reports.html",
        {"reports": staff_reports, "bookings": bookings_without_reports},
    )


@login_required(login_url="staff_login")
def generate_report(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    staff = get_object_or_404(Staff, user=request.user)

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        selected_children_ids = request.POST.getlist("children")

        if not selected_children_ids:
            messages.error(request, "Please select at least one child.")
            return redirect("generate_report", booking_id=booking.id)

        report = Report.objects.create(
            booking=booking, staff=staff, title=title, description=description, status="Pending"
        )
        report.children.set(Child.objects.filter(id__in=selected_children_ids))

        messages.success(request, "Report submitted successfully and is pending admin approval!")
        return redirect("reports")

    children = booking.children.all()
    return render(
        request, "dashboard/generate_report.html", {"booking": booking, "children": children}
    )


@login_required(login_url="staff_login")
def see_bookings(request):
    bookings = Booking.objects.all().order_by("-created_at")
    return render(request, "dashboard/see_bookings.html", {"bookings": bookings})
