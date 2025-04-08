import random
from django.core.mail import send_mail
from .models import EmailOTP

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_to_user(user):
    otp = generate_otp()
    EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp})
    
    name = user.first_name or user.email
    subject = "Your OTP Code"
    message = f"Hello {name},\n\nYour OTP code is: {otp}\nIt expires in 10 minutes."
    
    send_mail(subject, message, 'noreply@evoting.com', [user.email])
