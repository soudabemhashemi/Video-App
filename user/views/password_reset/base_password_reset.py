from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from ratelimit.decorators import ratelimit

from user.state import PasswordResetState


class BasePasswordResetView(FormView):

    password_reset_step = 0

    @method_decorator(ratelimit(key='user.utils.get_client_ip', rate='30/h', block=True))
    @method_decorator(ratelimit(key='user.utils.get_client_ip', rate='100/d', block=True))
    def dispatch(self, request, *args, **kwargs):
        password_reset_state = PasswordResetState.load(request)
        if not password_reset_state or not password_reset_state.user or \
                password_reset_state.step < self.password_reset_step:
            return HttpResponseRedirect(reverse('password-reset-begin'))
        self.password_reset_state = password_reset_state
        return super().dispatch(request, *args, **kwargs)

from django.contrib.auth.models import User