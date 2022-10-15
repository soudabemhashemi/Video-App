import re

from django.utils.translation import gettext_lazy as _


def validate_mobile_number(number):
    regex = re.compile('^09[0-9]{9}$')
    assert regex.match(number), _('Invalid mobile number.')
