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
        
        # Remove spaces and hyphens if any
        phone = re.sub(r"[\s\-]", "", phone)

        if phone.startswith('+254'):
            if not re.fullmatch(r'\+2547\d{8}', phone):
                raise forms.ValidationError("Phone must start with +2547 followed by 8 digits (e.g., +254712345678).")
        elif phone.startswith('07'):
            if not re.fullmatch(r'07\d{8}', phone):
                raise forms.ValidationError("Phone must start with 07 followed by 8 digits (e.g., 0712345678).")
        else:
            raise forms.ValidationError("Phone must start with +254 or 07.")

        return phone

class PositionForm(FormSettings):
    class Meta:
        model = Position
        fields = ['name', 'max_vote']


class CandidateForm(FormSettings):
    class Meta:
        model = Candidate
        fields = ['fullname', 'bio', 'position', 'photo']
