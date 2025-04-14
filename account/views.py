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
from django.views.decorators.http import require_POST

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
            send_otp_to_user(user, mode= 'password_reset')
            request.session['reset_email'] = email  # Store the email in session for later
            return redirect('verify_reset_otp')  # Redirect to OTP verification page
        except get_user_model().DoesNotExist:
            messages.error(request, 'Email not found.')  # Handle case where email doesn't exist
    
    return render(request, 'voting/forgot_password.html')  # Render the form for the forgot password page


from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EmailOTP

def verify_reset_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        email = request.session.get('reset_email')

        if not email:
            messages.error(request, 'Session expired or email missing. Please restart the password reset process.')
            return redirect('forgot_password')  # Adjust this to your actual URL name

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('forgot_password')  # This helps avoid the crash

        try:
            otp_record = EmailOTP.objects.get(user=user)
        except EmailOTP.DoesNotExist:
            messages.error(request, 'OTP not found. Please request a new one.')
            return redirect('forgot_password')

        if otp_record.otp == otp_input and not otp_record.is_expired():
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid or expired OTP.')

    return render(request, 'voting/verify_otp.html')



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
    return render(request, 'voting/reset_password.html')

@require_POST
def resend_reset_otp(request):
    email = request.session.get('reset_email')

    if not email:
        messages.error(request, 'Session expired. Please start the reset process again.')
        return redirect('forgot_password')

    try:
        user = get_user_model().objects.get(email=email)
        send_otp_to_user(user, mode= 'password_reset')
        request.session['reset_email'] = email  # Refresh session key
        messages.success(request, 'A new OTP has been sent to your email.')
    except get_user_model().DoesNotExist:
        messages.error(request, 'User not found. Please try again.')

    return redirect('verify_reset_otp')