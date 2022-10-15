from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import FormView

from user.forms import MobileEnterForm, EmailEnterForm
from user.services import AuthService


class BaseView(FormView):
    template_name = 'user/signup/initial_step.html'
    form_class = None
    send_verification_code = None
    success_url_name = None
    other_signup_option_url_name = None
    other_signup_option_text = None
    contact_type = None
    contact_field_name = None

    def __init__(self, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        self.contact = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('profile'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['other_signup_option_url'] = reverse(self.other_signup_option_url_name)
        data['other_signup_option_text'] = self.other_signup_option_text
        return data

    def form_valid(self, form):
        self.contact = form.cleaned_data[self.contact_field_name]
        self.send_verification_code(contact=self.contact)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return f'{reverse(self.success_url_name)}?{self.contact_type}={self.contact}'


class MobileInitialStepView(BaseView):
    form_class = MobileEnterForm
    send_verification_code = AuthService.send_mobile_verification_code
    success_url_name = 'signup-mobile-2'
    other_signup_option_url_name = 'signup-email-1'
    other_signup_option_text = _('Signup with email')
    contact_type = 'mobile'
    contact_field_name = 'mobile_number'


class EmailInitialStepView(BaseView):
    form_class = EmailEnterForm
    send_verification_code = AuthService.send_email_verification_code
    success_url_name = 'signup-email-2'
    other_signup_option_url_name = 'signup-mobile-1'
    other_signup_option_text = _('Signup with mobile number')
    contact_type = 'email'
    contact_field_name = 'email'
