from typing import Union

from django.core import signing
from django.http import HttpResponse, HttpRequest


class BaseState:
    key = ''
    timeout = 1 * 60 * 60

    def _as_dict(self) -> dict:
        return {}

    @classmethod
    def _from_dict(cls, data: dict) -> Union['BaseState', None]:
        raise cls()

    def save(self, response: HttpResponse):
        """
        Saves state in cookie
        :param response:
        :return:
        """
        response.set_cookie(
            key=self.key,
            value=signing.dumps(self._as_dict()),
            max_age=self.timeout,
            samesite='LAX'
        )

    def delete(self, response: HttpResponse):
        """
        Deletes state from cookie
        :param response:
        :return:
        """
        response.delete_cookie(key=self.key)

    @classmethod
    def load(cls, request: HttpRequest) -> Union['BaseState', None]:
        try:
            encoded = request.COOKIES.get(cls.key)
            if not encoded:
                return None

            data = signing.loads(encoded, max_age=cls.timeout)
            return cls._from_dict(data)
        except (signing.BadSignature, signing.SignatureExpired, AssertionError):
            return None

    @staticmethod
    def _remove_null_values_from_dict(data: dict):
        for key, value in list(data.items()):
            if value is None:
                del data[key]

        return data
