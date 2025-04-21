import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from .models import EmailOTP
from voting.models import Voter

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_to_user(user, mode='password_reset'):
    # Generate OTP
    otp = generate_otp()

    # Prepare email content
    name = user.first_name or user.email
    subject = "Your OTP Code"
    message = (
        f"Hello {name},\n\n"
        f"Your OTP code is: {otp}\n"
        f"It will expire in 3 minutes.\n\n"
        "If you did not request this, please ignore this email."
    )

    if mode == 'password_reset':
        # Store OTP in EmailOTP model
        EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp})
        print(f"[DEBUG] Password reset OTP {otp} saved for {user.email}")

    elif mode == 'voting':
        try:
            voter = user.voter  # use reverse relation to avoid mismatch
            voter.otp = str(otp)
            voter.otp_expiry = timezone.now() + timedelta(minutes=3)
            voter.save()
            print(f"[DEBUG] Voting OTP {otp} saved for voter: {voter} (user: {user.email})")
        except Voter.DoesNotExist:
            print(f"[ERROR] Voter not found for user {user.email}")
            return

    # Send the email
    try:
        send_mail(subject, message, 'noreply@evoting.com', [user.email])
        print(f"[DEBUG] OTP email sent to {user.email}")
    except Exception as e:
        print(f"[ERROR] Failed to send OTP email to {user.email}: {e}")
