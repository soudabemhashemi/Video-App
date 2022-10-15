import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from user.models import Mobile


class MobileEnterForm(forms.Form):
    mobile_number = forms.CharField(
        label=_('Mobile'),
        widget=forms.TextInput(attrs={'type': 'tel', 'class': 'form-control', 'placeholder': '09123456789'})
    )

    def clean(self):
        cleaned_data = super().clean()
        mobile_regex = re.compile(r'^09[0-9]{9}$')
        mobile_number = cleaned_data['mobile_number']
        is_mobile = mobile_regex.match(mobile_number)
        if not is_mobile:
            raise ValidationError({'mobile_number': _('Invalid mobile number.')})

        if Mobile.objects.filter(number=mobile_number).exists():
            raise ValidationError({'mobile_number': _('Mobile number is already used by another user.')})

        return cleaned_data
