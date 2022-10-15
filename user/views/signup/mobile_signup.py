from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _

from user.forms import MobileSignupForm
from user.services import AuthService
from user.views.signup.base_signup import BaseSignupView


class MobileSignupView(BaseSignupView):
    form_class = MobileSignupForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            kwargs.update({'mobile_number': self.request.GET.get('mobile')})
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['other_signup_option_url'] = reverse('signup-email-1')
        data['other_signup_option_text'] = _('Signup with email')
        return data

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            mobile_number = request.GET.get('mobile')
            code = request.GET.get('code')
            if not (mobile_number or code):
                return HttpResponseRedirect(reverse('signup-mobile-1'))
            if not AuthService.is_submitted_code_verified(AuthService.CONTACT_TYPE_MOBILE, mobile_number, code):
                return HttpResponseRedirect(reverse('signup-mobile-1'))
        return super().get(request, *args, **kwargs)
