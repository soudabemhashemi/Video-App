from django.db.models import Model, CharField, ForeignKey, SET_NULL
from django.utils.translation import ugettext_lazy as _


class Tag(Model):
    title = CharField(max_length=100, verbose_name=_('Title'))
    category = ForeignKey(to='Category', null=True, blank=True, on_delete=SET_NULL, related_name='tags', verbose_name=_('Category'))

    def __str__(self):
        return f'{self.category} - {self.title}'

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
