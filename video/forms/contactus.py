from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext as _
from video.models.contactus import ContactUs


class ContactUsForm(ModelForm):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": _("First name and last name"), 'class': "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': _('Email'), 'class': 'text-end form-control'}))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': _('Mobile'), 'class': 'form-control'}))
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": _('Message'), "rows": 5, "class": "ml-2 form-control"}
        ),
    )

    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'phone', 'description']
