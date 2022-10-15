from celery import shared_task

from video.services import VideoService


@shared_task
def process_video(video_id, generate_thumbnail=True):
    calculate_video_duration.apply_async(args=(video_id, ), queue='video')
    if generate_thumbnail:
        generate_video_poster_and_thumbnail.apply_async(args=(video_id, ), queue='video')
    generate_video_different_m3u8_files.apply_async(args=(video_id, ), queue='video')


@shared_task
def calculate_video_duration(video_id):
    VideoService.calculate_video_duration(video_id)


@shared_task
def generate_video_poster_and_thumbnail(video_id):
    VideoService.generate_video_poster_and_thumbnail(video_id)


@shared_task
def generate_video_different_m3u8_files(video_id):
    VideoService.generate_video_different_m3u8_files(video_id)
