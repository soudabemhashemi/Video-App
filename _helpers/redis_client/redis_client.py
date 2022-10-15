from django.conf import settings
from redis import StrictRedis

user_redis_client: StrictRedis = StrictRedis.from_url(settings.USER_REDIS_URL, decode_responses=True)
print("connected to user redis")

report_redis_client: StrictRedis = StrictRedis.from_url(settings.REPORT_REDIS_URL, decode_responses=True)
print("connected to report redis")

video_redis_client: StrictRedis = StrictRedis.from_url(settings.VIDEO_REDIS_URL, decode_responses=True)
print("connected to video redis")
