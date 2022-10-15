from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from user.services import AuthService


class MobileVerificationForm(forms.Form):
    mobile_number = forms.CharField(
        label=_('Mobile'),
        widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'form-control', 'placeholder': _('Enter your mobile number'), 'readonly': True
        })
    )
    verification_code = forms.CharField(
        label=_('Verification code'),
        widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'form-control', 'placeholder': _('Enter verification code sent to your mobile')
        })
    )

    def __init__(self, *args, **kwargs):
        _mobile_number = kwargs.pop('mobile', None)
        super(MobileVerificationForm, self).__init__(*args, **kwargs)
        self.initial['mobile_number'] = _mobile_number

    def clean(self):
        mobile_number = self.cleaned_data['mobile_number']
        code = self.cleaned_data['verification_code']
        if not AuthService.is_submitted_code_verified(
                contact_type=AuthService.CONTACT_TYPE_MOBILE, contact=mobile_number, code=code):
            raise ValidationError({'verification_code': _('Invalid verification code.')})
        return self.cleaned_data
