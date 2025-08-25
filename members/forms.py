# members/views.py (sau members/forms.py dacă le separi)
from django import forms
from core.models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email']
        error_messages = {
            'email': {
                'required': 'Email is required.',
                'unique': 'A member with this email already exists.',
            },
            'name': {'required': 'Name is required.'},
        }
