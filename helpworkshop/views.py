from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
# helpworkshop/views.py

def help_home(request):
    return render(request, 'helpworkshop/help_home.html')

def faq_view(request):
    return render(request, 'helpworkshop/faq.html')

def contact_support(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"Support Request from {name}"
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        send_mail(
            subject,
            full_message,
            settings.DEFAULT_FROM_EMAIL,  # from (same as our OTP sender)
            ['evotingjkuat@gmail.com'],   # to (support inbox)
            fail_silently=False,
        )

        return render(request, 'helpworkshop/contact.html', {
            'success': True,
            'name': name
        })

    return render(request, 'helpworkshop/contact.html')
