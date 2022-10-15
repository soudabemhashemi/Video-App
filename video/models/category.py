from django.db.models import Model, CharField, TextField
from django.utils.translation import ugettext_lazy as _


class Category(Model):
    title = CharField(max_length=100, verbose_name=_('Title'))
    icon = TextField(verbose_name=_('Icon'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
