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
        
        # Remove spaces and hyphens
        phone = re.sub(r"[\s\-]", "", phone)

        # Kenyan mobile number patterns
        local_pattern = r'^(07|01)\d{8}$'
        intl_pattern = r'^\+254(7|1)\d{8}$'

        if re.fullmatch(local_pattern, phone) or re.fullmatch(intl_pattern, phone):
            return phone
        else:
            raise forms.ValidationError(
                "Phone must start with 07 or 01 or +2547/+2541 followed by 8 digits."
            )

class PositionForm(FormSettings):
    class Meta:
        model = Position
        fields = ['name', 'max_vote']


class CandidateForm(FormSettings):
    class Meta:
        model = Candidate
        fields = ['fullname', 'bio', 'position', 'photo']
