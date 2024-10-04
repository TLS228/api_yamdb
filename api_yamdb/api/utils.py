from string import digits


def get_confirmation_code(code_length, nums=digits):
    return str.join('', set(nums))[:code_length]
