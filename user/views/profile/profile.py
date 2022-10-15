from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from user.forms import ProfileForm


class ProfileView(LoginRequiredMixin, FormView):
    form_class = ProfileForm
    template_name = 'user/profile/profile.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user
        kwargs.update({'user': user})
        return kwargs

    def get_success_url(self):
        return reverse('profile')

    def form_valid(self, form):
        messages.success(self.request, _('your info updated successfully.'))
        data = form.cleaned_data
        user = self.request.user
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()
        user.channel.description = data['channel_description']
        user.channel.save()
        return super(ProfileView, self).form_valid(form)
