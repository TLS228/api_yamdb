from string import digits

CONFIRM_CODE_LENGTH = 6


def get_confirmation_code(nums=digits):
    return str.join('', set(nums))[:CONFIRM_CODE_LENGTH]
