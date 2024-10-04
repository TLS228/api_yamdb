from string import digits

from reviews.constants import CONFIRMATION_CODE_LENGTH


def get_confirmation_code(nums=digits):
    return str.join('', set(nums))[:CONFIRMATION_CODE_LENGTH]
