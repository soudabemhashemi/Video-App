from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import FormView

from user.forms import EmailVerificationForm
from user.services import AuthService


class EmailVerificationView(FormView):
    form_class = EmailVerificationForm
    template_name = 'user/signup/contact_verification.html'

    def __init__(self, *args, **kwargs):
        super(EmailVerificationView, self).__init__(*args, **kwargs)
        self.email = None
        self.code = None

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        if not email:
            return HttpResponseRedirect(reverse('signup-email-1'))
        if not AuthService.is_verification_code_sent(contact_type=AuthService.CONTACT_TYPE_EMAIL, contact=email):
            return HttpResponseRedirect(reverse('signup-email-1'))
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            kwargs.update({'email': self.request.GET.get('email')})
        return kwargs

    def form_valid(self, form):
        self.email = form.cleaned_data['email']
        self.code = form.cleaned_data['verification_code']
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return f'{reverse("signup-email-3")}?email={self.email}&code={self.code}'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['other_signup_option_url'] = reverse('signup-mobile-1')
        data['other_signup_option_text'] = _('Signup with mobile number')
        return data
