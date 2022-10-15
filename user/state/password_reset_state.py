from typing import Union

from django.contrib.auth.models import User

from user.state import BaseState


class PasswordResetState(BaseState):

    key = 'passresetstate'
    # timeout = VERIFICATION_CODE_EXPIRE_TIME_IN_SECONDS
    timeout = 5 * 60

    BEGIN_STEP = 0
    SELECT_METHOD_STEP = 1
    CONFIRM_CODE_STEP = 2
    PERFORM_STEP = 3

    MOBILE_METHOD = 'mn'
    EMAIL_METHOD = 'ml'

    def __init__(self, user_id, method, step, mobile='', email=''):
        assert mobile or email
        self._user_id = user_id
        self._method = method
        self._step = step
        self._mobile = mobile
        self._email = email

    def _as_dict(self) -> dict:
        return {
            'user_id': self._user_id,
            'method': self._method,
            'step': self._step,
            'mobile': self._mobile,
            'email': self._email
        }

    @classmethod
    def _from_dict(cls, data: dict) -> Union['BaseState', None]:
        try:
            return PasswordResetState(
                user_id=data['user_id'],
                method=data['method'],
                step=data['step'],
                mobile=data['mobile'],
                email=data['email']
            )
        except AssertionError:
            return None

    @property
    def user(self):
        return User.objects.filter(id=self._user_id).first()

    @property
    def method(self):
        return self._method

    def set_method(self, method):
        if method == 'mobile':
            self._method = self.MOBILE_METHOD
        elif method == 'email':
            self._method = self.EMAIL_METHOD

    @property
    def step(self):
        return self._step

    def set_step(self, step):
        self._step = step

    @property
    def mobile(self):
        return self._mobile
