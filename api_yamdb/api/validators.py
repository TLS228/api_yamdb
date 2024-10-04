import re

from rest_framework.serializers import ValidationError

from reviews.constants import (USERNAME_REGEX, USERNAME_REGEX_ERROR_MESSAGE,
                               USERNAMES_BLACKLIST)


def username_validator(value):
    if value in USERNAMES_BLACKLIST or not re.match(USERNAME_REGEX, value):
        raise ValidationError(USERNAME_REGEX_ERROR_MESSAGE)
    return value
