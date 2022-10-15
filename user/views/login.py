from django.contrib.auth import views as auth_views

from user.forms import LoginForm
from user.services import VisitorService


class LoginView(auth_views.LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm

    def form_valid(self, form):
        response = super().form_valid(form=form)
        VisitorService.set_user_on_visitor(request=self.request)
        return response
