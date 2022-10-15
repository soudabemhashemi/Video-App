from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _

from user.forms import EmailSignupForm
from user.services import AuthService
from user.views.signup.base_signup import BaseSignupView


class EmailSignupView(BaseSignupView):
    form_class = EmailSignupForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            kwargs.update({'email': self.request.GET.get('email')})
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['other_signup_option_url'] = reverse('signup-mobile-1')
        data['other_signup_option_text'] = _('Signup with mobile number')
        return data

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            email = request.GET.get('email')
            code = request.GET.get('code')
            if not (email or code):
                return HttpResponseRedirect(reverse('signup-email-1'))
            if not AuthService.is_submitted_code_verified(AuthService.CONTACT_TYPE_EMAIL, email, code):
                return HttpResponseRedirect(reverse('signup-email-1'))
        return super().get(request, *args, **kwargs)
