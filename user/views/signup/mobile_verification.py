from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import FormView

from user.forms import MobileVerificationForm
from user.services import AuthService


class MobileVerificationView(FormView):
    form_class = MobileVerificationForm
    template_name = 'user/signup/contact_verification.html'

    def __init__(self, *args, **kwargs):
        super(MobileVerificationView, self).__init__(*args, **kwargs)
        self.mobile_number = None
        self.code = None

    def get(self, request, *args, **kwargs):
        mobile_number = request.GET.get('mobile')
        if not mobile_number:
            return HttpResponseRedirect(reverse('signup-mobile-1'))
        if not AuthService.is_verification_code_sent(contact_type=AuthService.CONTACT_TYPE_MOBILE, contact=mobile_number):
            return HttpResponseRedirect(reverse('signup-mobile-1'))
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            kwargs.update({'mobile': self.request.GET.get('mobile')})
        return kwargs

    def form_valid(self, form):
        self.mobile_number = form.cleaned_data['mobile_number']
        self.code = form.cleaned_data['verification_code']
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return f'{reverse("signup-mobile-3")}?mobile={self.mobile_number}&code={self.code}'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['other_signup_option_url'] = reverse('signup-email-1')
        data['other_signup_option_text'] = _('Signup with email')
        return data
