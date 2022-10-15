from django.core.exceptions import ValidationError
from django.db.models import Model, ForeignKey, CASCADE, CharField
from django.utils.translation import ugettext_lazy as _


def validate_url(value):
    if not value:
        return
    if not '.' in value or value.startswith('.'):
        raise ValidationError(_('Enter a valid url.'))


class Link(Model):
    channel = ForeignKey(to='Channel', on_delete=CASCADE, related_name='links', verbose_name=_('Channel'))
    title = CharField(max_length=100, verbose_name=_('Title'))
    link = CharField(max_length=500, verbose_name=_('Link'), validators=[validate_url])

    def __str__(self):
        return f'{self.channel} - {self.title}'

    class Meta:
        unique_together = (('channel', 'title'), ('channel', 'link'))
        verbose_name = _('Link')
        verbose_name_plural = _('Links')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not (self.link.startswith('https://') or self.link.startswith('http://')):
            self.link = f'https://{self.link}'

        return super(Link, self).save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
        )