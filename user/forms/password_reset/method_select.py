import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from user.state import PasswordResetState


class PasswordResetMethodSelectForm(forms.Form):
    contact = forms.CharField(
        label=_('Username, mobile or email'),
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
    )

    def clean(self):
        user = None
        contact = self.cleaned_data.get('contact')
        if re.match(r'(09)(\d){9}', contact):
            user = User.objects.filter(mobile__number=contact).first()
            self.cleaned_data['mobile'] = contact
            self.cleaned_data['method'] = PasswordResetState.MOBILE_METHOD
        else:
            emails = EmailAddress.objects.filter(email__iexact=email_or_mobile)
            self.cleaned_data['method'] = PasswordResetState.EMAIL_METHOD
            self.cleaned_data['email'] = email_or_mobile
            if emails.exists():
                user = emails.first().user

        if not user:
            raise ValidationError({
                'email_or_mobile': [_('User not found.')]
            })

        self.cleaned_data['user'] = user
        return self.cleaned_data

    def clean(self):
        contact = self.cleaned_data['contact']
        user = self.get_user(contact)
        if not user:
            raise ValidationError({'contact': _('User not found.')})

        self.cleaned_data['user'] = user
        return self.cleaned_data

    @staticmethod
    def get_user(contact):
        mobile_regex = re.compile(r'^09[0-9]{9}$')
        is_mobile = mobile_regex.match(contact)
        if is_mobile:
            try:
                return User.objects.get(mobile__number=contact)
            except User.DoesNotExist:
                pass

        email_regex = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
        is_email = email_regex.match(contact)
        if is_email:
            try:
                return User.objects.get(email=contact)
            except User.DoesNotExist:
                pass

        try:
            return User.objects.get(username=contact)
        except User.DoesNotExist:
            return
