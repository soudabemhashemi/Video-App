from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from user.models.mobile import Mobile


class BaseSignupForm(UserCreationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}), label=_('Username')
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}), label=_('First name'))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}), label=_('Last name')
    )
    password1 = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}), label=_('Password')
    )
    password2 = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}), label=_('Password confirmation')
    )


class MobileSignupForm(BaseSignupForm):
    mobile_number = forms.CharField(
        label=_('Mobile'),
        widget=forms.TextInput(attrs={'type': 'tel', 'class': 'form-control', 'readonly': True}),
    )

    class Meta:
        model = User
        fields = ('mobile_number', 'username', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        mobile_number = kwargs.pop('mobile_number', None)
        super(MobileSignupForm, self).__init__(*args, **kwargs)
        self.initial['mobile_number'] = mobile_number

    def save(self, commit=True):
        with transaction.atomic():
            user = super(MobileSignupForm, self).save(commit=commit)
            mobile_number = self.cleaned_data['mobile_number']
            Mobile.objects.create(number=mobile_number, user=user)
        return user


class EmailSignupForm(BaseSignupForm):
    email = forms.CharField(
        label=_('Email'),
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'readonly': True}),
    )

    def __init__(self, *args, **kwargs):
        email = kwargs.pop('email', None)
        super(EmailSignupForm, self).__init__(*args, **kwargs)
        self.initial['email'] = email

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'password1', 'password2')
