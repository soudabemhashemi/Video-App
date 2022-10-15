import time

from django.contrib.auth.models import User
from django.db.models import DateTimeField, ForeignKey
from django.db.models import Model, OneToOneField, CASCADE, CharField, ImageField, TextField, ManyToManyField
from django.core.validators import FileExtensionValidator
from django.utils.translation import ugettext_lazy as _
import jdatetime

from _helpers.models import BaseModel
from video.utils import FileSizeValidator, generate_channel_code

KB = 1024


class Channel(BaseModel):
    name = CharField(max_length=100, verbose_name=_('Name'), unique=True, default=generate_channel_code)
    title = CharField(max_length=100, verbose_name=_('Title'))
    user = OneToOneField(to=User, on_delete=CASCADE, verbose_name=_('User'))
    description = TextField(verbose_name=_('Description'))
    subscriptions = ManyToManyField(
        to='self', blank=True, symmetrical=False, through='Subscription', related_name='subscribers'
    )
    avatar = ImageField(
        upload_to='video/avatars/',
        validators=[
            FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']),
            FileSizeValidator(max_size=1000 * KB)
        ],
        null=True
    )
    cover = ImageField(
        upload_to='video/covers/',
        validators=[
            FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']),
            FileSizeValidator(max_size=1000 * KB)
        ],
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_created = not self.id
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        if is_created:
            self.create_initial_playlists()

    def create_initial_playlists(self):
        from video.models import Playlist
        Playlist.objects.create(
            channel=self, title='LL', privacy=Playlist.PRIVACY_PRIVATE, created_by=Playlist.CREATED_BY_SYSTEM
        )
        time.sleep(0.1)  # todo: fix this
        Playlist.objects.create(
            channel=self, title='WL', privacy=Playlist.PRIVACY_PRIVATE, created_by=Playlist.CREATED_BY_SYSTEM
        )
        time.sleep(0.1)  # todo: and this

    @property
    def watch_later_playlist(self):
        return self.playlists.get(title='WL')

    @property
    def liked_playlist(self):
        return self.playlists.get(title='LL')

    def jalil_date(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_at.date()).strftime("%Y/%m/%d")


class Subscription(Model):
    from_channel = ForeignKey(Channel, related_name='subscriber', on_delete=CASCADE)
    to_channel = ForeignKey(Channel, related_name='subscription', on_delete=CASCADE)
    subscribed_at = DateTimeField(auto_now_add=True)
