from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from video.models import Channel


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        subscriber = Channel.objects.get(user=request.user)
        try:
            channel = Channel.objects.get(pk=pk)
        except Channel.DoesNotExist:
            raise ValidationError({
                "channel": "Not found",
            })

        if channel not in subscriber.subscriptions.all():
            subscriber.subscriptions.add(channel)
            return Response({'subscribers': channel.subscribers.count()}, status=status.HTTP_200_OK)
        else:
            raise ValidationError({
                "Subscription": "Failed",
            })
