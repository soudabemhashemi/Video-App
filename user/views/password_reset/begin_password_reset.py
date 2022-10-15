from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView

from user.forms import BeginPasswordResetForm
from user.state import PasswordResetState


class BeginPasswordResetView(FormView):
    form_class = BeginPasswordResetForm
    template_name = 'user/password_reset/begin_password_reset.html'

    def render_to_response(self, context, **response_kwargs):
        user = self.request.user
        if user.is_authenticated:
            response = HttpResponseRedirect(reverse('password-reset-send'))
            if hasattr(user, 'mobile'):
                mobile = user.mobile.number
            else:
                mobile = ''

            email = user.email or ''

            if mobile:
                method = PasswordResetState.MOBILE_METHOD
            else:
                method = PasswordResetState.EMAIL_METHOD

            state = PasswordResetState(
                user_id=user.id,
                method=method,
                mobile=mobile,
                email=email,
                step=PasswordResetState.SELECT_METHOD_STEP
            )
            state.save(response)
            return response
        return super().render_to_response(context=context, **response_kwargs)

    def get_success_url(self):
        return reverse('password-reset-send')

    def form_valid(self, form):
        data = form.cleaned_data
        user = data.get('user')
        method = data.get('method')
        mobile = data.get('mobile')
        email = data.get('email')
        step = PasswordResetState.SELECT_METHOD_STEP

        response = HttpResponseRedirect(self.get_success_url())
        state = PasswordResetState(user_id=user.id, method=method, mobile=mobile, email=email, step=step)
        state.save(response)
        return response
