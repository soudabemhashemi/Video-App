from django.forms import Form, CharField, EmailField, TextInput, Textarea, formset_factory, URLField, IntegerField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class LinkForm(Form):
    title = CharField(widget=TextInput(attrs={'type': 'text', 'class': 'form-control', 'disabled': True}), label=_('Type'))
    url = URLField(widget=TextInput(attrs={'type': 'text', 'class': 'form-control', 'disabled': True}), label=_('Link'))
    id = IntegerField()


class ProfileForm(Form):
    username = CharField(
        widget=TextInput(attrs={'type': 'text', 'class': 'form-control', 'disabled': True}), label=_('Username'),
        required=False
    )
    first_name = CharField(
        widget=TextInput(attrs={'type': 'text', 'class': 'form-control'}), label=_('First name'), required=False
    )
    last_name = CharField(
        widget=TextInput(attrs={'type': 'text', 'class': 'form-control'}), label=_('Last name'), required=False
    )
    mobile = CharField(
        widget=TextInput(attrs={'type': 'text', 'class': 'form-control', 'disabled': True}), label=_('Mobile'),
        required=False
    )
    email = EmailField(
        widget=TextInput(attrs={'type': 'text', 'class': 'form-control', 'disabled': True}), label=_('Email'),
        required=False
    )
    password = CharField(
        widget=TextInput(attrs={'type': 'password', 'class': 'form-control', 'disabled': True}), label=_('Password'),
        required=False
    )
    channel_description = CharField(
        widget=Textarea(attrs={'type': 'text', 'class': 'form-control', 'rows': 6}), label=_('Channel description'),
        required=False
    )
    link_title = CharField(
        widget=TextInput(attrs={'type': 'text', 'class': 'form-control'}), label=_('Type'), required=False
    )
    link_url = URLField(
        widget=TextInput(attrs={'type': 'text', 'class': 'form-control'}), label=_('Link'), required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user
        links_form_set = formset_factory(LinkForm, extra=self.user.channel.links.count())
        self.formset = links_form_set()
        self.populate_initial_values()

    def populate_initial_values(self):
        self.initial['username'] = self.user.username
        self.initial['first_name'] = self.user.first_name
        self.initial['last_name'] = self.user.last_name
        mobile = getattr(self.user, 'mobile', None)
        if mobile:
            self.initial['mobile'] = mobile.number
        self.initial['email'] = self.user.email
        self.initial['password'] = '********'
        self.initial['channel_description'] = self.user.channel.description
        links = self.user.channel.links.all()
        for i in range(self.user.channel.links.count()):
            self.formset[i].initial['title'] = links[i].title
            self.formset[i].initial['url'] = links[i].link
            self.formset[i].initial['id'] = links[i].id

    def clean(self):
        if not self.cleaned_data.get('first_name'):
            raise ValidationError({'first_name': self.fields.get('first_name').error_messages.get('required')})
        if not self.cleaned_data.get('last_name'):
            raise ValidationError({'last_name': self.fields.get('last_name').error_messages.get('required')})

        if not self.errors:
            if self.cleaned_data.get('link_url') and not self.cleaned_data.get('link_title'):
                raise ValidationError({'link_title': self.fields.get('link_title').error_messages.get('required')})
            if not self.cleaned_data.get('link_url') and self.cleaned_data.get('link_title'):
                raise ValidationError({'link_url': self.fields.get('link_url').error_messages.get('required')})

        return super(ProfileForm, self).clean()
