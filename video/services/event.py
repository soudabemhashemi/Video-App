from django.utils import timezone
from redis.exceptions import ConnectionError

from _helpers.redis_client import report_redis_client


class EventService:
    VISIT_KEY_PATTERN = 'events:video:visit:{ts}'
    PLAY_KEY_PATTERN = 'events:video:play:{ts}'

    ITEM_PATTERN = '{video_code}:{visitor_uuid}'

    @classmethod
    def log_visit(cls, video, visitor_uuid, user):
        timestamp = int(timezone.now().timestamp() // 300 * 300)
        name = cls.VISIT_KEY_PATTERN.format(ts=timestamp)
        user_channel_id = user.channel.id if user else None
        value = f'{video.id}:{video.channel_id}:{visitor_uuid}:{user_channel_id}'
        try:
            report_redis_client.sadd(name, value)
        except ConnectionError:
            print('Failed to log video visit, redis down!')

    @classmethod
    def log_watch(cls, video, video_time, visitor_uuid, user):
        timestamp = int(timezone.now().timestamp() // 300 * 300)
        name = cls.VISIT_KEY_PATTERN.format(ts=timestamp)
        user_channel_id = user.channel.id if user else None
        value = f'{video.id}:{video_time}:{video.channel_id}:{visitor_uuid}:{user_channel_id}'
        try:
            report_redis_client.sadd(name, value)
        except ConnectionError:
            print('Failed to log video watch, redis down!')
