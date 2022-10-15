from django.core.exceptions import ValidationError
from django.forms import CharField, Form, TextInput
from django.utils.translation import gettext_lazy as _


class PerformPasswordResetForm(Form):
    password1 = CharField(
        widget=TextInput(attrs={'type': 'password', 'class': 'form-control'}), label=_('Password')
    )
    password2 = CharField(
        widget=TextInput(attrs={'type': 'password', 'class': 'form-control'}), label=_('Password confirmation')
    )

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError({
                'password2': _('The two password fields didn’t match.'),
            })
        return self.cleaned_data
