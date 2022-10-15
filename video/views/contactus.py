from django.views.generic.edit import FormView
from video.forms.contactus import ContactUsForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from video.mixin import CategoryMixinView


class ContactUsFormView(CategoryMixinView, FormView):
    form_class = ContactUsForm
    template_name = 'video/contact_us/contact_us_page.html'

    def form_valid(self, form):
        messages.success(self.request, _('Form submission successful'))
        post = form.save(commit=False)
        if self.request.user.username != '':
            post.user = self.request.user
        form.save()
        return super(ContactUsFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('video:contact_us')
