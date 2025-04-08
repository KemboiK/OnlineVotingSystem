from django.shortcuts import render, redirect, reverse
from .email_backend import EmailBackend
from django.contrib import messages
from .forms import CustomUserForm
from voting.forms import VoterForm
from django.contrib.auth import login, logout
from .models import EmailOTP
from .utils import send_otp_to_user
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your views here.


def account_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("adminDashboard"))
        else:
            return redirect(reverse("voterDashboard"))

    context = {}
    if request.method == 'POST':
        user = EmailBackend.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("adminDashboard"))
            else:
                return redirect(reverse("voterDashboard"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")

    return render(request, "voting/login.html", context)


def account_register(request):
    userForm = CustomUserForm(request.POST or None)
    voterForm = VoterForm(request.POST or None)
    context = {
        'form1': userForm,
        'form2': voterForm
    }
    if request.method == 'POST':
        if userForm.is_valid() and voterForm.is_valid():
            user = userForm.save(commit=False)
            voter = voterForm.save(commit=False)
            voter.admin = user
            user.save()
            voter.save()
            messages.success(request, "Account created. You can login now!")
            return redirect(reverse('account_login'))
        else:
            messages.error(request, "Provided data failed validation")
            # return account_login(request)
    return render(request, "voting/reg.html", context)


def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect(reverse("account_login"))

# **Password Reset Views**

def forgot_password(request):
    if request.user.is_authenticated:
        # Redirect to the user dashboard if they are already logged in
        return redirect('voterDashboard')  # or 'adminDashboard' depending on their role

    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = get_user_model().objects.get(email=email)
            send_otp_to_user(user)
            request.session['reset_email'] = email  # Store the email in session for later
            return redirect('verify_otp')  # Redirect to OTP verification page
        except get_user_model().DoesNotExist:
            messages.error(request, 'Email not found.')  # Handle case where email doesn't exist
    
    return render(request, 'account/forgot_password.html')  # Render the form for the forgot password page


def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST['otp']
        email = request.session.get('reset_email')
        user = get_user_model().objects.get(email=email)
        otp_record = EmailOTP.objects.get(user=user)
        if otp_record.otp == otp_input and not otp_record.is_expired():
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid or expired OTP.')
    return render(request, 'account/verify_otp.html')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm = request.POST['confirm']
        if password == confirm:
            email = request.session.get('reset_email')
            user = get_user_model().objects.get(email=email)
            user.password = make_password(password)
            user.save()
            messages.success(request, 'Password reset successfully.')
            return redirect('account_login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'account/reset_password.html')
