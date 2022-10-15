from django.contrib import admin, messages
from django.utils.translation import gettext as _, ngettext

from video.models import Video, Channel, Category, Tag, CrawledVideo, Playlist, Link, Report


class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'channel',
        'created_at',
        'category',
        'is_approved',
        'is_available',
        'privacy'
    )

    actions = ('approve_videos', 'disapprove_videos')

    @admin.action(description=_('Approve selected videos'))
    def approve_videos(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(
            request, _('%(updated)d video successfully approved.') % {'updated': updated}, messages.SUCCESS
        )

    @admin.action(description=_('Disapprove selected videos'))
    def disapprove_videos(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(
            request, _('%(updated)d video successfully disapproved.') % {'updated': updated}, messages.SUCCESS
        )


class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'user', 'result')


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(CrawledVideo)
admin.site.register(Playlist)
admin.site.register(Link)
admin.site.register(Report, ReportAdmin)
