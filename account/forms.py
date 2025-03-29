from django import forms
from .models import *
import re

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    widget = {
        'password': forms.PasswordInput(),
    }

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

        return make_password(password)

    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'email', 'password']
