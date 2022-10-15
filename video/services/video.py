import json
import os
import subprocess
from datetime import timedelta
from pathlib import Path
from random import randint

import ffmpeg
from django.conf import settings

from video.models import Video, VideoFormat


class VideoService:

    @staticmethod
    def calculate_video_duration(video_id):
        video = Video.objects.get(id=video_id)
        result = subprocess.run(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                "default=noprint_wrappers=1:nokey=1",
                video.file.path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        duration_in_seconds = int(float(result.stdout))
        duration = timedelta(seconds=duration_in_seconds)
        video.duration = duration
        video.save()

    @classmethod
    def generate_video_poster_and_thumbnail(cls, video_id):
        video = Video.objects.get(id=video_id)

        video_path = video.file.path
        capture_time = randint(5, 20)
        _name = f'{video.code}.jpeg'

        thumbnails_dir = os.path.join(settings.MEDIA_ROOT, Video.THUMBNAILS_UPLOAD_TO_SUBDIR)
        Path(thumbnails_dir).mkdir(parents=True, exist_ok=True)
        thumbnail_path = os.path.join(thumbnails_dir, _name)
        cls.capture_frame_from_video(inp_file_name=video_path, out_file_name=thumbnail_path, capture_time=capture_time,
                                     width=320)
        video.thumbnail = os.path.join(Video.THUMBNAILS_UPLOAD_TO_SUBDIR, _name)

        posters_dir = os.path.join(settings.MEDIA_ROOT, Video.POSTERS_UPLOAD_TO_SUBDIR)
        Path(posters_dir).mkdir(parents=True, exist_ok=True)
        poster_path = os.path.join(posters_dir, _name)
        cls.capture_frame_from_video(inp_file_name=video_path, out_file_name=poster_path, capture_time=capture_time)
        video.poster = os.path.join(Video.POSTERS_UPLOAD_TO_SUBDIR, _name)

        video.save()

    @classmethod
    def generate_video_different_m3u8_files(cls, video_id):
        video = Video.objects.get(id=video_id)
        video_path = video.file.path
        video_formats_dir = video.video_formats_dir_path
        print(video_formats_dir)
        if not os.path.exists(video_formats_dir):
            os.makedirs(video_formats_dir)
        resolution_str = subprocess.getoutput(
            f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of json {video_path}')
        resolution_data = json.loads(resolution_str)
        height = int(resolution_data.get('streams', [{}])[0].get('height'))
        if not height:
            print('invalid video resolution')
            return

        available_qualities_data = VideoFormat.get_video_qualities()
        video_qualities = [quality for quality in available_qualities_data.keys() if quality <= height]

        master_file_path = os.path.join(video_formats_dir, 'master.m3u8')
        master_file_content = '#EXTM3U\n'

        command = f'ffmpeg -hide_banner -y -i {video_path}'
        for quality in video_qualities:
            _quality_data = available_qualities_data[quality]
            quality_str = _quality_data['str']
            width = _quality_data['width']
            height = _quality_data['height']
            resolution = _quality_data['resolution']
            bitrate = _quality_data['bitrate']
            max_bitrate = _quality_data['max_bitrate']
            buffer_size = _quality_data['buffer_size']
            audio_bitrate = _quality_data['audio_bitrate']
            bandwidth = _quality_data['bandwidth']
            command += f' -vf scale=w={width}:h={height}:force_original_aspect_ratio=decrease -c:a aac -ar 48000 -c:v h264 -profile:v main -crf 20 -sc_threshold 0 -g 48 -keyint_min 48 -hls_time 4 -hls_playlist_type vod  -b:v {bitrate} -maxrate {max_bitrate} -bufsize {buffer_size} -b:a {audio_bitrate} -hls_segment_filename {video_formats_dir}/{quality_str}_%03d.ts {video_formats_dir}/{quality_str}.m3u8'
            master_file_content += f'#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={resolution}\n'
            master_file_content += f'{quality_str}.m3u8\n'

            VideoFormat.objects.get_or_create(video=video, quality=quality_str)

        with open(master_file_path, 'w') as f:
            f.write(master_file_content)

        os.system(command=command)

        video.is_available = True
        video.save()

    @staticmethod
    def capture_frame_from_video(inp_file_name, out_file_name, capture_time, width=None):
        if width:
            (
                ffmpeg
                .input(inp_file_name, ss=capture_time)
                .filter('scale', width, -1)
                .output(out_file_name, vframes=1)
                .overwrite_output()
                .run()
            )
        else:
            (
                ffmpeg
                .input(inp_file_name, ss=capture_time)
                .output(out_file_name, vframes=1)
                .overwrite_output()
                .run(overwrite_output=True)
            )
