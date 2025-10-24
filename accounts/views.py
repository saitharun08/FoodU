from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import User
from .forms import MobileLoginForm, OtpForm
from django.http import HttpResponse

STATIC_OTP = "1234"

def mobile_login(request):
    """Step 1: Ask user for mobile number."""
    if request.method == "POST":
        form = MobileLoginForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile']
            request.session['mobile'] = mobile
            # Auto-create user if not registered yet
            user, created = User.objects.get_or_create(mobile=mobile)
            if created:
                user.set_unusable_password()
                user.save()
                messages.info(request, "New user created with default role 'customer'.")
            return redirect('verify_otp')
    else:
        form = MobileLoginForm()
    return render(request, "accounts/mobile_login.html", {"form": form})

def verify_otp(request):
    """Step 2: Verify OTP (static: 1234)."""
    mobile = request.session.get('mobile')
    if not mobile:
        return redirect('mobile_login')

    if request.method == "POST":
        form = OtpForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if otp == STATIC_OTP:
                user = User.objects.get(mobile=mobile)
                login(request, user)
                messages.success(request, "Login successful!")

                # Redirect by role
                if user.role == 'admin':
                    return redirect('admin_dashboard')        # Named URL from orders/urls.py
                elif user.role == 'partner':
                    return redirect('partner_dashboard')
                else:
                    return redirect('customer_dashboard')
            else:
                messages.error(request, "Invalid OTP! Try again.")
    else:
        form = OtpForm()
    return render(request, "accounts/verify_otp.html", {"form": form, "mobile": mobile})

def unauthorized(request):
    return HttpResponse("❌ You are not authorized to view this page.")
