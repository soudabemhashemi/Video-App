import re

from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, CharField
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from user.models import Mobile
from user.services import AuthService
from user.utils import validate_mobile_number


class MobileNumberSerializer(Serializer):
    mobile = CharField()

    @staticmethod
    def validate_mobile(mobile):
        regex = re.compile('^09[0-9]{9}$')
        if not regex.match(mobile):
            raise ValidationError(_('Invalid mobile number.'))
        return mobile


class EmailAddressSerializer(Serializer):
    email = EmailField()


class MobileManagerSerializer(Serializer):
    mobile = CharField(validators=[validate_mobile_number])
    verification_code = CharField()


class EmailManagerSerializer(Serializer):
    email = EmailField()
    verification_code = CharField()


class MobileManagerView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, *args, **kwargs):
        serializer = MobileNumberSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            AuthService.send_mobile_verification_code(contact=data['mobile'])
            return Response({'success': True})

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = MobileManagerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            data = serializer.validated_data
            is_valid = AuthService.is_submitted_code_verified(
                contact_type=AuthService.CONTACT_TYPE_MOBILE,
                contact=data['mobile'],
                code=data['verification_code']
            )
            if is_valid:
                Mobile.objects.update_or_create(user=user, defaults={'number': data['mobile']})
                return Response({
                    'success': True,
                    'message': _('Mobile number updated successfully.')
                })
            return Response({
                'success': True,
                'message': _('Invalid verification code.')
            }, status=HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, *args, **kwargs):
        user = request.user
        Mobile.objects.filter(user=user).delete()
        return Response({'message': 'mobile deleted.'})


class EmailManagerView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, *args, **kwargs):
        serializer = EmailAddressSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            AuthService.send_email_verification_code(contact=data['email'])
            return Response({'message': 'verification code sent to email.'})

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = EmailManagerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            data = serializer.validated_data
            is_valid = AuthService.is_submitted_code_verified(
                contact_type=AuthService.CONTACT_TYPE_EMAIL,
                contact=data['email'],
                code=data['verification_code']
            )
            if is_valid:
                user.email = data['email']
                user.save()
                return Response({
                    'success': True,
                    'message': _('Email updated successfully.')
                })
            return Response({
                'success': True,
                'message': _('Invalid verification code.')
            }, status=HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, *args, **kwargs):
        user = request.user
        user.email = ''
        user.save()
        return Response({'message': 'email deleted.'})
