import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, TextInput
from django.utils.translation import gettext_lazy as _

from user.state import PasswordResetState


class BeginPasswordResetForm(Form):
    contact = CharField(
        label=_('Username, mobile or email'),
        widget=TextInput(attrs={'type': 'text', 'class': 'form-control'}),
    )

    def clean(self):
        contact = self.cleaned_data.get('contact')
        if re.match(r'(09)(\d){9}', contact):
            user = User.objects.filter(mobile__number=contact).first()
            self.cleaned_data['mobile'] = contact
            self.cleaned_data['method'] = PasswordResetState.MOBILE_METHOD
        elif re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', contact):
            user = User.objects.filter(email__iexact=contact).first()
            self.cleaned_data['method'] = PasswordResetState.EMAIL_METHOD
            self.cleaned_data['email'] = contact
        else:
            user = User.objects.filter(username__iexact=contact).first()

        if not user:
            raise ValidationError({
                'contact': [_('User not found.')]
            })

        if not self.cleaned_data.get('method'):
            if user.mobile:
                self.cleaned_data['method'] = 'mobile'
                self.cleaned_data['mobile'] = user.mobile.number
            elif user.email:
                self.cleaned_data['method'] = 'email'
                self.cleaned_data['email'] = user.email

        self.cleaned_data['user'] = user
        return self.cleaned_data
