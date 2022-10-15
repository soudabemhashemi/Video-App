from django.contrib.auth.models import User
from django.forms import Form, ChoiceField, RadioSelect
from django.utils.translation import gettext_lazy as _

from user.models import Mobile
from user.state import PasswordResetState


class SendPasswordResetForm(Form):
    password_reset_method = ChoiceField(
        label=_('Select one to send password reset code'),
        widget=RadioSelect()
    )

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', 0)
        reset_method = kwargs.pop('reset_method', None)
        super().__init__(*args, **kwargs)
        choices, initial_choice = self.get_password_reset_method_choices(user_id=user_id, reset_method=reset_method)
        self.fields['password_reset_method'].choices = choices
        self.initial['password_reset_method'] = initial_choice

    def get_password_reset_method_choices(self, user_id, reset_method):
        choices = []
        mobile = Mobile.objects.filter(user_id=user_id).first()
        if mobile:
            choice = ('mobile', mobile.masked_number)
            choices.append(choice)

        email = User.objects.filter(id=user_id).first().email
        if email:
            choice = ('email', self.masked_email(email))
            choices.append(choice)

        if reset_method:
            if reset_method == PasswordResetState.MOBILE_METHOD and mobile:
                initial_choice = 'mobile'
            elif reset_method == PasswordResetState.EMAIL_METHOD and email:
                initial_choice = 'email'
            else:
                initial_choice = None
        elif choices:
            initial_choice = choices[0][0]
        else:
            initial_choice = None

        return choices, initial_choice

    @staticmethod
    def masked_email(email):
        key, host = email.split('@')
        masked_key = key[:4] + ''.join(['*' for _ in key[4:]])
        return f'{masked_key}@{host}'

