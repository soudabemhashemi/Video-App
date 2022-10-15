from random import randint

from django.conf import settings

from _helpers.redis_client import user_redis_client


class AuthService:

    CONTACT_TYPE_MOBILE = 'mobile'
    CONTACT_TYPE_EMAIL = 'email'
    VERIFICATION_CODE_TIMEOUT = 5 * 60
    VERIFICATION_CODE_TEMPLATE = 'auth:verification:{contact_type}:{contact}'

    @classmethod
    def generate_verification_code(cls, contact_type, contact):
        key = cls.VERIFICATION_CODE_TEMPLATE.format(contact_type=contact_type, contact=contact)
        code = user_redis_client.get(key)
        if not code:
            code = randint(11111, 99999)
            user_redis_client.set(key, code, cls.VERIFICATION_CODE_TIMEOUT)
        return code

    @classmethod
    def send_mobile_verification_code(cls, contact):
        code = cls.generate_verification_code(contact_type=cls.CONTACT_TYPE_MOBILE, contact=contact)
        if settings.DEBUG:
            print(f'verification code send to {cls.CONTACT_TYPE_MOBILE} {contact}, code: {code}.')
        else:  # send code to mobile by KAVENEGAR
            print(f'verification code send to {cls.CONTACT_TYPE_MOBILE} {contact}, code: {code} by KAVENEGAR.')

    @classmethod
    def send_email_verification_code(cls, contact):
        code = cls.generate_verification_code(contact_type=cls.CONTACT_TYPE_EMAIL, contact=contact)
        if settings.DEBUG:
            print(f'verification code send to {cls.CONTACT_TYPE_EMAIL} {contact}, code: {code}')
        else:  # send code to email by KAFTAR
            print(f'verification code send to {cls.CONTACT_TYPE_EMAIL} {contact}, code: {code} by KAFTAR')

    @classmethod
    def is_verification_code_sent(cls, contact_type, contact):
        key = cls.VERIFICATION_CODE_TEMPLATE.format(contact_type=contact_type, contact=contact)
        return user_redis_client.exists(key)

    @classmethod
    def is_submitted_code_verified(cls, contact_type, contact, code):
        key = cls.VERIFICATION_CODE_TEMPLATE.format(contact_type=contact_type, contact=contact)
        verification_code = user_redis_client.get(key)
        return verification_code == code
