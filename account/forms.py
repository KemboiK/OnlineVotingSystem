from django import forms
from .models import *
import re 
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
        'required': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'required': True
    }))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())  # <-- Add this line

    widget = {
        'password': forms.PasswordInput(),
    }

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            instance = kwargs.get('instance').__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"
        else:
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True

    def clean_email(self):
        formEmail = self.cleaned_data['email'].lower()

        # JKUAT student email format enforcement
        pattern = r"^[a-zA-Z0-9._%+-]+@students\.jkuat\.ac\.ke$"
        if not re.match(pattern, formEmail):
            raise forms.ValidationError("You must use a JKUAT student email (example@students.jkuat.ac.ke).")

        # Check if email already exists in the database
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError("The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(id=self.instance.pk).email.lower()
            if dbEmail != formEmail:  # If the email has been changed
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    def clean_password(self):
        password = self.cleaned_data.get("password", None)
        
        if self.instance.pk is not None:
            if not password:
                return self.instance.password  # Keep existing password if not changed

        if password:
            # Password validation: at least 8 characters, one uppercase, one digit, and one special character
            if len(password) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            if not re.search(r'[A-Z]', password):
                raise ValidationError("Password must contain at least one uppercase letter.")
            if not re.search(r'[0-9]', password):
                raise ValidationError("Password must contain at least one digit.")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise ValidationError("Password must contain at least one special character.")

            # Hash the password if it's valid
            return make_password(password)
        else:
            raise ValidationError("Password is required")

    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'email', 'password']
