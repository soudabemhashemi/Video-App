import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class EmailEnterForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.TextInput(attrs={'type': 'email', 'class': 'form-control', 'placeholder': 'example@example.com'})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        email_regex = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
        is_email = email_regex.match(email)

        if not is_email:
            raise ValidationError({'email': _('Invalid email address.')})

        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': _('Email address is already used by another user.')})

        return cleaned_data
