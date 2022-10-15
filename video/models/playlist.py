from django.db import models, transaction, IntegrityError
from django.db.models import F
from django.utils.translation import ugettext_lazy as _

from video.utils import generate_playlist_code


class Playlist(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    code = models.CharField(max_length=8, default=generate_playlist_code, unique=True)
    channel = models.ForeignKey(
        to='Channel', on_delete=models.CASCADE, related_name='playlists', verbose_name=_('Channel')
    )
    videos = models.ManyToManyField(
        to='Video', related_name='playlists', verbose_name=_('Videos'), through='PlaylistVideoRelation'
    )
    PRIVACY_PUBLIC = 'PUBLIC'
    PRIVACY_UNLISTED = 'UNLISTED'
    PRIVACY_PRIVATE = 'PRIVATE'
    PRIVACY_CHOICES = (
        (PRIVACY_PUBLIC, PRIVACY_PUBLIC),
        (PRIVACY_UNLISTED, PRIVACY_UNLISTED),
        (PRIVACY_PRIVATE, PRIVACY_PRIVATE),
    )
    privacy = models.CharField(choices=PRIVACY_CHOICES, default=PRIVACY_PUBLIC, max_length=8, verbose_name=_('privacy'))

    CREATED_BY_SYSTEM = 'SYSTEM'
    CREATED_BY_USER = 'USER'
    CREATED_BY_CHOICES = (
        (CREATED_BY_SYSTEM, CREATED_BY_SYSTEM),
        (CREATED_BY_USER, CREATED_BY_USER),
    )
    created_by = models.CharField(
        choices=CREATED_BY_CHOICES, default=CREATED_BY_USER, max_length=8, verbose_name=_('created_by')
    )

    def __str__(self):
        return self.title

    def first_video(self):
        return self.playlistvideorelation_set.order_by('order').first().video

    class Meta:
        verbose_name = _('Playlist')
        verbose_name_plural = _('Playlists')

    def add_video(self, video):
        try:
            self.playlistvideorelation_set.create(video=video)
            success = True
            message = 'video added successfully to playlist'
        except IntegrityError:
            success = False
            message = 'Video already exists in playlist.'
        return success, message

    def remove_video(self, video):
        try:
            item = self.playlistvideorelation_set.get(video=video)
        except PlaylistVideoRelation.DoesNotExist:
            return False, 'Video does not exists in playlist.'

        current_order = item.order
        with transaction.atomic():
            self.playlistvideorelation_set.filter(video=video).delete()
            for item in self.playlistvideorelation_set.filter(order__gt=current_order).order_by('order'):
                self.playlistvideorelation_set.filter(id=item.id).update(order=F('order') - 1)
        return True, 'Video removed successfully from playlist.'

    def update_ordering(self, video, new_order):
        if not self.videos.filter(id=video.id):
            return False, 'Video is not in playlist.'

        orders = {item.video.id: item.order for item in self.playlistvideorelation_set.all()}
        current_order = PlaylistVideoRelation.objects.get(playlist=self, video=video).order
        move_direction = 'up' if new_order < current_order else 'down'
        print(move_direction)
        for item in self.playlistvideorelation_set.exclude(video=video):
            if move_direction == 'up':
                if item.order > current_order:
                    orders[item.video.id] -= 1
                if item.order >= new_order:
                    orders[item.video.id] += 1
            else:
                if item.order > current_order:
                    orders[item.video.id] -= 1
                if item.order > new_order:
                    orders[item.video.id] += 1

        new_order = min(new_order, self.videos.count()-1)
        orders[video.id] = new_order
        print(orders)
        total_items = self.playlistvideorelation_set.count()
        with transaction.atomic():
            self.playlistvideorelation_set.update(order=F('order') + total_items)
            for item in self.playlistvideorelation_set.all():
                self.playlistvideorelation_set.filter(id=item.id).update(order=orders[item.video.id])

        return True, 'video order updated successfully in playlist.'


class PlaylistVideoRelation(models.Model):
    added_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Added at'))
    playlist = models.ForeignKey(to='Playlist', on_delete=models.CASCADE)
    video = models.ForeignKey(to='Video', on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name=_('Playlist order'))

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = self.playlist.videos.count()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = (('playlist', 'video'), ('playlist', 'order'))
