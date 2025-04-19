from django import forms
from .models import *
from account.forms import FormSettings
from django.core.exceptions import ValidationError
import re


class VoterForm(FormSettings):
    class Meta:
        model = Voter
        fields = ['phone']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip().replace(" ", "").replace("-", "")

        if phone.startswith('+254'):
            phone = phone.replace('+254', '254', 1)
        elif phone.startswith('07') and len(phone) == 10:
            phone = '254' + phone[1:]
        elif phone.startswith('254') and len(phone) == 12:
            pass
        else:
            raise ValidationError("Phone number must start with +254 or 07 and be valid.")

        if not re.fullmatch(r'2547\d{8}', phone):
            raise ValidationError("Enter a valid Kenyan number like 0712345678 or +254712345678")

        return phone



class PositionForm(FormSettings):
    class Meta:
        model = Position
        fields = ['name', 'max_vote']


class CandidateForm(FormSettings):
    class Meta:
        model = Candidate
        fields = ['fullname', 'bio', 'position', 'photo']
