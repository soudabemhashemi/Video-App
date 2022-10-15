from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from user.services import AuthService


class EmailVerificationForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.TextInput(attrs={
            'type': 'email', 'class': 'form-control', 'placeholder': _('Enter your email'), 'readonly': True
        })
    )
    verification_code = forms.CharField(
        label=_('Verification code'),
        widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'form-control', 'placeholder': _('Enter verification code sent to your email')
        })
    )

    def __init__(self, *args, **kwargs):
        _email = kwargs.pop('email', None)
        super(EmailVerificationForm, self).__init__(*args, **kwargs)
        self.initial['email'] = _email

    def clean(self):
        email = self.cleaned_data['email']
        code = self.cleaned_data['verification_code']
        if not AuthService.is_submitted_code_verified(
                contact_type=AuthService.CONTACT_TYPE_EMAIL, contact=email, code=code):
            raise ValidationError({'verification_code': _('Invalid verification code.')})
        return self.cleaned_data
