from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse

from user.forms import PerformPasswordResetForm
from user.state import PasswordResetState
from user.views.password_reset.base_password_reset import BasePasswordResetView


class PerformPasswordResetView(BasePasswordResetView):
    form_class = PerformPasswordResetForm
    template_name = 'user/password_reset/perform_password_reset.html'
    password_reset_step = PasswordResetState.PERFORM_STEP

    def get(self, request, *args, **kwargs):
        state = self.password_reset_state
        if state and state.user:
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('password-reset-begin'))

    def get_success_url(self):
        return reverse('account_login')

    def form_valid(self, form):
        state = self.password_reset_state
        password = form.cleaned_data.get('password2')
        user = state.user
        if user:
            user.set_password(raw_password=password)
            user.save()
            response = HttpResponseRedirect(reverse('login'))
            state.delete(response)
            messages.success(self.request, 'گذرواژه شما با موفقیت تغییر کرد.')
            return response

        form.add_error(None, 'مشکلی پیش آمده است. دوباره تلاش کنید.')
        return super().form_invalid(form)
