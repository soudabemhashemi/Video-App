from django.http import HttpResponseRedirect
from django.urls import reverse
from user.forms import SendPasswordResetForm
from user.services import AuthService
from user.state import PasswordResetState
from user.views.password_reset.base_password_reset import BasePasswordResetView


class SendPasswordResetView(BasePasswordResetView):
    form_class = SendPasswordResetForm
    template_name = 'user/password_reset/send_password_reset.html'
    password_reset_step = PasswordResetState.SELECT_METHOD_STEP

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.password_reset_state.user
        method = self.password_reset_state.method
        kwargs.update({'user_id': user.id})
        kwargs.update({'reset_method': method})
        return kwargs

    def form_valid(self, form):
        state = self.password_reset_state
        user = state.user
        state.set_method(form.cleaned_data.get('password_reset_method'))
        if state.method == PasswordResetState.MOBILE_METHOD:
            AuthService.send_mobile_verification_code(contact=user.mobile.number)
            response = HttpResponseRedirect(reverse('password-reset-confirm-code'))
            state.set_step(PasswordResetState.CONFIRM_CODE_STEP)
            state.save(response)

        elif state.method == PasswordResetState.EMAIL_METHOD:
            AuthService.send_email_verification_code(contact=user.email)
            response = HttpResponseRedirect(reverse('password-reset-confirm-code'))
            state.set_step(PasswordResetState.CONFIRM_CODE_STEP)
            state.save(response)
        else:
            return HttpResponseRedirect(reverse('password-reset-begin'))
        return response
