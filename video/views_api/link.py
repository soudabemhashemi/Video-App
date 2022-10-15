from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from video.models import Link
from video.serializers.other import LinkSerializer


class LinkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def perform_create(self, serializer):
        channel = self.request.user.channel
        serializer.save(channel=channel)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': _('Your link has been successfully registered.')}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        super(LinkViewSet, self).update(request, *args, **kwargs)
        return Response({'success': _('Your link has been successfully registered.')}, status=status.HTTP_200_OK)
