import datetime
import re

from rest_framework.serializers import ValidationError

from reviews.constants import (USERNAME_REGEX, USERNAME_REGEX_ERROR_MESSAGE,
                               USERNAMES_BLACKLIST)


def username_validator(value):
    if value in USERNAMES_BLACKLIST or not re.match(USERNAME_REGEX, value):
        raise ValidationError(USERNAME_REGEX_ERROR_MESSAGE)
    return value


def year_validator(value):
    current_year = datetime.date.today().year
    if value > current_year:
        raise ValidationError(f'Год не может быть больше, чем {current_year}')
