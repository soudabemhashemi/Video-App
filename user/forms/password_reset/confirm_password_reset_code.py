from django.core.exceptions import ValidationError
from django.forms import Form, CharField, TextInput
from django.utils.translation import gettext_lazy as _

from user.services import AuthService
from user.state import PasswordResetState


class ConfirmPasswordResetCodeForm(Form):
    verification_code = CharField(
        label=_('Enter verification code sent to you'),
        widget=TextInput(attrs={
            'type': 'text', 'class': 'form-control', 'placeholder': _('ٰVerification code')
        }),
    )

    def __init__(self, *args, **kwargs):
        method = kwargs.pop('method')
        contact = kwargs.pop('contact')
        super().__init__(*args, **kwargs)
        self.method = method
        self.contact = contact

    def clean(self):
        code = self.cleaned_data.get('verification_code')
        if not code:
            raise ValidationError({
                'verification_code': _('No code entered.')
            })

        if self.method == PasswordResetState.MOBILE_METHOD:
            method = AuthService.CONTACT_TYPE_MOBILE
        else:
            method = AuthService.CONTACT_TYPE_EMAIL

        is_verified = AuthService.is_submitted_code_verified(contact_type=method, contact=self.contact, code=code)

        if not is_verified:
            raise ValidationError({
                'verification_code': _('Invalid code')
            })

        return self.cleaned_data
