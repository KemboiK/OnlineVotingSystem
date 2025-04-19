from django import forms
from .models import *
from account.forms import FormSettings
from django.core.exceptions import ValidationError
import re


class VoterForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['phone']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        # Remove any spaces
        phone = phone.replace(" ", "")

        # Rule 1: +254 format
        if phone.startswith('+254'):
            if not re.fullmatch(r'\+2547\d{8}', phone):
                raise forms.ValidationError("Phone must start with +254 ")
        
        # Rule 2: 07 format
        elif phone.startswith('07'):
            if not re.fullmatch(r'07\d{8}', phone):
                raise forms.ValidationError("Phone must start with 07 and be exactly 10 digits long")

        else:
            raise forms.ValidationError("Phone number must start with +254 or 07")

        return phone

class PositionForm(FormSettings):
    class Meta:
        model = Position
        fields = ['name', 'max_vote']


class CandidateForm(FormSettings):
    class Meta:
        model = Candidate
        fields = ['fullname', 'bio', 'position', 'photo']
