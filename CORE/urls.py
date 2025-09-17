"""
URL configuration for CORE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from childcare.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path("", Home, name="home"),
    path("signup_staff/", signup_staff, name="signup_staff"),
    path("login/", user_login, name="login"),
# Dashboard Staff Urls
    path("dashboard/", dashboard, name="dashboard"),
    path("reports/", reports, name="reports"),
    path("report/<int:booking_id>/generate/", generate_report, name="generate_report"),
    path("staff_profile/", staff_profile, name="staff_profile"),
    path("see_bookings/", see_bookings, name="see_bookings"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
