import os
from PIL import Image

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from _base.settings import BASE_DIR
from video.models import Video, Tag, Category
from video.serializers import VideoSerializer


class EditVideoAPIView(ModelViewSet):
    lookup_field = "code"
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        video = self.get_object()

        video_tags = video.tags.all()
        tags_str = []
        if request.data.get('tags'):
            tags_str = request.data.get('tags').split(',')
        for video_tag in video_tags:
            if video_tag.title not in tags_str:
                video.tags.remove(video_tag)
        for tag_title in tags_str:
            if not video_tags.filter(title=tag_title.strip()).exists():
                new_tag = Tag.objects.create(
                    title=tag_title,
                    category=Category.objects.get(title=video.category.title)
                ) if not Tag.objects.filter(
                    title=tag_title,
                    category=Category.objects.get(title=video.category.title)
                ).exists() else Tag.objects.get(
                    title=tag_title,
                    category=Category.objects.get(title=video.category.title)
                )
                video.tags.add(new_tag)

        input_thumbnail = request.data.get('thumbnail')
        if input_thumbnail:
            video.poster = input_thumbnail
            basewidth = 320
            img = Image.open(input_thumbnail)
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            save_to = os.path.join(BASE_DIR, 'media/video/thumbnails/')
            save_to += f'{video.code}_thumbnail.jpeg'
            img.convert('RGB').save(save_to)
            video.thumbnail = os.path.join('video/thumbnails/', f'{video.code}_thumbnail.jpeg')

        video.save()
        serializer = VideoSerializer(video, partial=True)
        return Response(serializer.data)
