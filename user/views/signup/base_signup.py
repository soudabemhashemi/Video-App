from django.contrib.auth import login
from django.urls import reverse
from django.views.generic import FormView

from user.services import VisitorService
from video.models import Channel


class BaseSignupView(FormView):
    template_name = 'user/signup/signup.html'

    def form_valid(self, form):
        user = form.save(commit=True)
        Channel.objects.create(user=user, name=user.username)
        login(request=self.request, user=user)
        VisitorService.set_user_on_visitor(request=self.request)
        return super(BaseSignupView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile')
