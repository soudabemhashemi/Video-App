from django.urls import reverse
from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit

from user.forms import ConfirmPasswordResetCodeForm
from user.state import PasswordResetState
from user.views.password_reset.base_password_reset import BasePasswordResetView


class ConfirmPasswordResetCodeView(BasePasswordResetView):
    form_class = ConfirmPasswordResetCodeForm
    template_name = 'user/password_reset/confirm_password_reset_code.html'
    password_reset_step = PasswordResetState.CONFIRM_CODE_STEP

    @method_decorator(ratelimit(key='user.utils.get_client_ip', rate='30/h', block=True))
    @method_decorator(ratelimit(key='user.utils.get_client_ip', rate='100/d', block=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.password_reset_state.user
        method = self.password_reset_state.method
        if method == self.password_reset_state.MOBILE_METHOD:
            contact = user.mobile.number
        else:
            contact = user.email

        if user:
            kwargs.update({'method': method, 'contact': contact})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # remaining_time = MobilePasswordResetCode.remaining_time_to_request_another_code(mobile=mobile)
        # context['remaining_time'] = remaining_time
        return context

    def get_success_url(self):
        return reverse('password-reset-perform')

    def form_valid(self, form):
        response = super().form_valid(form)
        state = self.password_reset_state
        state.set_step(PasswordResetState.PERFORM_STEP)
        state.save(response)
        return response
